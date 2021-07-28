from numpy import average
from django.db import models
from core.models import CoreModel


class Posting(CoreModel):
    """ 포스팅 모델입니다. """

    related_name = "postings"

    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name=related_name)
    cocktail_name = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    constituents = models.ManyToManyField("archives.Constituent", related_name=related_name)
    flavor_tags = models.ManyToManyField("archives.FlavorTag", related_name=related_name)

    def alchol(self):
        alcoholics = self.constituents.exclude(alcohol=None)
        return round(average(tuple(obj.alcohol for obj in alcoholics)), 2)

    def __str__(self):
        return f"{self.created_by} - {self.cocktail_name}"


class Picture(CoreModel):
    """ 포스팅에 담기는 사진을 다루는 모델입니다. """

    related_name = "pictures"

    image = models.ImageField(upload_to="postings", null=True, blank=True)
    posting = models.ForeignKey("postings.Posting", on_delete=models.CASCADE, related_name=related_name)

    def __str__(self):
        return f"[포스팅 사진] {self.posting}"


class Comment(CoreModel):
    """ 포스팅에 달리는 Comment 모델입니다. """

    related_name = "comments"

    posting = models.ForeignKey("postings.Posting", on_delete=models.CASCADE, related_name=related_name)
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name=related_name)
    photo = models.ImageField(upload_to="comment_images", null=True, blank=True)
    score = models.SmallIntegerField(null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.created_by}: {self.content[:25]}{'...' if len(self.content) > 10 else ''}"


class Reply(CoreModel):
    """ Comment 에달리는 Reply 모델입니다. """

    related_name = "replies"

    comment = models.ForeignKey("postings.Comment", on_delete=models.CASCADE, related_name=related_name)
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name=related_name)
    photo = models.ImageField(upload_to="comment_images", null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return f"[Reply to {self.comment.created_by}]{self.created_by}: {self.content[:25]}{'...' if len(self.content) > 10 else ''}"


class Like(CoreModel):
    """ 포스팅에 달리는 좋아요 모델입니다. """

    related_name = "likes"

    posting = models.ForeignKey("postings.Posting", on_delete=models.CASCADE, related_name=related_name)
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name=related_name)

    def __str__(self):
        return f"{self.created_by} -> [{self.posting}]"
