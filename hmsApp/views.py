
from . models import *
from . serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.hashers import check_password
from . perimissions import *
from rest_framework.authentication import  TokenAuthentication
from django.http import HttpResponse


def home(request):

    return HttpResponse("Hospital management system")

class GetAndAddDoctors(APIView):

    permission_classes = [IsDoctor]
    authentication_classes = [TokenAuthentication]

    def get(self,request):
        fields = ('id', 'username')
        queryset = UserAccount.objects.filter(is_doctor = True)
        serializers = UserSerializer(queryset, many = True, fields = fields)
        return Response(serializers.data)
    
    def post(self, request):

        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            return Response({"status": 201,"msg":"Created"})
        


@api_view(["GET","PUT","DELETE"])
@permission_classes([IsOwnerOrReadOnly])
@authentication_classes([TokenAuthentication])
def updateDoctor(request,pk):

    
    try: 
        doctor = UserAccount.objects.get(pk = pk, is_doctor = True)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":

        serializer = UserSerializer(doctor)
        return Response(serializer.data)
    
    if request.method == "PUT":
        
        serializer = UserSerializer(doctor, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200,"msg":"Updated"})
        else:
            return Response({"status": 500, "msg": serializer.errors})
        

    if request.method == "DELETE":
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class GetAndAddPatients(generics.ListCreateAPIView):
    
    permission_classes = [IsDoctor]
    authentication_classes = [TokenAuthentication]
   
    queryset = UserAccount.objects.filter(is_patient = True)
    serializer_class = UserSerializer

    def list(self, request):
       
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True, fields = ('id', 'username'))
        return Response(serializer.data)
    



@api_view(["GET","PUT","DELETE"])
@permission_classes([IsSameDoctorOfPatient])
@authentication_classes({TokenAuthentication})
def updatePatient(request,pk):



    try: 
        patient = UserAccount.objects.get(pk = pk, is_patient = True)

    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":

        serializer = UserSerializer(patient)
        return Response(serializer.data)
    
    if request.method == "PUT":
        
        serializer = UserSerializer(patient, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": status.HTTP_200_OK,"msg":"Updated"})
        else:
            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "msg": serializer.errors})
        

    if request.method == "DELETE":
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class PatientRecords(generics.ListCreateAPIView):
    permission_classes = [IsDoctor]
    authentication_classes = [TokenAuthentication]
    serializer_class = Patient_recordsSerializer

    def get_queryset(self):
        return Patient_Records.objects.filter(department = self.request.user.department)
    
    def list(self,request):
        queryset = self.get_queryset()
        serializer = Patient_recordsSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):

        serializer = Patient_recordsSerializer(data = request.data)
        try:
            if serializer.is_valid():
                serializer.save()
            patient = UserAccount.objects.get(pk = serializer.data["patient_id"])
            department = Department.objects.get(pk = serializer.data["department"])
            if request.user.department != department:
                return Response({"msg": "Not authorized to add records, department does not match"}, status= status.HTTP_406_NOT_ACCEPTABLE)
            patient.department = department
            patient.save()
            return Response({"msg": "Created record"}, status=status.HTTP_200_OK)
        except UserAccount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    


@api_view(["GET","PUT","DELETE"])
@permission_classes([IsSameDoctorAndPatient])
@authentication_classes([TokenAuthentication])
def updateRecords(request,pk):

    try: 
        patient_rec = Patient_Records.objects.get(pk = pk)
    except Patient_Records.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":

        serializer = Patient_recordsSerializer(patient_rec)
        return Response({"record": serializer.data},status= status.HTTP_200_OK)
    
    if request.method == "PUT":

        serializer = Patient_recordsSerializer(patient_rec, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Updated successfully"},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_304_NOT_MODIFIED)
    
    if request.method == "DELETE":

        patient_rec.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class DepartmentGet(generics.ListCreateAPIView):


    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer



@api_view(["GET","PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsDoctorOfSameDept])
def getPatientsOfDept(request, pk):

    dept = Department.objects.get(pk = pk)
    patient = UserAccount.objects.filter(department = dept, is_patient = True)
    serializer = UserSerializer(patient, many = True, fields = ["id", "username", "email"])
    return Response(serializer.data)


@api_view(["GET","PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsDoctorOfSameDept])
def getDoctorsOfDept(request,pk):
    
    dept = Department.objects.get(pk = pk)
    patient = UserAccount.objects.filter(department = dept, is_doctor = True)
    serializer = UserSerializer(patient, many = True, fields = ["id", "username", "email"])
    return Response(serializer.data)



class RegisterUser(APIView):

    def post(self,request):
        serializer = UserSerializer(data = request.data)

        if not serializer.is_valid():
            
            return Response({'status': 403, 'errors': serializer.errors,'message': "Please provide valid data"})
        
        serializer.save()

        user = UserAccount.objects.get(username = serializer.data['username'])

        if "is_doctor" in request.data:
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
        else:
            group = Group.objects.get(name = "Patients")
            user.groups.add(group)
            user.save()
         
        token , _ = Token.objects.get_or_create(user=user)
      
        return Response({'status': 201, 'token': str(token), 'message': "User created successfully"})
    


class LoginUser(APIView):

    def get(self,request):
        username = request.data["username"]
        password = request.data["password"]

        try:

            user = UserAccount.objects.get(username = username)
            if not check_password(password, user.password):
                return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            token = Token.objects.get_or_create(user = user)[0].key
            login(request,user)
            return Response({"token": token, "msg": "Successfully logged in!"}, status=status.HTTP_200_OK)
        except UserAccount.DoesNotExist:
            
            return Response(status=status.HTTP_404_NOT_FOUND)



class LogoutUser(APIView):

    def post(self, request):
        try:
            token =  Token.objects.get(user = request.user)
            token.delete()
            logout(request)
        except Token.DoesNotExist:
            logout(request)
        return Response({"msg": "Logged out successfully"}, status=status.HTTP_200_OK)



    




  
