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


if __name__ == "__main__":
    pytest.main()
