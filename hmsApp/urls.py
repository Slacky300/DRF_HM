from django.urls import path
from .views import *
urlpatterns = [
    path('departments/',DepartmentGet.as_view(), name="department"),
    path('departments/<int:pk>/',DepartementGetUpDel.as_view(), name="department_detail"),
    path('departments/<int:pk>/patients/',getPatientsOfDept,name="get_patients_dept"),
    path('register/',RegisterUser.as_view(), name="register_user")
]