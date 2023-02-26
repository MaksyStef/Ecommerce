from django.contrib.auth.base_user import BaseUserManager


# Create your managers here
class AccountManager(BaseUserManager):
    """
    Custom user model manager with ability to create users with Favourite and Cart fields
    """

    def create_user(self, username, email, password=None, **extra_fields):
        """ Create user with unique favourite and cart """
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, username, email, password, **extra_fields):
        """ Create user with unique favourite and cart """
        user = self.create_user(username=username, email=email, password=password, **extra_fields)
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """ Create user with unique favourite and cart """
        user = self.create_staffuser(username=username, email=email, password=password, **extra_fields)
        user.is_superuser = True
        user.save()
        return user
