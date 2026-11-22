"""
SQLite Database Layer for Behaviour-Aware Zero Trust Framework.
Provides structured storage, thread safety, and query utilities.
"""
import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from config import DB_PATH, DEFAULT_DEVICES

logger = logging.getLogger("DBManager")

class DatabaseManager:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = str(db_path)
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Creates tables and pre-populates initial devices if empty."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Devices Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                device_type TEXT NOT NULL,
                role TEXT NOT NULL,
                secret_hash TEXT NOT NULL,
                auth_status TEXT DEFAULT 'UNAUTHENTICATED',
                current_trust REAL DEFAULT 95.0,
                current_confidence REAL DEFAULT 0.85,
                risk_level TEXT DEFAULT 'LOW',
                access_policy TEXT DEFAULT 'ALLOW',
                allowed_publish TEXT,
                allowed_subscribe TEXT,
                sensitivity TEXT DEFAULT 'LOW',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # 2. Authentication Events
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS auth_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL,
                failure_reason TEXT,
                nonce TEXT
            );
            """)

            # 3. Behavior Records (Sliding Window metrics)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS behavior_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                window_sec REAL DEFAULT 5.0,
                msg_count INTEGER DEFAULT 0,
                rate_hz REAL DEFAULT 0.0,
                rate_anomaly REAL DEFAULT 0.0,
                payload_mean REAL DEFAULT 0.0,
                payload_anomaly REAL DEFAULT 0.0,
                unauth_attempts INTEGER DEFAULT 0,
                auth_failures INTEGER DEFAULT 0,
                reconnections INTEGER DEFAULT 0,
                replay_attempts INTEGER DEFAULT 0
            );
            """)

            # 4. Network Metrics
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS network_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                avg_latency_ms REAL DEFAULT 15.0,
                packet_loss_pct REAL DEFAULT 0.5,
                throughput_msg_sec REAL DEFAULT 10.0,
                broker_delay_ms REAL DEFAULT 1.2,
                cpu_pct REAL DEFAULT 10.0,
                ram_pct REAL DEFAULT 35.0,
                is_congested INTEGER DEFAULT 0,
                affected_devices_count INTEGER DEFAULT 0
            );
            """)

            # 5. Trust History
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS trust_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                raw_risk REAL,
                calculated_trust REAL,
                previous_trust REAL,
                smoothed_trust REAL,
                confidence_score REAL,
                network_context_discount REAL DEFAULT 0.0,
                breakdown_json TEXT,
                reason TEXT
            );
            """)

            # 6. Security Event Log
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                device_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                trust_before REAL,
                trust_after REAL,
                policy_decision TEXT,
                reason TEXT
            );
            """)

            # 7. Dynamic Nonce Challenges
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenge_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                nonce TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'PENDING',
                verified_at TIMESTAMP
            );
            """)

            # 8. Experiment Results (for Research Evaluation)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiment_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                experiment_name TEXT NOT NULL,
                model_variant TEXT NOT NULL,
                precision REAL,
                recall REAL,
                f1_score REAL,
                fpr REAL,
                detection_time_ms REAL,
                unauth_success_pct REAL,
                legit_success_pct REAL,
                revocation_delay_ms REAL,
                policy_latency_ms REAL,
                evaluations_count INTEGER,
                raw_metrics_json TEXT
            );
            """)

            conn.commit()

            # Populate initial devices if none exist
            cursor.execute("SELECT COUNT(*) FROM devices;")
            if cursor.fetchone()[0] == 0:
                import hashlib
                for dev in DEFAULT_DEVICES:
                    # Default secret is device_id + "_secret_2026"
                    secret_hash = hashlib.sha256(f"{dev['device_id']}_secret_2026".encode()).hexdigest()
                    cursor.execute("""
                    INSERT INTO devices (
                        device_id, device_type, role, secret_hash, auth_status,
                        current_trust, current_confidence, risk_level, access_policy,
                        allowed_publish, allowed_subscribe, sensitivity
                    ) VALUES (?, ?, ?, ?, 'AUTHENTICATED', ?, 0.90, 'LOW', 'ALLOW', ?, ?, ?);
                    """, (
                        dev["device_id"],
                        dev["device_type"],
                        dev["role"],
                        secret_hash,
                        dev["initial_trust"],
                        json.dumps(dev["allowed_publish"]),
                        json.dumps(dev["allowed_subscribe"]),
                        dev["sensitivity"]
                    ))
                conn.commit()
                logger.info("Initialized default IoT devices in SQLite database.")

    # --- Device Operations ---
    def get_all_devices(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devices ORDER BY device_id ASC;")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_device(self, device_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devices WHERE device_id = ?;", (device_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_device_trust(self, device_id: str, trust: float, confidence: float, risk_level: str, access_policy: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE devices 
            SET current_trust = ?, current_confidence = ?, risk_level = ?, access_policy = ?, last_seen = CURRENT_TIMESTAMP
            WHERE device_id = ?;
            """, (trust, confidence, risk_level, access_policy, device_id))
            conn.commit()

    def update_device_auth_status(self, device_id: str, status: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE devices SET auth_status = ?, last_seen = CURRENT_TIMESTAMP WHERE device_id = ?;", (status, device_id))
            conn.commit()

    # --- Logging and Records ---
    def log_auth_event(self, device_id: str, status: str, failure_reason: Optional[str] = None, nonce: Optional[str] = None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO auth_events (device_id, status, failure_reason, nonce)
            VALUES (?, ?, ?, ?);
            """, (device_id, status, failure_reason, nonce))
            conn.commit()

    def log_behavior(self, device_id: str, data: Dict[str, Any]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO behavior_records (
                device_id, window_sec, msg_count, rate_hz, rate_anomaly,
                payload_mean, payload_anomaly, unauth_attempts, auth_failures,
                reconnections, replay_attempts
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                device_id,
                data.get("window_sec", 5.0),
                data.get("msg_count", 0),
                data.get("rate_hz", 0.0),
                data.get("rate_anomaly", 0.0),
                data.get("payload_mean", 0.0),
                data.get("payload_anomaly", 0.0),
                data.get("unauth_attempts", 0),
                data.get("auth_failures", 0),
                data.get("reconnections", 0),
                data.get("replay_attempts", 0)
            ))
            conn.commit()

    def log_network_metric(self, metric: Dict[str, Any]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO network_metrics (
                avg_latency_ms, packet_loss_pct, throughput_msg_sec,
                broker_delay_ms, cpu_pct, ram_pct, is_congested, affected_devices_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                metric.get("avg_latency_ms", 15.0),
                metric.get("packet_loss_pct", 0.5),
                metric.get("throughput_msg_sec", 10.0),
                metric.get("broker_delay_ms", 1.2),
                metric.get("cpu_pct", 10.0),
                metric.get("ram_pct", 35.0),
                1 if metric.get("is_congested") else 0,
                metric.get("affected_devices_count", 0)
            ))
            conn.commit()

    def log_trust_evaluation(self, eval_data: Dict[str, Any]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO trust_history (
                device_id, raw_risk, calculated_trust, previous_trust,
                smoothed_trust, confidence_score, network_context_discount,
                breakdown_json, reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                eval_data["device_id"],
                eval_data["raw_risk"],
                eval_data["calculated_trust"],
                eval_data["previous_trust"],
                eval_data["smoothed_trust"],
                eval_data["confidence_score"],
                eval_data.get("network_context_discount", 0.0),
                json.dumps(eval_data.get("breakdown", {})),
                eval_data.get("reason", "")
            ))
            conn.commit()

    def log_security_event(self, event: Dict[str, Any]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO security_events (
                device_id, event_type, severity, description,
                trust_before, trust_after, policy_decision, reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                event["device_id"],
                event["event_type"],
                event["severity"],
                event["description"],
                event.get("trust_before", 0.0),
                event.get("trust_after", 0.0),
                event.get("policy_decision", "DENY"),
                event.get("reason", "")
            ))
            conn.commit()

    # --- Query helpers for Dashboard & Analytics ---
    def get_latest_network_metrics(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM network_metrics ORDER BY id DESC LIMIT ?;", (limit,))
            rows = cursor.fetchall()
            return [dict(r) for r in reversed(rows)]

    def get_device_trust_history(self, device_id: str, limit: int = 60) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trust_history WHERE device_id = ? ORDER BY id DESC LIMIT ?;", (device_id, limit))
            rows = cursor.fetchall()
            return [dict(r) for r in reversed(rows)]

    def get_recent_security_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM security_events ORDER BY id DESC LIMIT ?;", (limit,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def reset_all_data(self):
        """Resets dynamic history while restoring default devices to clean state."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM auth_events;")
            cursor.execute("DELETE FROM behavior_records;")
            cursor.execute("DELETE FROM network_metrics;")
            cursor.execute("DELETE FROM trust_history;")
            cursor.execute("DELETE FROM security_events;")
            cursor.execute("DELETE FROM challenge_records;")
            cursor.execute("DELETE FROM experiment_results;")
            cursor.execute("""
            UPDATE devices 
            SET auth_status = 'AUTHENTICATED', current_trust = 95.0, 
                current_confidence = 0.90, risk_level = 'LOW', access_policy = 'ALLOW',
                last_seen = CURRENT_TIMESTAMP;
            """)
            conn.commit()
            logger.info("Database reset completed.")

