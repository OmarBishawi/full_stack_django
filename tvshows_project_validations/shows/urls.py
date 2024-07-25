from django.urls import path
from . import views

app_name = 'shows'

urlpatterns = [
    path('', views.index, name='index'),  # List all shows
    path('new/', views.new_show, name='new'),  # Form to create a new show
    path('create/', views.new_show, name='create'),  # POST route to create a new show
    path('<int:id>/', views.show_detail, name='detail'),  # Show details
    path('<int:id>/edit/', views.edit_show, name='edit'),  # Form to edit a show
    path('<int:id>/update/', views.edit_show, name='update'),  # POST route to update a show
    path('<int:id>/destroy/', views.delete_show, name='destroy'),  # POST route to delete a show
]
