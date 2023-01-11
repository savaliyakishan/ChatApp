from django.urls import path
from . import views,dashbord
urlpatterns = [
    # base Urls

    path('',views.index,name="Home"),
    path('login/',views.userlogin,name="User-Login"),
    path('ragister/',views.ragister,name="Ragister"),
    path('logout/',views.userLogout,name="User-Logout"),

    #deshbord
    path('deshbord/',dashbord.index,name="Dashbord"),
    path('deshbord/profile/',dashbord.profile,name="User-Profile"),
]
