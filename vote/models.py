from django.db import models
from django.conf import settings

from restaurant.models import Menu


class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="votes"
    )
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "menu", "created_at"],
                name="unique_vote"
            ),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.menu}"
