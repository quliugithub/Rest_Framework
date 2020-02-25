from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.request import Request
# Create your views here.
#2 from rest_framework.versioning import BaseVersioning
#3 from rest_framework.versioning import QueryParameterVersioning
from rest_framework.versioning import URLPathVersioning
from django.urls import reverse
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
