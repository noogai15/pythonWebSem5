import datetime

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models

fs = FileSystemStorage(location="/media/images")


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
    price = models.CharField(max_length=30, default="0€")

    age_rating = models.IntegerField(choices=AGE_RATINGS)
    creator = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    image = models.ImageField(
        upload_to="images",
        blank=True,
    )

    # image = models.FileField(
    # upload_to="images/",
    # blank=True,
    # )

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

    def get_upvotes(self):
        upvotes = Vote.objects.filter(up_or_down='U',
                                      game=self)
        return upvotes

    def get_upvotes_count(self):
        return len(self.get_upvotes())

    def get_downvotes(self):
        downvotes = Vote.objects.filter(up_or_down='D',
                                        game=self)
        return downvotes

    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def vote(self, user, up_or_down):
        U_or_D = 'U'
        if up_or_down == 'down':
            U_or_D = 'D'
        vote = Vote.objects.create(up_or_down=U_or_D,
                                   user=user,
                                   game=self
                                   )


    def __str__(self):
        return self.name

    def __repr__(self):
        return self.get_full_name() + " / " + self.creator + " / " + self.genre


class Comment(models.Model):
    text = models.TextField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, related_name="upvote")

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def get_comment_prefix(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

    def __str__(self):
        return self.get_comment_prefix() + ' (' + self.user.username + ')'

    def __repr__(self):
        return self.get_comment_prefix() + ' (' + self.user.username + ' / ' + str(self.timestamp) + ')'


class Vote(models.Model):
    VOTE_TYPES = [
        ('U', 'up'),
        ('D', 'down'),
    ]

    up_or_down = models.CharField(max_length=1,
                                  choices=VOTE_TYPES,
                                 )
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.up_or_down + ' on ' + self.book.title + ' by ' + self.user.username

    def getUserFromVote(self):
        return self.user