from django.urls import path
from . import views
urlpatterns = [
    # base Urls
    path('',views.home,name="Home"),
    path('ragister/',views.ragister,name="Ragister"),
]
