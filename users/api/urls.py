from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (EmployerViewSet, CustomTokenObtainPairView,
                    CustomTokenRefreshView, CustomTokenVerifyView,
                    LogoutView, EmployeeViewSet, EmployeeJobListViewSet,
                    JobTitleViewSet, JobApplicationCreateView,
                    JobApplicationListView, ApplicationStatusUpdateViewSet)
# EmployeeViewSet, JobTitleViewSet, JobApplicationViewSet,
#                     RegisterEmployeeView)

router = DefaultRouter()
router.register(r'employers', EmployerViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'jobs', JobTitleViewSet)
router.register(r'employee-get-job-list', EmployeeJobListViewSet, 
                basename='employe-get-all-job')
# router.register(r'applications', JobApplicationViewSet)
# router.register(r'job-list', EmployerJobListViewSet,basename='job-list')

urlpatterns = [
    path('', include(router.urls)),
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('jwt/logout/', LogoutView.as_view()),
    # path('register-employee/', RegisterEmployeeView.as_view(), name='register-employee')
    # path('apply/', JobApplicationCreateView.as_view(), name='job-application-create'),
    path('apply/<int:job_id>/', JobApplicationCreateView.as_view(), name='job-application'),
    path('application/list/', JobApplicationListView.as_view(), name='job-application-list'),

    # update 
    path('application/update/<int:pk>/', ApplicationStatusUpdateViewSet.as_view(), name='job-application-update'),

]