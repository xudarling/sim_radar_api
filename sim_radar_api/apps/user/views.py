from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.decorators import action
from . import serializer
from . import models
from sim_radar_api.utils.response import APIResponse


class LoginView(ViewSet):

    # 手机号/用户名/邮箱 密码 登录接口
    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        ser = serializer.UserSerializers(data=request.data)
        if ser.is_valid():
            token = ser.context['token']
            username = ser.context['user'].username

            return APIResponse(token=token, username=username)
        else:
            return APIResponse(code=0, msg=ser.errors)

    # 手机号 验证码 登录接口
    @action(methods=['POST'], detail=False)
    def code_login(self, request, *args, **kwargs):

        ser = serializer.CodeUserSerializers(data=request.data)
        if ser.is_valid():
            token = ser.context['token']
            username = ser.context['user'].username

            return APIResponse(token=token, username=username)
        else:
            return APIResponse(code=0, msg=ser.errors)

    # 验证手机号
    @action(methods=['GET'], detail=False)
    def check_telephone(self, request, *args, **kwargs):
        import re
        telephone = request.query_params.get('telephone')
        if not re.match('^1[3-9][0-9]{9}$', telephone):
            return APIResponse(code=0, msg='手机号格式错误')
        try:
            models.User.objects.get(telephone=telephone)
            return APIResponse(code=1)
        except:
            return APIResponse(code=0, msg='手机号未注册')


class SendSmsView(ViewSet):
    from .throttlings import SMSThrottle

    throttle_classes = [SMSThrottle]  # 局部添加 访问频率限制

    # 发送验证码
    @action(methods=['GET'], detail=False)
    def send_sms(self, request, *args, **kwargs):
        import re
        import random
        from sim_radar_api.libs.tencent.sms import send_sms_single
        from django.core.cache import cache
        from django.conf import settings
        from rest_framework.exceptions import ValidationError

        telephone = request.query_params.get('telephone')
        if not re.match('^1[3-9][0-9]{9}$', telephone):
            return APIResponse(code=0, msg='手机号格式错误')

        # 生成验证码 和短信 模板
        code = random.randrange(1000, 9999)
        template_id = settings.TENCENT_SMS_TEMPLATE.get('login')

        # 由于没有免费短信了 故 验证码 设定为 9999
        # result = send_sms_single(phone_num=telephone, template_id=template_id, template_param_list=[code, ])
        code = 9999
        result = {'result': 0}

        # 缓存
        cache.set(settings.PHONE_CACHE_KEY % telephone, code, 180)

        if result['result'] != 0:
            return APIResponse(code=0, msg='短信验证码发送失败')
        else:
            return APIResponse(code=1, msg='短信验证码发送成功')


class RegisterView(GenericViewSet, CreateModelMixin):
    queryset = models.User.objects.all()
    serializer_class = serializer.UserRegisterSerializers

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        username = response.data.get('username')

        return APIResponse(code=1, msg='注册成功', username=username)
