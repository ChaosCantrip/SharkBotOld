from datetime import datetime, timedelta

timeFormat = "%d/%m/%Y-%H:%M:%S"


class Cooldown:

    def __init__(self, name: str, expiry: str, duration: timedelta) -> None:
        self.name = name
        self.expiry = datetime.strptime(expiry, timeFormat)
        self.duration = duration

    @property
    def expired(self) -> bool:
        return datetime.utcnow() > self.expiry

    def extend(self) -> None:
        self.expiry += self.duration

    def reset(self) -> None:
        self.expiry = datetime.utcnow() + self.duration

    @property
    def timestring(self) -> str:
        return datetime.strftime(self.expiry, timeFormat)

    @property
    def time_remaining(self) -> timedelta:
        return self.expiry - datetime.utcnow()

    @property
    def time_remaining_string(self) -> str:
        seconds = int(self.time_remaining.total_seconds())
        days, seconds = seconds // (24 * 60 * 60), seconds % (24 * 60 * 60)
        hours, seconds = seconds // (60 * 60), seconds % (60 * 60)
        minutes, seconds = seconds // 60, seconds % 60

        output_string = ""
        if days != 0:
            if days == 1:
                output_string += f"{days} day, "
            else:
                output_string += f"{days} days, "
        if hours != 0:
            if hours == 1:
                output_string += f"{hours} hour, "
            else:
                output_string += f"{hours} hours, "
        if minutes != 0:
            if minutes == 1:
                output_string += f"{minutes} minute, "
            else:
                output_string += f"{minutes} minutes, "
        if output_string == "":
            if seconds == 1:
                output_string += f"{seconds} second "
            else:
                output_string += f"{seconds} seconds "
        else:
            output_string = output_string[:-2] + f" and {seconds} "
            if seconds == 1:
                output_string += f"second "
            else:
                output_string += f"seconds "

        return output_string
