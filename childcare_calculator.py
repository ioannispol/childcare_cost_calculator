from calendar import monthrange
from datetime import datetime


class ChildCareCalculator:
    def calculate_monthly_cost(
        self,
        full_day_fee,
        short_day_fee,
        full_day_hours,
        short_day_hours,
        government_free_hours_per_week,
        weekly_schedule,
        year,
        month,
    ):
        days_in_month = monthrange(year, month)[1]
        total_monthly_cost = 0
        total_monthly_hours = 0

        for day in range(1, days_in_month + 1):
            weekday = (day - 1) % 7
            if weekday in weekly_schedule:
                if weekly_schedule[weekday] == "full":
                    total_monthly_cost += full_day_fee
                    total_monthly_hours += full_day_hours
                elif weekly_schedule[weekday] == "short":
                    total_monthly_cost += short_day_fee
                    total_monthly_hours += short_day_hours

        free_hours_per_month = government_free_hours_per_week * 4.33
        paid_hours = max(total_monthly_hours - free_hours_per_month, 0)

        hourly_rate_full = full_day_fee / full_day_hours
        hourly_rate_short = short_day_fee / short_day_hours
        adjusted_cost = paid_hours * (
            hourly_rate_full if total_monthly_hours > 0 else hourly_rate_short
        )

        return adjusted_cost

    @staticmethod
    def parse_time_range(time_range, default):
        if not time_range:
            return default
        try:
            start_time, end_time = time_range.split("-")
            start_time = datetime.strptime(start_time.strip(), "%I%p")
            end_time = datetime.strptime(end_time.strip(), "%I%p")
            duration = (end_time - start_time).seconds / 3600
            return duration
        except Exception as e:
            raise ValueError(
                f"Invalid time range format: {time_range}. Expected format: '8am-6pm'. {e}"
            )
