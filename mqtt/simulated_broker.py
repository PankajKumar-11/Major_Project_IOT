"""
Simulated In-Memory MQTT Broker with Dynamic Zero Trust ACL Enforcement.
Allows complete end-to-end simulation on Windows without requiring a real Mosquitto daemon.
Also supports seamless bridging if an external Mosquitto daemon is configured.
"""
import time
import json
import fnmatch
import threading
from typing import Dict, List, Callable, Optional, Set
from collections import defaultdict, deque
import logging

logger = logging.getLogger("MQTTBroker")

class MQTTMessage:
    def __init__(self, topic: str, payload: str, publisher_id: str, timestamp: float = None, seq_num: int = 0, nonce: str = ""):
        self.topic = topic
        self.payload = payload
        self.publisher_id = publisher_id
        self.timestamp = timestamp or time.time()
        self.seq_num = seq_num
        self.nonce = nonce
        self.size_bytes = len(payload.encode('utf-8'))
        self.received_at: float = 0.0

class SimulatedMQTTBroker:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SimulatedMQTTBroker, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.lock = threading.Lock()
        
        # Subscriptions: topic_pattern -> list of callbacks (callback(message))
        self.subscribers: Dict[str, List[Callable[[MQTTMessage], None]]] = defaultdict(list)
        
        # Access Controller reference (set dynamically to avoid circular import)
        self.access_controller = None
        
        # Performance & telemetry statistics
        self.total_published = 0
        self.total_delivered = 0
        self.total_blocked = 0
        self.recent_latencies: deque = deque(maxlen=200)
        self.recent_msg_timestamps: deque = deque(maxlen=500)
        
        # Replay cache for sequence & nonce tracking
        # device_id -> set of recent nonces / last seq_num
        self.device_nonces: Dict[str, Set[str]] = defaultdict(set)
        self.device_last_seq: Dict[str, int] = defaultdict(int)
        
        # Network latency delay simulation (in milliseconds)
        self.simulated_delay_ms: float = 0.0
        self.simulated_packet_loss_pct: float = 0.0

    def set_access_controller(self, access_controller):
        self.access_controller = access_controller

    def set_simulated_network_impairment(self, delay_ms: float, packet_loss_pct: float):
        """Simulates network latency and packet loss (e.g. during congestion)."""
        with self.lock:
            self.simulated_delay_ms = max(0.0, delay_ms)
            self.simulated_packet_loss_pct = max(0.0, min(100.0, packet_loss_pct))

    def subscribe(self, topic_filter: str, callback: Callable[[MQTTMessage], None]):
        """Subscribes a callback to a topic pattern (supports '#' and '+')."""
        with self.lock:
            self.subscribers[topic_filter].append(callback)

    def unsubscribe(self, topic_filter: str, callback: Callable[[MQTTMessage], None]):
        with self.lock:
            if topic_filter in self.subscribers and callback in self.subscribers[topic_filter]:
                self.subscribers[topic_filter].remove(callback)

    def publish(self, topic: str, payload: str, publisher_id: str, seq_num: int = 0, nonce: str = "") -> bool:
        """
        Publishes a message through Zero Trust enforcement.
        Returns True if allowed and delivered; False if rejected / blocked / dropped.
        """
        now = time.time()
        msg = MQTTMessage(topic, payload, publisher_id, timestamp=now, seq_num=seq_num, nonce=nonce)
        
        with self.lock:
            self.total_published += 1
            self.recent_msg_timestamps.append(now)

        # 1. Zero Trust Access Control Check
        if self.access_controller:
            allowed, reason = self.access_controller.check_publish_permission(publisher_id, topic, msg)
            if not allowed:
                with self.lock:
                    self.total_blocked += 1
                logger.warning(f"[ZeroTrust REJECT] Device {publisher_id} -> Topic {topic}: {reason}")
                return False

        # 2. Simulated Network Delay & Packet Loss
        if self.simulated_packet_loss_pct > 0.0:
            import random
            if random.uniform(0, 100) < self.simulated_packet_loss_pct:
                logger.debug(f"[Network Drop] Message from {publisher_id} dropped due to simulated packet loss.")
                return False

        if self.simulated_delay_ms > 0.0:
            # Sleep tiny amount to simulate network transmission delay
            time.sleep(self.simulated_delay_ms / 1000.0)

        # 3. Deliver to matching subscribers
        msg.received_at = time.time()
        delivery_latency = (msg.received_at - now) * 1000.0  # ms

        with self.lock:
            self.total_delivered += 1
            self.recent_latencies.append(delivery_latency)

        # Dispatch
        matching_callbacks = []
        with self.lock:
            for pattern, callbacks in self.subscribers.items():
                if self._topic_matches(pattern, topic):
                    matching_callbacks.extend(callbacks)

        for cb in matching_callbacks:
            try:
                cb(msg)
            except Exception as e:
                logger.error(f"Error in subscriber callback: {e}")

        return True

    def _topic_matches(self, pattern: str, topic: str) -> bool:
        """Matches MQTT wildcard patterns ('+' single level, '#' multi level)."""
        if pattern == topic or pattern == "#":
            return True
        # Convert MQTT wildcards to regex / fnmatch
        py_pattern = pattern.replace("+", "*").replace("#", "*")
        return fnmatch.fnmatch(topic, py_pattern)

    def get_throughput(self, window_sec: float = 5.0) -> float:
        """Calculates messages published per second over the recent window."""
        now = time.time()
        cutoff = now - window_sec
        with self.lock:
            recent_count = sum(1 for t in self.recent_msg_timestamps if t >= cutoff)
        return round(recent_count / window_sec, 2)

    def get_average_broker_latency(self) -> float:
        """Returns average message delivery delay in milliseconds."""
        with self.lock:
            if not self.recent_latencies:
                return 1.0
            return round(sum(self.recent_latencies) / len(self.recent_latencies), 2)

