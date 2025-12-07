from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, ):
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
        except (UserModel.DoesNotExist, UserModel.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
