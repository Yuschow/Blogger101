from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User

class UserAPI(APIView):
    def post(self, request):
        # 创建用户
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not username or not password or not email:
            return Response({"error": "missing parameter"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User(username=username, email=email)
        user.set_password(password)  # 密码加密
        user.save()

        return Response({"message": "user created", "id": user.id}, status=status.HTTP_201_CREATED)

    def get(self, request):
        # 查询用户
        username = request.query_params.get("username")
        if not username:
            return Response({"error": "Missing username"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
