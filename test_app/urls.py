from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("with_html", views.with_html),
    path("with_java", views.with_java),
    path("with_template", views.with_template),
]
