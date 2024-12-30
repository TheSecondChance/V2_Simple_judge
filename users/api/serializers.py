from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from users.models import Employer, Employee, JobTitle, JobApplication
from rest_framework.serializers import BooleanField

# from djoser.serializers import UserCreateSerializer
# from rest_framework import serializers


# # class UserSerializer(ModelSerializer):
# #     class Meta:
# #         model = User
# #         fields = ['id', 'email', 'phone_number', 'password', 're_password', 'role', 'is_active', 'is_staff', 'is_superuser']




class EmployerSerializer(ModelSerializer):
    is_employer = serializers.BooleanField(read_only=True)

    class Meta:
        model = Employer
        fields = ['id', 'email', 'phone_number', 'company_name', 'is_employer']

class EmployeeSerializer(ModelSerializer):
    is_employee = serializers.BooleanField(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'email', 'phone_number', 'first_name', 'middle_name',
                  'last_name', 'is_employee', 'gender', 'city', 'country']

class JobTitleSerializer(ModelSerializer):
    application_count = serializers.IntegerField(read_only=True)
    list_application_per_job = serializers.SerializerMethodField()
    apply_form_url = serializers.CharField(read_only=True)

    class Meta:
        model = JobTitle
        fields = ['id', 'title', 'description', 'requirement',
                  'deadline', 'apply_form_url',
                  'application_count', 'list_application_per_job']
        
    def get_list_application_per_job(self, obj):
        return f"http://127.0.0.1:8000/api/application/list?job_id={obj.id}"

class EmployeeJobListSerializer(ModelSerializer):
    application_count = serializers.IntegerField(read_only=True)
    apply_form_url = serializers.CharField(read_only=True)

    class Meta:
        model = JobTitle
        fields = ['id', 'title', 'deadline', 
                  'description', 'requirement',
                  'application_count', 'apply_form_url']

class JobApplicationUpdateSerializer(ModelSerializer):
    is_pending = BooleanField(required=True)
    is_approved = BooleanField(required=True)
    is_rejected = BooleanField(required=True)

    class Meta:
        model = JobApplication
        fields = ['is_pending', 'is_approved', 'is_rejected']

class JobApplicationSerializer(ModelSerializer):
 
    # job = JobTitleSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)
    status_update_url = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = ['id', 'employee', 'resume', 'is_pending',
                  'is_approved', 'is_rejected', 'status_update_url']
    
    def get_status_update_url(self, obj):
        return f"http://127.0.0.1:8000/api/application/update/{obj.id}/"

class PostJobApplicationSerializer(ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['resume']

    def create(self, validated_data):
        return JobApplication.objects.create(**validated_data)



from djoser import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(serializers.UserCreateSerializer):
    class Meta(serializers.UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'company_name', 'first_name', 'middle_name', 'last_name', 'gender', 'city', 'country',
                  'register_date', 'is_employer', 'password')



