from django.urls import path
from .views import *
urlpatterns = [
    path('departments/',DepartmentGet.as_view(), name="department"),
    path('departments/<int:pk>/',DepartementGetUpDel.as_view(), name="department_detail"),
    path('departments/<int:pk>/patients/',getPatientsOfDept,name="get_patients_dept"),
    path('register/',RegisterUser.as_view(), name="register_user"),
    path('doctors/', GetDoctors.as_view(), name="doctors"),
    path('doctors/<int:pk>/', updateDoctor, name="upt_doctor"),
    path('patients/', GetPatients.as_view(), name="patients"),
    path('patients/<int:pk>/', updatePatient, name="upt_patients"),
    path('patient_records/', PatientRecords.as_view(),name="patient_records"),
    path('patient_records/<int:pk>/', updateRecords,name="upt_patient_records"),
    path('login/',loginUser,name="login"),
    path('logout/', logoutUser, name="logout"),
]