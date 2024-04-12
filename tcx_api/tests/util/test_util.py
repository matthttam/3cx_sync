from sync.factories.user_entity_factory import UserEntityFactory
from tcx_api.components.schemas.pbx.schedule import Schedule
from tcx_api.components.schemas.pbx.enums import RuleHoursType
import pytest
from tcx_api.util import TcxStrEnum, TcxStrEnumMeta
from enum import auto, StrEnum
from tcx_api.util import Util


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


class TestUtil:
    def test_instanciate_object(self):
        class test_object:
            def __init__(self, a) -> None:
                self.a = a

        return_object = Util.instanciate_object(test_object(a="test"), test_object)
        return_object_from_dict = Util.instanciate_object({"a": "test"}, test_object)
        return_none = Util.instanciate_object(None, test_object)

        assert isinstance(return_object, test_object)
        assert isinstance(return_object_from_dict, test_object)
        assert return_none is None

    def test_instanciate_list_of_objects(self):
        class test_object:
            def __init__(self, a) -> None:
                self.a = a

        test_list_of_objects = [test_object(a="test"), test_object(a="test2")]
        test_list_of_dicts = [{"a": "test"}, {"a": "test2"}]

        return_list_of_objects = Util.instanciate_list_of_objects(
            test_list_of_objects, test_object
        )
        return_list_of_objects_from_list_of_dicts = Util.instanciate_list_of_objects(
            test_list_of_dicts, test_object
        )
        return_empty_list = Util.instanciate_list_of_objects(None, test_object)

        assert isinstance(return_list_of_objects, list)
        assert all(isinstance(v, test_object) for v in return_list_of_objects)
        assert isinstance(return_list_of_objects_from_list_of_dicts, list)
        assert all(
            isinstance(v, test_object)
            for v in return_list_of_objects_from_list_of_dicts
        )

        assert isinstance(return_empty_list, list)
        assert return_empty_list == []

    def test_instanciate_str_enum(self):
        class test_enum(TcxStrEnum):
            NONE = auto()
            a = auto()

        return_str_from_str = Util.instanciate_str_enum("a", test_enum)
        return_str_from_enum_value = Util.instanciate_str_enum(test_enum.a, test_enum)
        return_none = Util.instanciate_str_enum(None, test_enum)

        assert isinstance(return_str_from_str, str)
        assert isinstance(return_str_from_enum_value, str)
        assert return_none is None

        with pytest.raises(KeyError):
            Util.instanciate_str_enum("invalid_value", test_enum)

    def test_instanciate_list_of_str_enum(self):
        class test_enum(TcxStrEnum):
            NONE = auto()
            a = auto()
            b = auto()

        return_list_from_list_of_str = Util.instanciate_list_of_str_enum(
            ["a", "b"], test_enum
        )
        return_list_from_list_of_enum = Util.instanciate_list_of_str_enum(
            [test_enum.a, test_enum.b], test_enum
        )
        return_empty_list = Util.instanciate_list_of_str_enum(None, test_enum)

        assert isinstance(return_list_from_list_of_str, list)
        assert all(isinstance(v, str) for v in return_list_from_list_of_str)
        assert isinstance(return_list_from_list_of_enum, list)
        assert all(isinstance(v, str) for v in return_list_from_list_of_enum)
        assert return_empty_list == list()

        with pytest.raises(KeyError):
            Util.instanciate_list_of_str_enum(["a", "invalid_value"], test_enum)


if __name__ == "__main__":
    pytest.main()
