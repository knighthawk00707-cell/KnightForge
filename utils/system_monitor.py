import os
import psutil


class SystemMonitor:

    @staticmethod
    def memory_usage():

        process = psutil.Process(os.getpid())

        return process.memory_info().rss

    @staticmethod
    def format_size(size):
        units = ["Bytes", "KB", "MB", "GB", "TB"]

        value = float(size)

        for unit in units:

            if value < 1024:
                return f"{value:.2f} {unit}"

            value /= 1024

        return f"{value:.2f} PB"