from django.shortcuts import render, HttpResponse

# Create your views here.
from api import models


def db(request):

    v1 = models.UserInfo.objects.create(username="admin", password="123")
    v2 = models.UserInfo.objects.create(username="x1", password="123")

    models.Blog.objects.create(
        category=1,
        image="xxx/xxx.png",
        title="x经理",
        summary=".....",
        text="xxxxxxxxxx",
        creator=v1
    )

    models.Blog.objects.create(
        category=2,
        image="xxx/xxx.png",
        title="a经理",
        summary=".....cccccc",
        text="xxxxxxxxxxdddddddddd",
        creator=v2
    )

    return HttpResponse("成功")


class BlogView:
    pass