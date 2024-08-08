import psutil
from src.logger import logger
from src.config_manager import config_manager

class ResourceMonitor:
    def __init__(self):
        self.cpu_threshold = config_manager.get('resource_threshold')['cpu']
        self.memory_threshold = config_manager.get('resource_threshold')['memory']

    def check_resources(self):
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent

        if cpu_percent > self.cpu_threshold or memory_percent > self.memory_threshold:
            logger.warning(f"High resource usage: CPU {cpu_percent}%, Memory {memory_percent}%")

        return {
            'cpu': cpu_percent,
            'memory': memory_percent,
            'disk': psutil.disk_usage('/').percent
        }

    def get_system_info(self):
        return {
            'cpu_count': psutil.cpu_count(),
            'total_memory': psutil.virtual_memory().total,
            'total_disk': psutil.disk_usage('/').total
        }

resource_monitor = ResourceMonitor()