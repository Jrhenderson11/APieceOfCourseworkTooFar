from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('cv', views.cv, name='CV'),
    path('cv/edit', views.cv_edit, name='cv_edit'),
]
