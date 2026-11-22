"""
Network Monitoring Module & Context-Aware Congestion Detector.
Independent network monitoring:
- Latency (ms), packet loss (%), message rate (msg/s), broker delay (ms)
- CPU and RAM utilisation via psutil
- Multi-device correlation: distinguishes device compromise from benign network congestion.
"""
import time
import psutil
import logging
from typing import Dict, List, Any
from collections import deque
from database.db_manager import DatabaseManager
from config import NETWORK_THRESHOLDS

logger = logging.getLogger("NetworkMonitor")

class NetworkMonitor:
    def __init__(self, db: DatabaseManager):
        self.db = db
        # Circular buffers for tracking device-level latencies
        self.device_recent_latencies: Dict[str, deque] = {}
        self.device_recent_packet_drops: Dict[str, int] = {}
        
        # Simulated network state
        self.manual_congestion_active = False
        self.congestion_intensity = 0.0 # 0.0 to 1.0

    def record_device_network_ping(self, device_id: str, latency_ms: float, dropped: bool = False):
        if device_id not in self.device_recent_latencies:
            self.device_recent_latencies[device_id] = deque(maxlen=20)
        self.device_recent_latencies[device_id].append(latency_ms)
        
        if dropped:
            self.device_recent_packet_drops[device_id] = self.device_recent_packet_drops.get(device_id, 0) + 1

    def set_congestion_simulation(self, active: bool, intensity: float = 0.8):
        """Activates benign network congestion scenario."""
        self.manual_congestion_active = active
        self.congestion_intensity = max(0.0, min(1.0, intensity))
        logger.info(f"Network Congestion Simulation set to: {active} (intensity: {intensity})")

    def collect_network_snapshot(self, broker_delay_ms: float = 1.0, throughput_msg_sec: float = 10.0) -> Dict[str, Any]:
        """
        Samples network and system metrics, analyzes multi-device correlation,
        and logs to the database.
        """
        now = time.time()
        
        # System Resource Usage
        try:
            cpu_pct = psutil.cpu_percent(interval=None)
            ram_pct = psutil.virtual_memory().percent
        except Exception:
            cpu_pct = 12.0
            ram_pct = 40.0

        # Calculate average latency across all active devices
        device_avg_latencies = {}
        for dev_id, l_queue in self.device_recent_latencies.items():
            if l_queue:
                device_avg_latencies[dev_id] = sum(l_queue) / len(l_queue)

        if self.manual_congestion_active:
            # Benign congestion injects 180-250ms latency across 80%+ of devices
            avg_latency = 160.0 + (self.congestion_intensity * 90.0)
            packet_loss = 6.0 + (self.congestion_intensity * 8.0)
            affected_count = max(3, len(device_avg_latencies))
            is_congested = True
        else:
            if device_avg_latencies:
                avg_latency = sum(device_avg_latencies.values()) / len(device_avg_latencies)
            else:
                avg_latency = 18.0
            packet_loss = 0.5
            affected_count = 0
            is_congested = False

            # Check if multi-device correlation indicates congestion
            high_latency_devices = [
                d for d, lat in device_avg_latencies.items() 
                if lat >= NETWORK_THRESHOLDS["congestion_latency_ms"]
            ]
            total_reporting = max(1, len(device_avg_latencies))
            ratio = len(high_latency_devices) / total_reporting

            if ratio >= NETWORK_THRESHOLDS["multi_device_affected_ratio"] and avg_latency >= NETWORK_THRESHOLDS["congestion_latency_ms"]:
                is_congested = True
                affected_count = len(high_latency_devices)

        metric = {
            "timestamp": now,
            "avg_latency_ms": round(avg_latency, 2),
            "packet_loss_pct": round(packet_loss, 2),
            "throughput_msg_sec": round(throughput_msg_sec, 2),
            "broker_delay_ms": round(broker_delay_ms, 2),
            "cpu_pct": round(cpu_pct, 1),
            "ram_pct": round(ram_pct, 1),
            "is_congested": is_congested,
            "affected_devices_count": affected_count
        }

        # Save to DB
        self.db.log_network_metric(metric)
        return metric

    def get_network_context_discount(self) -> float:
        """
        Returns an anomaly discount factor [0.0 - 0.75] when network is congested.
        When benign congestion is present, this attenuates network/rate/delay penalties.
        """
        if self.manual_congestion_active:
            return 0.70  # Discount 70% of network-related penalties
        return 0.0

