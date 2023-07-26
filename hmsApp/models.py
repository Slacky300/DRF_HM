from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class Department(models.Model):

    name = models.CharField(max_length=100)
    diagnostics = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, password = None):
        if not email:
            raise ValueError('User must provide a email')
        
        user = self.model(
            email = email,
            username = username
        )


        user.set_password(password)
        user.save(using = self._db)

        return user


    def create_superuser(self, email, username, password = None):
        user = self.create_user(email,username,password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using = self._db)

        return user
    
    def create_doctor(self, email, username, password = None):
        user = self.create_user(email, username, password)

        user.is_doctor = True
        user.is_patient = False
        user.save(using = self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length = 50,unique=True)
    username = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING, null=True, blank=True)
    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username}"


class Patient_Records(models.Model):

    record_id = models.CharField(max_length=50, unique = True)
    patient_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="patients")
    created_date = models.DateField(auto_now=True)
    diagnostics = models.TextField()
    observations = models.TextField()
    treatments = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    misc = models.TextField(null=True,blank=True)
    doctor_name = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='doctors', null=True, blank=True)


    def __str__(self):
        return f"{self.record_id} - {str(self.patient_id.username)}"