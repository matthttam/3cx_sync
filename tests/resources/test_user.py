from tcx_api.resources.user import UserFactory
from tcx_api.resources.user import BreakTime

import pytest


class TestUserFactory:
    def test_create_user_entity(self):
        user_data = {
            "AuthID": "12345",
            "Enabled": True,
        }

        user = UserFactory.create_user(**user_data)

        assert user.AuthID == user_data["AuthID"]
        assert user.Enabled == user_data["Enabled"]

    def test_create_user_entity_breaktime(self):
        user_data = {"AuthID": "12345", "Enabled": True, "BreakTime": {}}

        user = UserFactory.create_user(**user_data)

        assert user.AuthID == user_data["AuthID"]
        assert user.Enabled == user_data["Enabled"]
        assert isinstance(user.BreakTime, BreakTime)

    def test_create_user_invalid_property(self):
        # Test data with an invalid property
        user_data = {
            "AuthID": "12345",
            "Enabled": True,
            "invalid_property": "value",  # Adding an invalid property
        }

        # Ensure that creating a user with an invalid property raises an exception
        with pytest.raises(ValueError):
            UserFactory.create_user(**user_data)


if __name__ == "__main__":
    pytest.main()
