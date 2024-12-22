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
        include_tax_free,
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
        hourly_rate_short = short_day_fee / short_day_hours if short_day_hours else 0
        adjusted_cost = paid_hours * (
            hourly_rate_full if total_monthly_hours > 0 else hourly_rate_short
        )

        if include_tax_free:
            # Calculate the top-up amount
            top_up_amount = (adjusted_cost / 8) * 2
            # Ensure the top-up does not exceed the maximum allowed per month
            max_monthly_top_up = 500 / 3
            top_up_amount = min(top_up_amount, max_monthly_top_up)
            adjusted_cost = max(adjusted_cost - top_up_amount, 0)

        return adjusted_cost

    @staticmethod
    def parse_time_range(
        time_range, default_full="8am-6pm", default_short="9am-5pm", is_full_day=True
    ):
        default = default_full if is_full_day else default_short
        if not time_range:
            time_range = default
        try:
            start_time, end_time = time_range.split("-")
            try:
                start_time = datetime.strptime(start_time.strip(), "%I:%M%p")
            except ValueError:
                start_time = datetime.strptime(start_time.strip(), "%I%p")
            try:
                end_time = datetime.strptime(end_time.strip(), "%I:%M%p")
            except ValueError:
                end_time = datetime.strptime(end_time.strip(), "%I%p")
            duration = (end_time - start_time).seconds / 3600
            return duration
        except Exception as e:
            raise ValueError(
                f"Invalid time range format: {time_range}. Expected format: '8am-6pm' or '9am-5pm'. {e}"
            )
