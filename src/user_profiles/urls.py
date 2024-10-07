from django.urls import path, include
from . import views

urlpatterns = [
#    path("", home_page_view, name="home"),
    path("", views.profile_list_view),
    path("<username>/", views.profile_detail_view)
  ]
