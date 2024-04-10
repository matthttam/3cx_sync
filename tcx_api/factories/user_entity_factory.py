from tcx_api.components.schemas.pbx.user import User


class UserEntityFactory:
    @staticmethod
    def create_user(**kwargs):
        return User(**kwargs)
