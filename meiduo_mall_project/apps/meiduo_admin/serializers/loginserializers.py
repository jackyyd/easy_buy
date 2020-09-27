from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=20,
        allow_blank=False,
        allow_null=False
    )
    password = serializers.CharField(
        required=True,
        max_length=20,
        min_length=8,
        allow_blank=False,
        allow_null=False
    )
    # 校验
    def validate(self, attrs):
        user = authenticate(**attrs)
        if user is None:
            raise serializers.ValidationError("用户名或密码错误！")

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return {
            'user': user,
            'token': token
        }
