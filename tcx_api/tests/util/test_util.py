from sync.factories.user_entity_factory import UserEntityFactory
from tcx_api.components.schemas.pbx.schedule import Schedule
from tcx_api.components.schemas.pbx.enums import RuleHoursType
import pytest
from tcx_api.util import TcxStrEnum, TcxStrEnumMeta
from enum import auto, StrEnum


class TestTcxStrEnum:
    def test_tcxstrenum_inherits_strenum(self):
        assert issubclass(TcxStrEnum, StrEnum)

    def test_tcxstream_metaclass_is_tcxstrenummeta(self):
        assert type(TcxStrEnum) == TcxStrEnumMeta

    def test_tcxstrenum_sets_none(self):
        class test_enum(TcxStrEnum):
            NONE = auto()
            a = auto()
            b = auto()

        assert test_enum["NONE"] == "None"
        assert test_enum["None"] == "None"

    def test_create_user_entity_breaktime(self):
        user_data = {
            "Id": 1,
            "AuthID": "12345",
            "Enabled": True,
            "BreakTime": {"Type": RuleHoursType.BreakTime},
        }

        user = UserEntityFactory.create_user(**user_data)

        assert user.AuthID == user_data["AuthID"]
        assert user.Enabled == user_data["Enabled"]
        assert isinstance(user.BreakTime, Schedule)


if __name__ == "__main__":
    pytest.main()
