from django.urls import path
from django.urls.resolvers import URLPattern
from .views import ContactView


urlpatterns = [
    path("", ContactView.as_view(), name="contact")
]

