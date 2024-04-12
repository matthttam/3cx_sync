from tcx_api.components.schemas.pbx.user import User
from app.mapping import CSVMapping


class UserEntityFactory:
    @staticmethod
    def create_user(**kwargs):
        return User(**kwargs)

    @staticmethod
    def create_user_with_csv_mapping(csv_mapping: CSVMapping, csv_data):
        # map the csv data using the csv_mapping file and return an initialized user
        pass
