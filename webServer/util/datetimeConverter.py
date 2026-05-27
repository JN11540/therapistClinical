import time as time


class datetimeConverter:
    @staticmethod
    def get_current_timestamp() -> int:
        return int(time.time())