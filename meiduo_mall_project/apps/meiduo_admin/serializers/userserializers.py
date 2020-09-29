from rest_framework import serializers
from apps.users.models import User
from django.contrib.auth.hashers import make_password


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'mobile',
            'email',

            'password',
        ]


        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8, 'max_length': 20, 'required': True},
            'username': {'max_length': 20, 'required': True},
            'mobile': {'required': True}
        }

    def validate(self, attrs):
        # 1. 密码加密
        raw_password = attrs.pop('password')  # 明文
        secret_password = make_password(raw_password)
        attrs['password'] = secret_password
        attrs['is_staff'] = True
        return attrs
