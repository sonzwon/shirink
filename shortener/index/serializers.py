# from django.contrib.auth.models import User as U
# from shortener.models import Users
# from rest_framework import serializers


# class UserBaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = U
#         exclude = ("password",)

# class RegisterSerializer(serializers.Serializer):
#     full_name = serializers.CharField(max_length=30, required=False)
#     username = serializers.CharField(max_length=30, required=False)
#     email = serializers.EmailField(max_length=254)

#     def create(self, request, data, commit=True):
#         inst = U()
#         inst.username = data.get("username", None)
#         inst.email = data.get("email")
