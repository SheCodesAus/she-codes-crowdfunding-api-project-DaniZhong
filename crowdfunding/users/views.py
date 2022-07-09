from django.shortcuts import render

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserDetailSerializer
from .permissions import IsUser

# Create your views here.
class CustomUserList(APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
            return Response(serializer.data)
        return Response(serializer.errors)

# users/<pk>
class CustomUserDetail(APIView):
    permission_classes = [IsUser]

    def get_object(self, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            self.check_object_permissions(self.request,user)
            return user
        except CustomUser.DoesNotExist:
            raise Http404
    
    # GET request
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserDetailSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        serializer = CustomUserDetailSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            if ('password' in self.request.data):
                password = make_password(self.request.data['password'])
                serializer.save(password=password)
            else:
                serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )   

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response({'message': 'User was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)