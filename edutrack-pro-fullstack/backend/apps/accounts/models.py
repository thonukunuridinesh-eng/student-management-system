from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.text import slugify


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _generate_username(self, email):
        base_username = slugify(email.split("@")[0])[:140] or "user"
        username = base_username
        counter = 1

        while self.model.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        return username

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address is required.")

        email = self.normalize_email(email)
        extra_fields.setdefault("username", self._generate_username(email))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", User.Role.ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    username = models.CharField(max_length=150, unique=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["first_name", "last_name", "email"]

    def save(self, *args, **kwargs):
        if not self.username and self.email:
            base_username = slugify(self.email.split("@")[0])[:140] or "user"
            username = base_username
            counter = 1

            while User.objects.exclude(pk=self.pk).filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            self.username = username

        super().save(*args, **kwargs)

    @property
    def full_name(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name or self.email

    def __str__(self):
        return f"{self.full_name} ({self.role})"
