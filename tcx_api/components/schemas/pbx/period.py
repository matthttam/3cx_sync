from tcx_api.components.schemas.pbx.enums import DayOfWeek


class Period:
    def __init__(
        self, DayOfWeek: DayOfWeek = None, Start: str = None, Stop: str = None
    ) -> None:
        self.DayOfWeek = DayOfWeek
        self.Start = Start
        self.Stop = Stop
