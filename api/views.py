from django.shortcuts import render, HttpResponse

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models
from rest_framework import serializers


def db(request):

    # v1 = models.UserInfo.objects.create(username="admin", password="123")
    # v2 = models.UserInfo.objects.create(username="x1", password="123")
    #
    # models.Blog.objects.create(
    #     category=1,
    #     image="xxx/xxx.png",
    #     title="x经理",
    #     summary=".....",
    #     text="xxxxxxxxxx",
    #     creator=v1
    # )
    #
    # models.Blog.objects.create(
    #     category=2,
    #     image="xxx/xxx.png",
    #     title="a经理",
    #     summary=".....cccccc",
    #     text="xxxxxxxxxxdddddddddd",
    #     creator=v2
    # )

    # 添加评论
    # models.Comment.objects.create(content='x1',blog_id=1,user_id=1)
    # models.Comment.objects.create(content='x222',blog_id=1,user_id=2)

    return HttpResponse("成功")

class BlogUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ["id", "username"]

class BlogSerializers(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_display")
    ctime = serializers.DateTimeField(format="%Y-%m-%d")
    # creator_name = serializers.CharField(source="creator.username")
    # creator = serializers.SerializerMethodField()
    creator = BlogUserSerializers()

    class Meta:
        model = models.Blog
        fields = ["category", "image", "title", "summary", "ctime", "comment_count", "favor_count", "creator"]

    # 钩子函数
    # def get_creator(self, obj):
    #     return {"id": obj.creator_id, "name": obj.creator.username}

class BlogView(APIView):
    def get(self, reqest, *args, **kwargs):
        """ 获取博客列表 """

        # 1.读取数据库中的博客信息
        queryset = models.Blog.objects.all().order_by("-id")

        # 2.序列化
        ser = BlogSerializers(instance=queryset, many=True)

        # 3.返回
        context = {"code":1000, "data":ser.data}
        return Response(context)

class BlogDetailSerializers(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_display")
    ctime = serializers.DateTimeField(format="%Y-%m-%d")
    creator = BlogUserSerializers()

    class Meta:
        model = models.Blog
        fields = "__all__"


class BlogDetailView(APIView):
    def get(self, reqest, *args, **kwargs):
        """ 获取博客列表 """

        # 1.获取ID
        pk = kwargs.get("pk")

        # 2.根据ID获取对象
        instance = models.Blog.objects.filter(id=pk).first()
        if not instance:
            return Response({"code": 1001, "error": "不存在"})

        # 3.序列化
        ser = BlogSerializers(instance=instance, many=False)

        # 4.返回
        context = {"code": 1000, "data": ser.data}
        return Response(context)

from ext.hook import NbHookSerializer
class CommentSerializers(NbHookSerializer,serializers.ModelSerializer):
    # user = serializers.CharField(source="user.username")
    class Meta:
        model = models.Comment
        fields = ["id", "content", "user"]

    def nb_user(self, obj):
        return obj.user.username

class CommentView(APIView):
    def get(self, request, blog_id):
        """ 评论列表 """
        # 1.获取评论对象
        queryset = models.Comment.objects.filter(blog_id=blog_id)

        # 2.序列化
        ser = CommentSerializers(instance=queryset, many=True)

        # 4.返回
        context = {"code": 1000, "data": ser.data}
        return Response(context)
