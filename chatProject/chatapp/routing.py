from django.urls import path
from . import consumers

webscoket_urlpatterns=[
    path('ws/jac/<int:sender_id>/<int:reciver_id>/',consumers.myAsyncJsonConsumer.as_asgi()),
]
