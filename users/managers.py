from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise ValueError("Email це обов'язкове поле для заповнення")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password
        )

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
