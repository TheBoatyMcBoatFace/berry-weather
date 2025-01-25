# station/sensors/system.py
import os
import psutil

def get_system_stats():
    """
    Collect system performance stats (CPU, memory, disk usage).
    Returns:
        dict: System stats with keys for CPU, memory, and disk usage.
    """
    return {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent,
    }
