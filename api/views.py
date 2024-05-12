import uuid

from django.shortcuts import render, HttpResponse

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models
from rest_framework import serializers, exceptions

from ext.auth import BlogAuthentication, NoAuthentication


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
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True}
        }

    def nb_user(self, obj):
        return obj.user.username

class CommentView(APIView):
    authentication_classes = [BlogAuthentication]

    def get(self, request, blog_id):
        """ 评论列表 """
        # 1.获取评论对象
        queryset = models.Comment.objects.filter(blog_id=blog_id)

        # 2.序列化
        ser = CommentSerializers(instance=queryset, many=True)

        # 4.返回
        context = {"code": 1000, "data": ser.data}
        return Response(context)

    def post(self, request, blog_id):
        """ 发布评论 """
        # 判断是否用户登录
        if not request.user:
            return Response({"code": 3000, "error": "认证失败"})

        blog_object = models.Blog.objects.filter(id=blog_id).first()
        if not blog_object:
            return Response({"code": 2000, "error": "博客不存在"})

        ser = CommentSerializers(data=request.data)
        if not ser.is_valid():
            return Response({"code": 1002, "error": "验证失败","detail":ser.errors})

        ser.save(blog=blog_object, user=request.user)
        return Response({"code": 1000, "data": ser.data})

        # /api/comment/1/
        # {"content":"...."}
        # 保存



class RegisterSerializers(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["id", "username", "password", "confirm_password"]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True}
        }

    def validate_password(self, value):
        print("密码：", value)
        return value

    def validate_confirm_password(self, value):
        print(value)
        print(self.initial_data)
        password = self.initial_data.get("password")
        if password != value:
            raise exceptions.ValidationError("密码不一致")
        return value

# 用户注册
class RegisterView(APIView):

    def post(self, request):

        # 1.提交数据{"username":123123, "password":123123, "confirm_password":"xxx"}

        # 2.校验 + 保存
        ser = RegisterSerializers(data=request.data)
        if ser.is_valid():
            ser.validated_data.pop("confirm_password")
            ser.save()
            return Response({"code": 1000, "data": ser.data})
        else:
            return Response({"code": 1001, "error": "注册失败", "detail": ser.errors})

class LoginSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.UserInfo
        fields = ["username", "password"]


class LoginView(APIView):

    def post(self, request):
        # request.data  # {"username":"", "password":""}
        ser = LoginSerializers(data=request.data)
        if not ser.is_valid():
            return Response({"code": 1001, "error": "校验失败", "detail": ser.errors})

        instance = models.UserInfo.objects.filter(**ser.validated_data).first()
        if not instance:
            return Response({"code": 1002, "error": "用户名或密码错误"})

        token = str(uuid.uuid4())
        instance.token = token
        instance.save()

        return Response({"code": 1000, "token": token})


# # 创建评论
# class CreateComment(APIView):
#     def post(self):
#         pass
#

class FavorSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Favor
        fields = ["id",'blog']


class FavorView(APIView):
    # 查询评论是否存在 不存在添加 、 存在 不添加

    authentication_classes = [BlogAuthentication, NoAuthentication]

    def post(self, request):
        print(request.user)
        ser = FavorSerializers(data=request.data)
        if not ser.is_valid():
            return Response({"code": 1002, "error": "校验失败", "detail":ser.errors})

        # 1.存在，不再点赞
        exists = models.Favor.objects.filter(user=request.user, **ser.validated_data).exists()
        if exists:
            return Response({"code": 1005, "error": "已存在"})

        # 2.不存在， 点赞
        ser.save(user=request.user)
        return Response({"code": 1000, "data": ser.data})
