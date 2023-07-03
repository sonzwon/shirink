from django.contrib.auth.models import User
from shortener.models import Users, ShortenedUrls, QrCode
from rest_framework import serializers
from shortener.utils import url_count_changer, create_qr


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class UserSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer(read_only=True)

    class Meta:
        model = Users
        fields = ["id", "url_count", "organization", "user"]


class UrlListSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = ShortenedUrls
        fields = "__all__"


class UrlCreateSerializer(serializers.Serializer):
    nick_name = serializers.CharField(max_length=50)
    target_url = serializers.CharField(max_length=2000)
    category = serializers.IntegerField(required=False)

    def create(self, request, data, commit=True):
        inst = ShortenedUrls()
        inst.creator_id = request.user.id
        inst.category = data.get("category", None)
        inst.target_url = data.get("target_url").strip()
        if commit:
            try:
                inst.save()
            except Exception as e:
                print(e)
            else:
                url_count_changer(request, True)
        print(inst)
        return inst


class BrowerStatSerializer(serializers.Serializer):
    web_browser = serializers.CharField(max_length=50)
    count = serializers.IntegerField()
    date = serializers.DateField(source="created_at__date", required=False)


class QrListSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = QrCode
        fields = "__all__"


class QrCreateSerializer(serializers.Serializer):
    nick_name = serializers.CharField(max_length=50)
    target_url = serializers.CharField(max_length=2000)
    category = serializers.IntegerField(required=False)

    def create(self, request, data, commit=True):
        inst = QrCode()
        inst.creator_id = request.user.id
        inst.category = data.get("category", None)
        inst.target_url = data.get("target_url").strip()
        qr_code = create_qr(inst.nick_name, inst.target_url)
        inst.qr_img = qr_code
        if commit:
            try:
                inst.save()
            except Exception as e:
                print(e)
            else:
                url_count_changer(request, True)
        print(inst)
        return inst
