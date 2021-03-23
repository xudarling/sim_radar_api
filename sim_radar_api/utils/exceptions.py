#     'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
# 全局处理异常 + 加入日志
from rest_framework.views import exception_handler

from .response import APIResponse
from .logger import log


def common_exception_handler(exc, context):
    ret = exception_handler(exc, context)
    # 记录错误日志
    log.error('view是: %s, 错误是: %s' % (context['view'].__class__.__name__, str(exc)))
    if not ret:
        if isinstance(exc, KeyError):
            return APIResponse(code=0, msg='key error')
        return APIResponse(code=0, msg='error', result=str(exc))
    else:
        return APIResponse(code=0, msg='error', result=ret.data)
