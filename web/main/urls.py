from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # URL 패턴은 루트 URL에 해당하므로 비워둡니다.
    path('main/<int:lecture_id>/', views.detail, name='detail'),
    path('main/create_comment/<int:lecture_id>', views.create_comment, name='create_comment'),
    path('main/new_comment/<int:lecture_id>', views.new_comment, name='new_comment'),
    path('main/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comment/update/<int:comment_id>/', views.update, name='update_comment'),
    path('main/add/<int:lecture_id>/', views.add_lecture, name='add_lecture'),
    path('main/my_lectures/', views.user_lectures, name='user_lectures'),
    path('main/delete_lecture/<int:user_lecture_id>/', views.delete_my_lecture, name='delete_my_lecture'),
    path('main/filter/', views.lecture_list, name='filter'),
    path('main/Ai/', views.ai, name='ai'),
    path("main/learn/",views.learn, name= "learn"),

]
