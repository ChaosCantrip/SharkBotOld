from datetime import datetime, timedelta

timeFormat = "%Y/%m/%d-%H:%M:%S"


class Cooldown:

    def __init__(self, name: str, expiry: str, duration: timedelta) -> None:
        self.name = name
        self.expiry = datetime.strptime(expiry, timeFormat)
        self.duration = duration

    @property
    def expired(self) -> bool:
        return datetime.now() > self.expiry

    def extend(self) -> None:
        self.expiry += self.duration

    def reset(self) -> None:
        self.expiry = datetime.now() + self.duration

    @property
    def timestring(self) -> str:
        return datetime.strftime(self.expiry, timeFormat)

    @property
    def timeremaining(self) -> timedelta:
        return self.expiry - datetime.now()

    @property
    def timeremainingstr(self) -> str:
        seconds = int(self.timeremaining.total_seconds())
        days, seconds = seconds // (24 * 60 * 60), seconds % (24 * 60 * 60)
        hours, seconds = seconds // (60 * 60), seconds % (60 * 60)
        minutes, seconds = seconds // 60, seconds % 60

        outputString = ""
        if days != 0:
            if days == 1:
                outputString += f"{days} day, "
            else:
                outputString += f"{days} days, "
        if hours != 0:
            if hours == 1:
                outputString += f"{hours} hour, "
            else:
                outputString += f"{hours} hours, "
        if minutes != 0:
            if minutes == 1:
                outputString += f"{minutes} minute, "
            else:
                outputString += f"{minutes} minutes, "
        if outputString == "":
            if seconds == 1:
                outputString += f"{seconds} second "
            else:
                outputString += f"{seconds} seconds "
        else:
            outputString = outputString[:-2] + f" and {seconds} "
            if seconds == 1:
                outputString += f"second "
            else:
                outputString += f"seconds "

        return outputString




class NewCooldown(Cooldown):

    def __init__(self, name: str, duration: timedelta) -> None:
        self.name = name
        self.expiry = datetime.now()
        self.duration = duration
