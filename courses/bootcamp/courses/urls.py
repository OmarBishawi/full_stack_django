from django.urls import path
from . import views

urlpatterns = [
    path('',views.index , name="index"),
    path('add/',views.add_course , name="add_course"),
    path('remove/<int:course_id>/', views.remove_course, name= 'remove_course'),
    path('comment/<int:course_id>/', views.course_comments , name='course_comments'),
]