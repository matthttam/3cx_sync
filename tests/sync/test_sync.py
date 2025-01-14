import pytest
from unittest.mock import MagicMock, patch
from sync.sync import Sync, run_sync
from sync.logging import SyncLogger, LogLevel
from sync.sync_strategy import SyncSourceStrategy
from tcx_api.resources.users import UsersResource
from tcx_api.resources.groups import GroupsResource
from sync.comparison import UserChangeDetail
from tcx_api.components.schemas.pbx import User


@pytest.fixture
def mock_logger():
    return MagicMock(spec=SyncLogger)


@pytest.fixture
def mock_sync_source():
    return MagicMock(spec=SyncSourceStrategy)


@pytest.fixture
def sync_instance(mock_logger, mock_sync_source):
    return Sync(logger=mock_logger, sync_source=mock_sync_source)


class TestSync:

    def test_sync_initialization(self, sync_instance, mock_logger):
        sync_instance.sync()
        mock_logger.log.assert_any_call(LogLevel.INFO, "Initializing Sync")

    @patch('sync.sync.AppConfig')
    @patch('sync.sync.TCX_API_Connection')
    def test_sync_authentication(self, mock_api_connection, mock_app_config, sync_instance, mock_logger):
        mock_app_config.return_value.server_url = "http://testserver"
        sync_instance.sync()
        mock_logger.log.assert_any_call(LogLevel.INFO, "Authenticating to 3CX at http://testserver")

    @patch('sync.sync.UsersResource')
    @patch('sync.sync.GroupsResource')
    def test_get_users(self, mock_users_resource_class, mock_groups_resource_class, sync_instance, mock_logger):
        mock_users_resource = MagicMock(spec=UsersResource)
        mock_users_resource_class.return_value = mock_users_resource

        mock_groups_resource = MagicMock(spec=GroupsResource)
        mock_groups_resource_class.return_value = mock_groups_resource

        mock_users_resource.return_value.list_user.return_value = [MagicMock(spec=User)]
        users = sync_instance.get_users()
        assert len(users) == 1
        mock_logger.log.assert_any_call(LogLevel.INFO, "Fetched 1 Users From 3CX")

    def test_create_user(self, sync_instance, mock_logger):
        mock_user = MagicMock(spec=User)
        mock_user.Number = "123"
        sync_instance.user_resource = MagicMock(spec=UsersResource)
        sync_instance.group_resource = MagicMock(spec=GroupsResource)
        sync_instance.create_user(mock_user)
        mock_logger.log.assert_any_call(LogLevel.INFO, "Creating 3CX user 123")

    def test_update_user(self, sync_instance, mock_logger):
        mock_user_change_detail = MagicMock(spec=UserChangeDetail)
        mock_user_change_detail.Number = "123"
        sync_instance.user_resource = MagicMock(spec=UsersResource)
        sync_instance.update_user(mock_user_change_detail)
        mock_logger.log.assert_any_call(LogLevel.INFO, "Updating 3CX user 123")

    def test_handle_logout_hotdesk_on_disable(self, sync_instance, mock_logger):
        mock_user_change_detail = MagicMock(spec=UserChangeDetail)
        mock_user_change_detail.field_changes = {"Enabled": MagicMock(new=False)}
        mock_user_change_detail.Number = "123"
        sync_instance.user_resource = MagicMock(spec=UsersResource)
        sync_instance.log_user_out_of_assigned_hotdesks_by_number = MagicMock()
        sync_instance.handle_logout_hotdesk_on_disable(mock_user_change_detail)
        sync_instance.log_user_out_of_assigned_hotdesks_by_number.assert_called_with("123")

    def test_run_sync(self, mock_logger, mock_sync_source):
        with patch('sync.sync.Sync') as mock_sync:
            run_sync(mock_logger, mock_sync_source)
            mock_sync.assert_called_once()
            mock_sync.return_value.sync.assert_called_once()