from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from django.core.cache import cache
from django.conf import settings
import re

from . import models


class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['username', 'password', 'id']

        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        # 多方式登录
        user = self._get_user(attrs)
        # 签发token
        token = self._get_token(user)

        self.context['token'] = token
        self.context['user'] = user

        return attrs

    def _get_user(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        # 多方式登录
        if re.match('^1[3-9][0-9]{9}$', username):
            user = models.User.objects.filter(telephone=username).first()
        elif re.match('^.*@.*$', username):
            user = models.User.objects.filter(email=username).first()
        else:
            user = models.User.objects.filter(username=username).first()
        if user:
            ret = user.check_password(password)
            if ret:
                return user
            else:
                raise ValidationError('密码或用户名错误')
        else:
            raise ValidationError('用户不存在')

    def _get_token(self, user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


# 手机号 验证码
class CodeUserSerializers(serializers.ModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['telephone', 'code']

    def validate(self, attrs):

        user = self._get_user(attrs)
        # 签发token
        token = self._get_token(user)

        self.context['token'] = token
        self.context['user'] = user

        return attrs

    def _get_user(self, attrs):

        telephone = attrs.get('telephone')
        code = attrs.get('code')

        cache_code = str(cache.get(settings.PHONE_CACHE_KEY % telephone))

        if code != cache_code:
            raise ValidationError('验证码错误')

        if re.match('^1[3-9][0-9]{9}$', telephone):
            user = models.User.objects.filter(telephone=telephone).first()
            if user:
                cache.set(settings.PHONE_CACHE_KEY % telephone, '')  # 把使用过的验证码删除
                return user
            else:
                raise ValidationError('用户不存在')
        else:
            raise ValidationError('手机号格式错误')

    def _get_token(self, user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


# 注册
class UserRegisterSerializers(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4, write_only=True)

    class Meta:
        model = models.User
        fields = ['telephone', 'password', 'code', 'username']

        extra_kwargs = {
            'password': {'max_length': 18, 'min_length': 4},
            'username': {'read_only': True}
        }

    def validate(self, attrs):
        telephone = attrs.get('telephone')
        code = attrs.get('code')

        cache_code = str(cache.get(settings.PHONE_CACHE_KEY % telephone))

        if code != cache_code:
            raise ValidationError('验证码错误')

        if not re.match('^1[3-9][0-9]{9}$', telephone):
            raise ValidationError('手机号格式错误')

        exist = models.User.objects.filter(telephone=telephone).exists()
        if exist:
            raise ValidationError('手机号已注册')
        cache.set(settings.PHONE_CACHE_KEY % telephone, '')  # 把使用过的验证码删除

        attrs['username'] = telephone
        attrs.pop('code')
        return attrs

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user
