from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name="home"),
    path('departments/',DepartmentGet.as_view(), name="department"),
    path('departments/<int:pk>/patients/',getPatientsOfDept,name="get_patients_dept"),
    path('departments/<int:pk>/doctors/',getDoctorsOfDept,name="get_doctors_dept"),
    path('register/',RegisterUser.as_view(), name="register_user"),
    path('doctors/', GetAndAddDoctors.as_view(), name="doctors"),
    path('doctors/<int:pk>/', updateDoctor, name="upt_doctor"),
    path('patients/', GetAndAddPatients.as_view(), name="patients"),
    path('patients/<int:pk>/', updatePatient, name="upt_patients"),
    path('patient_records/', PatientRecords.as_view(),name="patient_records"),
    path('patient_records/<int:pk>/', updateRecords,name="upt_patient_records"),
    path('login/',LoginUser.as_view(),name="login"),
    path('logout/', LogoutUser.as_view(), name="logout"),
]