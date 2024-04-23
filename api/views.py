from django.shortcuts import render, HttpResponse

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models
from rest_framework import serializers


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

class BlogSerializers(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_display")
    ctime = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = models.Blog
        fields = ["category", "image", "title", "summary", "ctime", "comment_count", "favor_count", "creator"]

class BlogView(APIView):
    def get(self, reqest, *args, **kwargs):
        """ 获取博客列表 """

        # 1.读取数据库中的博客信息
        queryset = models.Blog.objects.all().order_by("-id")

        # 2.序列化
        ser = BlogSerializers(instance=queryset, many=True)

        # 3.返回
        return Response(ser.data)
