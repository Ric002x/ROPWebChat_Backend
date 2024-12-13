from django.contrib.auth.hashers import check_password, make_password

from users.models import User


class Authentication:
    def signin(self, email: str, password: str) -> User | bool:
        user = User.objects.filter(email=email).first()

        if user and check_password(password, user.password):
            return user

        return False

    def signup(self, email: str, name: str, password: str) -> User | bool:
        if User.objects.filter(email=email).exists():
            return False

        user = User.objects.create(
            email=email,
            name=name,
            password=make_password(password)
        )

        return user
