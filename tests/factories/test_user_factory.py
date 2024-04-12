from sync.factories.user_entity_factory import UserEntityFactory
from tcx_api.components.schemas.pbx.enums import RuleHoursType
from tcx_api.components.schemas.pbx.schedule import Schedule


class TestUserFactory:
    def test_create_user_entity(self):
        user_data = {
            "Id": 1,
            "AuthID": "12345",
            "Enabled": True,
        }

        user = UserEntityFactory.create_user(**user_data)

        assert user.AuthID == user_data["AuthID"]
        assert user.Enabled == user_data["Enabled"]

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
