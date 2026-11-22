"""
Adaptive Verification Scheduler.
Adjusts reassessment frequency based on real-time risk levels:
- LOW RISK: Every 30 seconds
- MEDIUM RISK: Every 10 seconds
- HIGH RISK: Every 2 seconds
- Critical security violations trigger instant evaluation.
"""
import time
import logging
from typing import Dict
from config import REASSESSMENT_INTERVALS

logger = logging.getLogger("AdaptiveScheduler")

class AdaptiveVerificationScheduler:
    def __init__(self, intervals: Dict[str, float] = None):
        self.intervals = intervals or dict(REASSESSMENT_INTERVALS)
        # device_id -> last_evaluation_timestamp
        self.last_eval_time: Dict[str, float] = {}

    def get_interval(self, risk_level: str) -> float:
        """Returns required reassessment interval in seconds."""
        if risk_level == "HIGH":
            return self.intervals.get("HIGH_RISK", 2.0)
        elif risk_level == "MEDIUM":
            return self.intervals.get("MEDIUM_RISK", 10.0)
        else:
            return self.intervals.get("LOW_RISK", 30.0)

    def is_due_for_reassessment(self, device_id: str, risk_level: str) -> bool:
        """Checks if device should undergo re-evaluation now based on its risk interval."""
        now = time.time()
        last = self.last_eval_time.get(device_id, 0.0)
        interval = self.get_interval(risk_level)
        return (now - last) >= interval

    def mark_evaluated(self, device_id: str):
        self.last_eval_time[device_id] = time.time()

    def trigger_immediate_evaluation(self, device_id: str):
        """Forces immediate reassessment (e.g. following high-severity event)."""
        self.last_eval_time[device_id] = 0.0

