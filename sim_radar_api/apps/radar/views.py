from django.shortcuts import render
import json

from sim_radar_api.utils.response import APIResponse
# Create your views here.
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from .radar import get_dbz, get_one_dbz, get_all_canvas, plt_value,\
    get_canvas, plt_value2, get_canvas2


class Radar(ViewSet):

    # # 获取 雷达及天气信息 返回 回波图
    # @action(methods=['POST'], detail=False)
    # def value(self, request, *args, **kwargs):
    #     print(request.data)
    #
    #     res = plt_value(**request.data)
    #     return APIResponse(code=1, ret=res)
    #
    # # 获取 插值后回波
    # @action(methods=['POST'], detail=False)
    # def dbz(self, request, *args, **kwargs):
    #     print(request.data)
    #     angleData, radiusData, dbzData, vrData = get_dbz(**request.data)
    #     return APIResponse(
    #         code=1, angleData=angleData, radiusData=radiusData,
    #         dbzData=dbzData, vrData=vrData
    #     )

    ###
    @action(methods=['POST'], detail=False)
    def dbz(self, request, *args, **kwargs):
        """
        返回dBZ和Vr
        """
        ret = get_dbz(**request.data)
        return APIResponse(code=1, ret=ret)

    @action(methods=['POST'], detail=False)
    def onedbz(self, request, *args, **kwargs):
        ret = get_one_dbz(**request.data)
        return APIResponse(code=1, ret=ret)

    # 版本 0.1 使用, 直接返回 全都仰角的 数据
    @action(methods=['POST'], detail=False)
    def canvasAll(self, request, *args, **kwargs):
        ret = get_all_canvas(**request.data)
        return APIResponse(code=1, ret=ret)

    # 模拟观测功能 用户点击开始观测 返回 dBZ 和 Vr
    @action(methods=['POST'], detail=False)
    def canvas(self, request, *args, **kwargs):
        ret = get_canvas(**request.data)
        return APIResponse(code=1, ret=ret)

    #  对比功能: 用户 点击开始模拟 返回 对比观测的 dBZ 和 Vr 数据
    @action(methods=['POST'], detail=False)
    def canvas2(self, request, *args, **kwargs):
        ret = get_canvas2(**request.data)
        return APIResponse(code=1, ret=ret)

    # 用户设置雷达参数后 返回 天气场和雷达位置 图
    @action(methods=['POST'], detail=False)
    def pltImg(self, request, *args, **kwargs):
        ret = plt_value(**request.data)
        return APIResponse(code=1, ret=ret)

    # 开打页面时, 返回 不带雷达范围的天气场图
    @action(methods=['POST'], detail=False)
    def pltImg2(self, request, *args, **kwargs):
        print(request.data)
        ret = plt_value2(**request.data)
        return APIResponse(code=1, ret=ret)
