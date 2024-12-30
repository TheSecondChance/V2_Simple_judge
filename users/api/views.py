from rest_framework import status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import AllowAny
from users.models import Employer, Employee, JobTitle, JobApplication

from .serializers import (EmployerSerializer, EmployeeSerializer,
                          JobTitleSerializer, JobApplicationSerializer,
                          JobApplicationUpdateSerializer, EmployeeJobListSerializer)
from django.db.models import Count
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView, GenericAPIView
from users.email_notifications import send_approval_email, send_rejection_email

from rest_framework import generics, permissions



class EmployerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      GenericViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer


class EmployeeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      GenericViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# class JobTitleViewSet(ModelViewSet):
#     queryset = JobTitle.objects.all()
#     serializer_class = JobTitleSerializer

#     def perform_create(self, serializer):
#         user = self.request.user

#         if user.is_employee:
#             raise PermissionDenied("Employees are not allowed to post jobs.")
#         if not user.is_employer:
#             raise PermissionDenied("Only employers can submit job posts.")

#         job = serializer.save(employer=user)

#         form = f"http://127.0.0.1:8000/api/apply/{job.id}/"

#         job.generated_form_url = form
#         job.save()
        
#         return Response({
#             'message': 'Job created successfully',
#             'job_id': job.id,
#             'title': job.title,
#             'employer': job.employer.email,
#             'form': job.generated_form_url  
#         }, status=status.HTTP_201_CREATED)


class JobTitleViewSet(ModelViewSet):
    queryset = JobTitle.objects.annotate(application_count=Count('jobapplication'))
    serializer_class = JobTitleSerializer

    def perform_create(self, serializer):
        user = self.request.user

        # Prevent employees from posting jobs
        if user.is_employee:
            raise PermissionDenied("Employees are not allowed to post jobs.")
        if not user.is_employer:
            raise PermissionDenied("Only employers can submit job posts.")

        # Create job and save employer information
        job = serializer.save(employer=user)

        # Automatically generate a submission form URL for the job
        form_url = f"http://127.0.0.1:8000/api/apply/{job.id}/"
        job.generated_form_url = form_url
        job.save()

        # Return a response with job details
        return Response({
            'message': 'Job created successfully',
            'job_id': job.id,
            'title': job.title,
            'employer': job.employer.email,
            'form_url': job.generated_form_url  # Generated form URL
        }, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        # Get the current user
        user = self.request.user

        # If the user is an employer, show only their jobs with the count of applications
        if user.is_employee:
            raise PermissionDenied("Employee can not allowed to get job list.")
        if not user.is_employer:
            raise PermissionDenied("Only Employers can view their job list.")

        return JobTitle.objects.filter(employer=user).annotate(application_count=Count('jobapplication'))

class EmployeeJobListViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = JobTitle.objects.annotate(application_count=Count('jobapplication'))
    serializer_class = EmployeeJobListSerializer

    def get_queryset(self):
        # Get the current user
        user = self.request.user

        # If the user is an employer, show only their jobs with the count of applications
        if user.is_employer:
            raise PermissionDenied("Employer not allowed to get this job list.")
        if not user.is_employee:
            raise PermissionDenied("Only Employee get job list.")
        
        return JobTitle.objects.annotate(application_count=Count('jobapplication'))

        # If the user is not an employer, deny access
        # raise PermissionDenied("Only employers can view their job listings.")


# class JobApplicationViewSet(ModelViewSet):
#     queryset = JobApplication.objects.all()
#     serializer_class = JobApplicationSerializer

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_employer:
#             # Filter job applications based on the employer through the JobTitle model
#             application_list = JobApplication.objects.filter(job__employer=user)
#             return application_list
        
#         raise PermissionDenied("Only employers can view their job applications.")


class JobApplicationListView(ListAPIView):
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_employee:
            raise PermissionDenied("Employees are not allowed to get applications list.")
        if not user.is_employer:
            raise PermissionDenied("Only employers can get applications list.")

        job_id = self.request.query_params.get('job_id')
        
        if job_id:
            return JobApplication.objects.filter(job__id=job_id)
        return JobApplication.objects.none()
        
class ApplicationStatusUpdateViewSet(UpdateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationUpdateSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        print(request.data)

        # Initialize an empty dictionary for modified data
        modifyed_request = {}

        # Safely access 'is_approved' and 'is_rejected' from request.data
        if request.data.get('is_approved') is True:
            # Update fields if approved
            modifyed_request.update({
                "is_approved": True,
                "is_pending": False,
                "is_rejected": False
            })

        elif request.data.get('is_rejected') is True:
            # Update fields if rejected
            modifyed_request.update({
                "is_rejected": True,
                "is_pending": False,
                "is_approved": False
            })
        else:
            modifyed_request.update({
                "is_rejected": False,
                "is_pending": True,
                "is_approved": False
            })


        # Validate and update the instance with the new data
        serializer = self.get_serializer(instance, data=modifyed_request, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Get company name
        company_name = instance.job.employer.company_name

        # Send email notifications based on the application status
        if instance.is_approved:
            send_approval_email(instance.employee, instance.job, company_name)
        elif instance.is_rejected:
            send_rejection_email(instance.employee, instance.job, company_name)

        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import PostJobApplicationSerializer

from rest_framework.exceptions import PermissionDenied



class JobApplicationCreateView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = PostJobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        user = self.request.user
        # Check if the user is an employer or not an employee
        if user.is_employer:
            raise PermissionDenied("Employers are not allowed to submit job applications.")
        if not user.is_employee:
            raise PermissionDenied("Only employees can submit job applications.")

        # Get the job from the URL parameter
        job_id = self.kwargs['job_id']
        job = JobTitle.objects.get(pk=job_id)

        #check if the employee has already submitted
        existing_application = JobApplication.objects.filter(employee=user, job=job).exists()
        if existing_application:
            raise PermissionDenied("You have already submitted an application for this job.")

        # Save the job application with the employee (current user) and the job
        serializer.save(employee=user, job=job)






class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response
        
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response