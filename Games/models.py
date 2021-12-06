import datetime
import math
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.conf import settings

fs = FileSystemStorage(location="/media/images")


# Create your models here.
class Game(models.Model):
    custom_permissions = [(
        ("can_edit_own_comment", "Can edit own comment"),
    )]
    GENRES = [
        ("HORROR", "Horror"),
        ("FPS", "First Person Shooter"),
        ("RTS", "Real-Time Strategy"),
        ("RPG", "Role-Playing Game"),
    ]
    AGE_RATINGS = [(0, "0+"), (6, "6+"), (12, "12+"), (16, "16+"), (18, "18+")]
    age_rating = models.IntegerField(choices=AGE_RATINGS)

    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=200)
    genre = models.CharField(max_length=10, choices=GENRES)
    price = models.CharField(max_length=30, default="0€")
    average_stars = models.IntegerField(default=0)

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

    myuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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

    def get_average_star_rating(self):
        return self.average_stars
        

    def get_desc_preview(self):
        if len(self.desc) < 25:
            return self.desc
        else:
            return self.desc[0:25] + "..."

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.get_full_name() + " / " + self.creator + " / " + self.genre


class Comment(models.Model):
    text = models.TextField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    

    STAR_RATINGS = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    star_rating = models.IntegerField(choices=STAR_RATINGS, default=0)

    reports = models.IntegerField(default=0)

    class Meta:
        ordering = ["timestamp"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def get_comment_prefix(self):
        if len(self.text) > 50:
            return self.text[:50] + "..."
        else:
            return self.text

    def get_upvotes(self):
        upvotes = Vote.objects.filter(up_or_down="U", comment=self)
        return upvotes

    def get_upvotes_count(self):
        return len(self.get_upvotes())

    def get_downvotes(self):
        downvotes = Vote.objects.filter(up_or_down="D", comment=self)
        return downvotes

    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def vote(self, myuser, game, U_or_D):
        vote = Vote.objects.create(
            up_or_down=U_or_D, myuser=myuser, game=game, comment=self
        )
    
    def report(self, reporter):
        Report.objects.create(reporter=reporter, comment=self, author=self.myuser, message=self.text)

    def reverse_vote(self, myuser, game, up_or_down):
        Vote.objects.filter(up_or_down=up_or_down, comment=self, myuser=myuser).delete()

    def __str__(self):
        return self.get_comment_prefix() + " (" + self.myuser.username + ")"

    def __repr__(self):
        return (
            self.get_comment_prefix()
            + " ("
            + self.myuser.username
            + " / "
            + str(self.timestamp)
            + ")"
        )


class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reporter")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="commenter")
    message = models.CharField(max_length=255)

    def __str__(self):
        return (self.author + ": " + self.message_content + ", reported by " + self.reporter)

    def __repr__(self):
        return (self.author + " " + self.message_content + " " + self.author)

class Vote(models.Model):
    VOTE_TYPES = [
        ("U", "up"),
        ("D", "down"),
    ]

    up_or_down = models.CharField(
        max_length=1,
        choices=VOTE_TYPES,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.up_or_down + " on " + self.book.title + " by " + self.myuser.username



class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def get_cart_price(self):
        return None


class OrderItem(models.Model):
    product = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def get_total(self):
        return None