from typing import Final


class HoursGrid:
    def __init__(self, *, step: int = 2) -> None:
        self.hours1: Final[list[int]] = [h for h in range(10, 18, step)]
        self.hours2: Final[list[int]] = [h for h in range(8, 18, step)]
        self.hours3: Final[list[int]] = [h for h in range(8, 22, step)]
        self.hours4: Final[list[int]] = self.hours1 * 2
        self.hours5: Final[list[int]] = self.hours2 * 2
        self.hours6: Final[list[int]] = self.hours3 * 2
        self.hours7: Final[list[int]] = [h for h in range(8, 22)] * 3

    def sort_events(self, enumber: int) -> list[int]:
        hours: list[int] = []
        for hrs in (
            self.hours1,
            self.hours2,
            self.hours3,
            self.hours4,
            self.hours5,
            self.hours6,
            self.hours7,
        ):
            if len(hours) <= enumber:
                hours = hrs
                break
        else:
            assert False, f"too many events ({enumber}) for single date"

        return [hours[i] for i in range(enumber)]
