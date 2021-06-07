from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView
from .views import index, by_rubric, add_and_save, bb_delete, BbCreateView,rubrics
from .views import api_rubrics,api_bb,api_rubric_detail,api_bb_detail


urlpatterns = [
    path('api/bb/<int:pk>/',api_bb_detail),
    path('api/rubric/<int:pk>/',api_rubric_detail),
    path('api/rubrics/',api_rubrics),
    path('api/bb/',api_bb),
    path('',index,name='index'),
    path('<int:rubric_id>/',by_rubric,name='by_rubric'),
    path('add/',add_and_save,name='add'),
    path('delete/<int:pk>/',bb_delete,name='bb_delete'),
    path('add/rubrics/',BbCreateView.as_view(),name='add_rubrics'),
    path('delete/rubrics/',rubrics,name='rubrics'),
    path('accounts/login/',LoginView.as_view(),name='login'),
    path('accounts/logout/',LogoutView.as_view(template_name='registration/logged_out.html'),name='logout'),
    path('accounts/password_change/',PasswordChangeView.as_view(template_name='registration/password_change_form.html'),name='password_change'),
]