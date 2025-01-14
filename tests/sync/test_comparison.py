import pytest
from sync.comparison import FieldChange, UserChangeDetail, UserComparer
from tcx_api.components.schemas.pbx import User, Group
from sync.sync_strategy import SyncSourceStrategy
from sync.logging import SyncLogger
from unittest.mock import MagicMock

class TestFieldChange:
    def test_field_change_initialization(self):
        old_value = "old_value"
        new_value = "new_value"
        field_change = FieldChange(old=old_value, new=new_value)
        
        assert field_change.old == old_value
        assert field_change.new == new_value


    class TestFieldChange:
        def test_field_change_initialization(self):
            old_value = "old_value"
            new_value = "new_value"
            field_change = FieldChange(old=old_value, new=new_value)
            
            assert field_change.old == old_value
            assert field_change.new == new_value


    class TestUserChangeDetail:
        def test_user_change_detail_initialization(self):
            field_changes = {
                "field1": FieldChange(old="old1", new="new1"),
                "field2": FieldChange(old="old2", new="new2")
            }
            user_to_update = User(Id=123, Number="456")
            user_change_detail = UserChangeDetail(field_changes=field_changes, user_to_update=user_to_update)
            
            assert user_change_detail.field_changes == field_changes
            assert user_change_detail.user_to_update == user_to_update

        def test_user_change_detail_id_property(self):
            user_to_update = User(Id=123, Number="456")
            user_change_detail = UserChangeDetail(field_changes={}, user_to_update=user_to_update)
            
            assert user_change_detail.Id == 123

        def test_user_change_detail_number_property(self):
            user_to_update = User(Id=123, Number="456")
            user_change_detail = UserChangeDetail(field_changes={}, user_to_update=user_to_update)
            
            assert user_change_detail.Number == "456"

        def test_user_change_detail_str_method(self):
            field_changes = {
                "field1": FieldChange(old="old1", new="new1"),
                "field2": FieldChange(old="old2", new="new2")
            }
            user_change_detail = UserChangeDetail(field_changes=field_changes)
            
            expected_str = "'field1' from 'old1' to 'new1', 'field2' from 'old2' to 'new2'"
            assert str(user_change_detail) == expected_str



    class TestUserComparer:
            class SyncSource(SyncSourceStrategy):
                @property
                def mapping(self):
                    return self._mapping
                
                @mapping.setter
                def mapping(self, value):
                    self._mapping = value

                def initialize(self):
                    return super().initialize()

                def get_source_users(self):
                    return [User(Id=1, Number="100", FirstName="New Name"), User(Id=2, Number="101", FirstName="Old Name")]

                def get_source_groups(self):
                    return [Group(Id=1, Name="Group 1"), Group(Id=2, Name="Group 2")]

                def get_user_update_fields(self):
                    return ["FirstName"]
            
            @pytest.fixture
            def custom_sync_source(self):
                mock_logger = MagicMock(spec=SyncLogger)
                yield self.SyncSource(mock_logger)
                

            def test_init(self, custom_sync_source):
                tcx_user_list = [User(Id=1, Number="100"), User(Id=2, Number="101")]
                comparer = UserComparer(tcx_user_list=tcx_user_list, sync_source=custom_sync_source)
                
                assert comparer.tcx_user_list == tcx_user_list
                assert comparer.sync_source == custom_sync_source

            def test__index_users(self,custom_sync_source):
                users = [User(Id=1, Number="100"), User(Id=2, Number="101")]
                comparer = UserComparer(tcx_user_list=users, sync_source=custom_sync_source)
                indexed_users = comparer._index_users(users)
                
                assert indexed_users == {"100": users[0], "101": users[1]}

            def test_get_user_change_details(self, custom_sync_source):
                tcx_user_list = [User(Id=1, Number="100", FirstName="Old Name"), User(Id=2, Number="101", FirstName="Old Name")]
                comparer = UserComparer(tcx_user_list=tcx_user_list, sync_source=custom_sync_source)
                user_change_details = comparer.get_user_change_details()
                
                assert len(user_change_details) == 1
                assert user_change_details[0].field_changes == {"FirstName": FieldChange(old="Old Name", new="New Name")}

            def test_compare_user(self, custom_sync_source):
                tcx_user_list = [User(Id=1, Number="100", FirstName="Old Name"), User(Id=2, Number="101", FirstName="Old Name")]
                comparer = UserComparer(tcx_user_list=tcx_user_list, sync_source=custom_sync_source)
                update_fields = ["FirstName"]
                source_user = custom_sync_source.get_source_users()[0]
                user_change_detail = comparer.compare_user(tcx_user_list[0], source_user, update_fields)
                
                assert user_change_detail.field_changes == {"FirstName": FieldChange(old="Old Name", new="New Name")}
                assert user_change_detail.user_to_update.FirstName == "New Name"

            def test_get_users_to_create(self, custom_sync_source):
                tcx_user_list = [User(Id=1, Number="100", FirstName="Old Name")]
                comparer = UserComparer(tcx_user_list=tcx_user_list, sync_source=custom_sync_source)
                users_to_create = comparer.get_users_to_create()
                
                assert len(users_to_create) == 1
                assert users_to_create[0].Number == "101"
