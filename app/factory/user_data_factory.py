from app.models.user import User, UserRequest


class UserDataFactory:
    @staticmethod
    def to_user(user_request: UserRequest) -> User:
        user = User(
            name=user_request.name,
            email=user_request.email,
            password=user_request.password
        )
        return user
