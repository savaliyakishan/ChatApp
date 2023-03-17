from django.urls import path
from . import views,dashbord,message
urlpatterns = [
    # base Urls

    path('',views.index,name="Home"),
    path('login/',views.userlogin,name="User-Login"),
    path('ragister/',views.ragister,name="Ragister"),
    path('logout/',views.userLogout,name="User-Logout"),

    #deshbord
    path('deshbord/',dashbord.index,name="Dashbord"),
    path('deshbord/<int:pk>',dashbord.index,name="Chat-with-User"),
    path('deshbord/profile/',dashbord.profile,name="User-Profile"),

    # message
    path('deshbord/<int:pk>/message',message.messageinfo,name="Chat-with-User-message"),

    # Call

    # path('deshbord/<int:sender>/Call/<int:reciver>',message.callinfo,name="Chat-with-User-message"),
]
