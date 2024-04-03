from src.v1.views.views import welcome
from src.v1.views.reply_views import ReplyModelViewSet
from src.v1.views.user_views import UserModelViewSet, SignUserViewSet
from src.v1.views.support_ticket_views import SupportTicketModelViewSet

from django.urls import path

from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)
router.register(r"user", UserModelViewSet, basename="user")
router.register(r"reply", ReplyModelViewSet, basename="reply")
router.register(r"sign_user", SignUserViewSet, basename="sign_user")
router.register(r"support_ticket", SupportTicketModelViewSet, basename="support_ticket")


urlpatterns = [
    path("welcome", welcome),
]

urlpatterns += router.urls
