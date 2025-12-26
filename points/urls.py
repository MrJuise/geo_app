from django.urls import path
from .api import PointCreateAPIView, MessageCreateAPIView, PointSearchAPIView, MessageSearchAPIView

urlpatterns = [
    path('points/', PointCreateAPIView.as_view(), name='point-create'),
    path('points/messages/', MessageCreateAPIView.as_view(), name='message-create'),
    path('points/search/', PointSearchAPIView.as_view(), name='point-search'),
    path('message/search/', MessageSearchAPIView.as_view(), name='message-search'),
]