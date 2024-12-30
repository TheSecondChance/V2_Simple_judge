from django.utils import timezone
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.urls import reverse

PHONE_REGEX = r"^251(7|9)\d{8}"

    
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email fields must be set")
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin): 
    phone_validation = RegexValidator(
        regex=PHONE_REGEX,
        message="Phone Number Not Correct"
    )

    email = models.EmailField(unique=True, max_length=255)
    phone_number = models.CharField(max_length=12, unique=True, validators=[phone_validation],
                                    help_text="12 digit character should start with 251 followed by 7 or 9")
    company_name = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    middle_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    gender = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    country = models.CharField(max_length=40, null=True, blank=True)
    register_date = models.DateTimeField(default=timezone.now)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_employer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'is_employer','is_employee',
                       'first_name', 'last_name', 'middle_name', 'gender',
                       'city', 'country', 'company_name']

    
    def __str__(self):
        return f"{self.first_name} | {self.email}"


class EmployerManager(BaseUserManager): 
    def get_queryset(self):
        return super().get_queryset().filter(is_employer=True)

class Employer(User):
    objects = EmployerManager()  
    
    class Meta:
        proxy = True  
        verbose_name = "Employer"
        verbose_name_plural = "Employers"


class JobTitle(models.Model):
    title = models.CharField(max_length=255)
    apply_form_url = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    requirement = models.TextField()
    deadline = models.CharField(max_length=20)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class EmployeeManager(BaseUserManager): 
    def get_queryset(self):
        return super().get_queryset().filter(is_employee=True)

class Employee(User):
    objects = EmployeeManager()

    class Meta:
        proxy = True  
        verbose_name = "Employee"
        verbose_name_plural = "Employees"


class JobApplication(models.Model):
    # employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')

    is_pending = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} applied for {self.job}"