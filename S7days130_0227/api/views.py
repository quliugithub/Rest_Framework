from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
import json
from rest_framework.request import Request
# Create your views here.
#2 from rest_framework.versioning import BaseVersioning
#3 from rest_framework.versioning import QueryParameterVersioning
from rest_framework.versioning import URLPathVersioning
from django.urls import reverse
from api import models
#2class ParamVersion(object):
#2   def determine_version(self, request, *args, **kwargs):
#2       version = request.query_params.get('version')
#2       return version

class UsersView(APIView):
    #2 versioning_class = ParamVersion
    #3 versioning_class = QueryParameterVersioning
    #4 versioning_class = URLPathVersioning
    def get(self,request,*args,**kwargs):
        self.dispatch
        #version = request._request.GET.get('version')

        #version = request.query_params.get('version')
        print(request.version)
        #反向生成URL(rest_framework)
        u1 = request.versioning_scheme.reverse(viewname='uuu',request=request)
        print(u1)

        #反向生成URL
        u2 = reverse(viewname='uuu',kwargs={'version':2})
        print(u2)
        return HttpResponse('用户列表')


class DjangoView(APIView):

    def post(self,request,*args,**kwargs):
        print(type(request._request))
        from django.core.handlers.wsgi import WSGIRequest
        return HttpResponse('POST和GET')


from rest_framework.parsers import JSONParser,FormParser
class ParserView(APIView):

    #parser_classes =  [JSONParser,FormParser]
    """
    JSONParser表示只能解析content-type:/application/json头
    FormParser表示只能解析content-type：application/x-www-form-urlencoded
    
    """
    def post(self,request,*args,**kwargs):
        """
        允许用户发送JSON数据
        a.content_type: application.json
        b.{'name':'alex',age:18}
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        """
        获取用户请求
        获取用户请求体
        根据用户请求偷和 parser_classes =  [JSONParser,FormParser]中支持的请求偷进行比较
        
        """
        #获取解析后的结果
        print(request.data)
        return HttpResponse('ParserView')

from rest_framework import serializers
class RolesSerializers(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()

class RolesView(APIView):

    def get(self, request, *args, **kwargs):

        #方式一
        #roles = models.Role.objects.all().values('id','title')
        #roles = list(roles)
        #ret = json.dumps(roles,ensure_ascii=True)
        #方式二 对于(obj,obj,obj)
        #roles = models.Role.objects.all()
        #ser = RolesSerializers(instance=roles,many=True)
        #ret = json.dumps(ser.data)
        #return HttpResponse(ret)

        roles = models.Role.objects.all().first()
        ser = RolesSerializers(instance=roles,many=False)
        #ser.data已经是序列化好的数据
        print(ser.data)
        #ret = json.dumps(ser.data)
        return HttpResponse(ser.data)


# class UserInfoSerializers(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#     #source参数 连接数据库字段
#     #type = serializers.CharField(source="user_type")
#     #get_提取到的字段_display 将数据库中的选项展示对应的中文值
#     #source中的名字不能和变量名相同
#     type2 = serializers.CharField(source="get_user_type_display")
#     gp = serializers.CharField(source='group.title')
#     #rl = serializers.CharField(source='role.all')
#     rl = serializers.SerializerMethodField()
#
#     def get_rl(self,obj):
#         role_obj_list = obj.role.all()
#         print(role_obj_list)
#         ret = []
#         for item in role_obj_list:
#             ret.append({"id":item.id,"title":item.title})
#         return ret


class UserInfoSerializers(serializers.ModelSerializer):
    # UsType = serializers.CharField(source="get_user_type_display")
    # rls = serializers.SerializerMethodField()
    #
    # def get_rls(self,obj):
    #     role_obj_list = obj.role.all()
    #     ret = []
    #     for item in role_obj_list:
    #         ret.append({"id":item.id,"title":item.title})
    #     return ret
    #
    # class Meta:
    #     model = models.UserInfo
    #     #fields = '__all__'
    #     fields = ["id","username","password","UsType","rls","group"]

    class Meta:
        model = models.UserInfo
        #ields = '__all__'
        fields = ["username","password"]
        depth = 1
class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        userinfo = models.UserInfo.objects.all()
        ser = UserInfoSerializers(instance=userinfo,many=True)
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)


class xxxvalidators(object):
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        # if value != self.base:
        #     message = 'This field must be %s.' % self.base
        #     raise serializers.ValidationError(message)
        if not value.startswith(self.base):
            message = "标题必须以%s开头 " % self.base
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # 执行验证之前调用,serializer_fields是当前字段对象
        pass

class UserGroupSerializers(serializers.Serializer):
    title = serializers.CharField(error_messages={"requied":"标题不能为空"},validators=[xxxvalidators('老男人'),])

class UserGroupView(APIView):
    def post(self, request, *args, **kwargs):
        #print(request.data)
        ser = UserGroupSerializers(data=request.data)
        #print(ser)
        if ser.is_valid():
            print(ser.validated_data)
        else:
            print(ser.errors)

        return HttpResponse("POST请求，响应内容")







