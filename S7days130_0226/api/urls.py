from django.conf.urls import url
from api import views
urlpatterns = [
#    url(r'user/$',views.UsersView.as_view())
    url(r'^(?P<version>[V1|V2]+)/users/$', views.UsersView.as_view(),name='uuu'),
    url(r'^(?P<version>[V1|V2]+)/django/$', views.DjangoView.as_view(),name='ddd'),
    url(r'^(?P<version>[V1|V2]+)/parser/$', views.ParserView.as_view(),name='p'),
    url(r'^(?P<version>[V1|V2]+)/roles/$', views.RolesView.as_view(),name='p1'),
    url(r'^(?P<version>[V1|V2]+)/usersinfo/$', views.UserInfoView.as_view(),name='p1')
]