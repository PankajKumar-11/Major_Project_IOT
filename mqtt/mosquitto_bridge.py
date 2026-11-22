"""
Mosquitto Bridge for connecting to a live local Mosquitto broker if available.
"""
from traitlets import Any
import logging
import threading
from typing import Optional, Callable

try:
    import paho.mqtt.client as mqtt
    PAHO_AVAILABLE = True
except ImportError:
    PAHO_AVAILABLE = False

logger = logging.getLogger("MosquittoBridge")

class MosquittoBridge:
    def __init__(self, host: str = "localhost", port: int = 1883):
        self.host = host
        self.port = port
        self.client: Optional[Any] = None
        self.is_connected = False

    def connect(self, client_id: str = "zerotrust_orchestrator", username: str = None, password: str = None) -> bool:
        if not PAHO_AVAILABLE:
            logger.warning("paho-mqtt is not installed. Real Mosquitto bridge disabled.")
            return False

        try:
            # Paho MQTT 2.x compatibility
            try:
                self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
            except AttributeError:
                self.client = mqtt.Client(client_id=client_id)

            if username and password:
                self.client.username_pw_set(username, password)

            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            
            # Non-blocking attempt with short timeout
            self.client.connect(self.host, self.port, keepalive=30)
            self.client.loop_start()
            return True
        except Exception as e:
            logger.info(f"Mosquitto broker not reachable at {self.host}:{self.port} ({e}). Simulation mode will be used.")
            self.is_connected = False
            return False

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.is_connected = True
            logger.info(f"Connected to live Mosquitto broker at {self.host}:{self.port}")
        else:
            self.is_connected = False
            logger.warning(f"Connection to Mosquitto failed with code {rc}")

    def _on_disconnect(self, client, userdata, rc, properties=None):
        self.is_connected = False
        logger.info("Disconnected from live Mosquitto broker.")

    def publish(self, topic: str, payload: str, qos: int = 0) -> bool:
        if self.client and self.is_connected:
            self.client.publish(topic, payload, qos=qos)
            return True
        return False

    def disconnect(self):
        if self.client and self.is_connected:
            self.client.loop_stop()
            self.client.disconnect()
            self.is_connected = False

