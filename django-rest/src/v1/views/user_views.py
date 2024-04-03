from src.v1.models import User
from src.v1.permissions.get_list_user_permission import GetListUserPermission
from src.v1.paginations.custom_page_number_pagination import CustomPageNumberPagination
from src.v1.serializers.user_serializers import (
    CreateUserSerializer,
    DetailUserSerializer,
    ListUserSerializer,
    LoginUserSerializer,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, authentication, status, filters


class SignUserViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    queryset = User.objects.filter(is_active=True)

    @action(
        detail=False, methods=["POST"], url_path="sign-up", name="Create User",
    )
    def create_user(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=["POST"], url_path="sign-in",
    )
    def login(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, GetListUserPermission]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        # user can get only his/her support tickets
        # staff can get all support tickets
        user = self.request.user
        if user.is_employee:
            return User.objects.filter(
                is_active=True).order_by("id")

        return User.objects.filter(
            id=user.id, is_active=True).order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return ListUserSerializer

        return DetailUserSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
