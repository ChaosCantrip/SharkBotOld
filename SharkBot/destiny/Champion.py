class Champion:

    def __init__(self, name: str, icon: str):
        self.name = name
        self.icon = icon

    @property
    def text(self) -> str:
        return f"{self.icon} {self.name}"


champions = [
    Champion(
        name="Barrier",
        icon="(Barrier Icon)"
    ),
    Champion(
        name="Overload",
        icon="(Overload Icon)"
    ),
    Champion(
        name="Unstoppable",
        icon="(Unstoppable Icon)"
    )
]
