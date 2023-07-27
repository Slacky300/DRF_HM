from rest_framework import permissions
from .models import *
from rest_framework.response import Response
class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor 
    
class IsOwnerOrReadOnly(permissions.BasePermission):

    

   def has_object_permission(self, request, view, obj):
       
       if request.method in permissions.SAFE_METHODS:
           return True
       
       return obj.id == request.user.id
   
class IsSameDoctorOfPatient(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
      
        if request.method in permissions.SAFE_METHODS:
           return True
       

        try:
            patient_rec = Patient_Records.objects.filter(patient_id = obj).first()

            return patient_rec.doctor_name.id == request.user.id
        except Patient_Records.DoesNotExist:
            return Response({"msg": "not so good"})


class IsSameDoctorAndPatient(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
           return True
        
        return obj.patient_id.id == request.user.id or obj.doctor_name.id == request.user.id