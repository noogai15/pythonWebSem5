import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Game(models.Model):
    GENRES = [
        ("HORROR", "Horror"),
        ("FPS", "First Person Shooter"),
        ("RTS", "Real-Time Strategy"),
        ("RPG", "Role-Playing Game"),
    ]
    AGE_RATINGS = [(0, "0+"), (6, "6+"), (12, "12+"), (16, "16+"), (18, "18+")]

    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=200)
    genre = models.CharField(max_length=10, choices=GENRES)

    age_rating = models.IntegerField(choices=AGE_RATINGS)
    creator = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="users",
        related_query_name="user",
    )

    class Meta:
        ordering = ["name", "-genre"]
        verbose_name = "Game"
        verbose_name_plural = "Game"

    def get_age_rating(self):
        return self.age_rating.display()

    def get_desc_preview(self):
        if len(self.desc) < 25:
            return self.desc
        else:
            return self.desc[0:25] + "..."

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.get_full_name() + " / " + self.creator + " / " + self.genre
