import ast
from datetime import datetime, timedelta
from pytz import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count
from postings.models import Posting
from archives.models import Constituent, FlavorTag

class_mapping = {
    "Constituent": Constituent,
    "FlavorTag": FlavorTag,
}


class Intro:
    """인트로 페이지"""

    def get_popularity_postings(*, offset: int, step=8):
        # ? 관계형 필드로 정렬할때 .all().annotate를 사용하지 않으면 이상한 결과가 나오더라
        return Posting.objects.all().annotate(likes=Count("posting_likes")).order_by("-likes")[offset : offset + step]

    def get_latest_postings(*, offset: int, step=8):
        return Posting.objects.order_by("-created")[offset : offset + step]

    def search(word):
        (word,) = word
        results = {
            "cocktail_name": Posting.objects.filter(cocktail_name__iregex=rf"{word}"),
            "created_by": Posting.objects.filter(created_by__username__iregex=rf"{word}"),
            "content": Posting.objects.filter(content__iregex=rf"{word}"),
            "constituents": Posting.objects.filter(constituents__name__iregex=rf"{word}"),
            "flavor_tags": Posting.objects.filter(flavor_tags__expression__iregex=rf"{word}"),
        }

        return "page/search-result/main.html", {key: set(value) for key, value in results.items() if value}

    def tag_search(data_list):
        """data는 posting이다"""
        data_ground = []
        for data in data_list:
            data = ast.literal_eval(data)
            current_obj = class_mapping[data["class"]].objects.get(pk=data["pk"])
            data_ground.extend(current_obj.postings.all())

        # ? 태그 참조 갯수로 포스팅들을 분류, 정렬하는 로직입니다.
        organized = [{"data": data, "count": data_ground.count(data)} for data in set(data_ground)]
        organized.sort(key=lambda x: x["count"], reverse=True)
        mex_ref = organized[0]["count"]
        content = [(count, []) for count in range(mex_ref, 0, -1)]
        for info in organized:
            container = [i[1] for i in content if i[0] == info["count"]][0]
            container.append(info["data"])
        return "page/tagsearch-result/main.html", content

    func_mapping = {
        "search": search,
        "tag_search": tag_search,
    }

    @classmethod
    def main(cls, request):
        """
        html에 DOM을 뿌린 후 JavaScript에서 가져가도록 합니다.

        JavaScript가 두 클래스를 동시에 뿌릴 수 있도록 zip을 써서 데이터를 가공함
        즉, 앞단에서는 포스팅 갯수 많은 순서대로 constituent,flavorTag가 순서대로 뿌려짐
        """

        # 포스팅에 많이 사용된 태그가 앞에 오도록 정렬
        # ? annotate를 사용해서 reference_count 피쳐를 만든 뒤, order_by에서 해당 피쳐를 사용해 정렬하는 코드입니다.
        organize = lambda model: model.objects.all().annotate(reference_count=Count("postings")).order_by("-reference_count")
        tags = []

        for constituent in organize(Constituent):
            tags.append(
                {
                    "content": constituent.name.replace("\n", ""),
                    "class": "Constituent",
                    "type": constituent.kind,
                    "alcohol": True if (v := constituent.alcohol) and v > 0 else False,
                    "pk": constituent.pk,
                }
            )
        for flavor_tag in organize(FlavorTag):
            tags.append(
                {
                    "content": flavor_tag.expression.replace("\n", ""),
                    "class": "FlavorTag",
                    "type": flavor_tag.category,
                    "alcohol": False,
                    "pk": flavor_tag.pk,
                }
            )

        return render(
            request,
            "page/intro/main.html",
            {
                "tags": tags,
                "popularity_postings": cls.get_popularity_postings(offset=0),
                "latest_postings": cls.get_latest_postings(offset=0),
            },
        )

    @classmethod
    def search_progress(cls, request):

        content = dict(request.POST)
        if tag_list := content.get("tag", False):
            content["classifier"] = ["tag_search"]
            content["search_for"] = tag_list

        # func_mapping에 명시된 함수에 content["search_for"] 리스트를 준다.
        html, result = cls.func_mapping[content["classifier"][0]](content["search_for"])
        # max_ref는 tag_search에서만 사용되는 값

        return render(request, html, {"content": result})
