from django.contrib import admin
from django.utils.html import mark_safe
from . import models


class PictureInline(admin.StackedInline):
    """ 다른 Admin에 사진 모델을 같이 볼 수 있도록 만들어둔 클래스 """

    model = models.Picture


class CommentInline(admin.StackedInline):

    model = models.Comment


class LikeInline(admin.StackedInline):

    model = models.Like


class ReplyInline(admin.StackedInline):

    model = models.Reply


@admin.register(models.Posting)
class PostingAdmin(admin.ModelAdmin):
    """ 포스팅 Admin 정의 """

    list_per_page = 10

    list_display = (
        "cocktail_name",
        "alchol",
        "created_by",
        "get_image",
        "created",
    )
    ordering = ("-created",)

    raw_id_fields = ("created_by",)
    search_fields = (
        "cocktail_name",
        "created_by__username",
        "constituents__name",
        "flavor_tags__expression",
        "flavor_tags__category",
    )
    filter_horizontal = (
        "constituents",
        "flavor_tags",
    )

    inlines = (PictureInline, LikeInline, CommentInline)

    def get_image(self, obj):
        """ info: obj 인자로는 Posting객체가 들어온다 """

        return mark_safe(f'<img width="50px" src="{obj.pictures.all()[0].image.url}" />')

    get_image.short_description = "Picture"


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    list_per_page = 50

    list_display = (
        "created_by",
        "content",
        "reply_counter",
        "posting",
        "get_image",
        "score",
        "created",
    )
    search_fields = (
        "posting__cocktail_name",
        "created_by__username",
        "score",
        "content",
    )
    list_filter = ("score",)

    ordering = ("-created",)
    raw_id_fields = ("created_by",)

    inlines = (ReplyInline,)

    def get_image(self, obj):
        """ info: obj 인자로는 Comment객체가 들어온다 """
        if obj.photo:
            return mark_safe(f'<img width="50px" src="{obj.photo.url}" />')

    def reply_counter(self, obj):
        return obj.replies.all().count()

    reply_counter.short_description = "replies"

    get_image.short_description = "Comment Image"
