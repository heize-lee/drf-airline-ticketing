# backend/accounts/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializers import ChangePasswordSerializer

@api_view(['POST'])
def signup(request):
    data = request.data
    user = User.objects.create_user(
        first_name=data['firstName'],
        last_name=data['lastName'],
        email=data['email'],
        username=data['email'],
        password=data['password']
    )
    return Response({"message": "User created successfully", "user": {
        "id": user.id,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "email": user.email,
        "tickets": []
    }}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    data = request.data
    user = authenticate(username=data['email'], password=data['password'])
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "token": str(refresh.access_token),
            "user": {
                "id": user.id,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                "tickets": []
            }
        })
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, uid):
    try:
        user = User.objects.get(id=uid)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if not user.check_password(serializer.data.get("old_password")):
            return Response({"message": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
