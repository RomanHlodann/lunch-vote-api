import os
import uuid

from django.db import models
from django.utils.text import slugify


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True
    )

    def __str__(self) -> str:
        return self.name


def menu_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.restaurant.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/menus/", filename)


class Menu(models.Model):
    image = models.ImageField(
        upload_to=menu_image_file_path,
        blank=True,
        null=True
    )
    description = models.CharField(max_length=255)
    date = models.DateField()
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="menus"
    )

    def __str__(self) -> str:
        return f"{self.description} from {self.restaurant.name}"
