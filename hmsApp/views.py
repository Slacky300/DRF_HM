from django.shortcuts import render
from . models import *
from . serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

class DepartmentGet(generics.ListCreateAPIView):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartementGetUpDel(generics.RetrieveDestroyAPIView):
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer



@api_view(["GET"])
def getPatientsOfDept(request, pk):

    dept = Department.objects.get(pk = pk)
    patient = UserAccount.objects.filter(department = dept)
    serializer = UserSerializer(patient, many = True)
    return Response(serializer.data)






class RegisterUser(APIView):

    def post(self,request):
        serializer = UserSerializer(data = request.data)
        if not serializer.is_valid():
            
            return Response({'status': 403, 'errors': serializer.errors,'message': "Please provide valid data"})
        serializer.save()
        user = UserAccount.objects.get(username = serializer.data['username'])
        if request.data["is_patient"]:
            group = Group.objects.get(name = "Patients")
            user.groups.add(group)
            user.save()
        elif request.data["is_doctor"]:
            if not request.data["department"]:
                return Response({"status": 403, "message": "Department id must be provided"})
            user.is_doctor = True
            dept = Department.objects.get(pk = request.data["department"])
            if not dept:
                return Response({"status": 404, "message": "No such department exists"})
            
            user.department = dept
            user.is_patient = False
            group = Group.objects.get(name = "Doctors")
            user.groups.add(group)
            user.save()
        token , _ = Token.objects.get_or_create(user=user)
      
        return Response({'status': 201, 'token': str(token), 'message': "User created successfully"})
    