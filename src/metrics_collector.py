import time
from src.logger import logger

class MetricsCollector:
    def __init__(self):
        self.start_time = time.time()
        self.email_count = 0
        self.error_count = 0

    def increment_email_count(self):
        self.email_count += 1

    def increment_error_count(self):
        self.error_count += 1

    def get_metrics(self):
        uptime = time.time() - self.start_time
        return {
            'uptime': uptime,
            'email_count': self.email_count,
            'error_count': self.error_count
        }

    def log_metrics(self):
        metrics = self.get_metrics()
        logger.info(f"Metrics: {metrics}")

metrics_collector = MetricsCollector()