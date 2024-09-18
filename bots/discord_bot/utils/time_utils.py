from datetime import datetime, timedelta
import pytz

class TimeUtils:
    def __init__(self):
        self.brt_timezone = pytz.timezone('America/Sao_Paulo')

    def is_weekday(self) -> bool:
        today = datetime.now(self.brt_timezone)
        return today.weekday() < 5  # Monday is 0, Sunday is 6

    def is_between_hours(self, start_hour: int = 0, end_hour: int = 23) -> bool:
        now = datetime.now(self.brt_timezone)
        current_hour = now.hour
        
        return start_hour <= current_hour < end_hour

    def is_valid_time(self) -> bool:
        return self.is_weekday() and self.is_between_hours()
