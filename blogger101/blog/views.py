from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .models import Group
from .models import Role
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
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

class GroupAPI(APIView):
    def post(self,request):
        groupname = request.data.get("groupname")
        groupcode = request.data.get("groupcode")

        if not groupname or not groupcode:
            return Response({"error":"Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)
        
        if Group.objects.filter(groupname=groupname).exists():
            return Response({"error":"groupname already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        group = Group(groupname=groupname,groupcode=groupcode)
        group.save()

        return Response({"message":"group created", "id": group.id}, status=201)
    
    def get(self,request):
            page = int(request.query_params.get("page", 1))
            page_size = int(request.query_params.get("page_size", 10))

            groups = Group.objects.all().order_by("id")
            paginator = Paginator(groups, page_size)

            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                return Response({"error": "Inavalid page number"}, status=400)
            
            data = [
                {
                    "id": g.id,
                    "groupname":g.groupname,
                    "groupcode":g.groupcode
                }
                for g in page_obj
            ]

            return Response({
                "total": paginator.count,
                "page": page,
                "page_size": page_size,
                "total_pages": paginator.num_pages,
                "results": data,
            },status=200)
    
class RoleAPI(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        group_id = request.data.get("group_id")

        if not user_id or not group_id:
            return Response({"error": "Missing user_id or group_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error":"user not found"}, status= status.HTTP_404_NOT_FOUND)
        
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"error":"group not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if Role.objects.filter(user=user, group=group).exists():
            return Response({"error": "Role already exists"}, status=status.HTTP_400_BAD_REQUEST)
        role = Role(user=user, group=group)
        role.save()
        
        return Response({"message": "Role created", "id": role.id}, status=status.HTTP_201_CREATED)
    
    def get(self,request):
        user_id = request.query_params.get("user_id", None)

        if not user_id:
            return Response(
                {"error": "Missing user_id parameter"},status=status.HTTP_400_BAD_REQUEST)
        
        roles = Role.objects.filter(user__id=user_id).select_related("user", "group")

        if not roles.exists():
            return Response(
                {"error": "No roles found for this user"},status=status.HTTP_404_NOT_FOUND)
        
        data = []
        for role in roles:
            data.append({
                "role_id": role.id,
                "user_id": role.user.id,
                "username": role.user.username,
                "group_id": role.group.id,
                "groupname": role.group.groupname
            })
        
        return Response({"roles": data}, status=status.HTTP_200_OK)
            
        
        






    
