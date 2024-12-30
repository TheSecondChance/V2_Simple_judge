from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Employer, Employee, JobTitle, JobApplication

admin.site.site_header = "Simple Form"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'phone_number', 'company_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'phone_number')
    ordering = ('email',)
    search_fields = ('email', 'phone_number')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('phone_number', 'company_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_employer', 'is_employee')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'company_name', 'phone_number', 'is_active', 'is_staff', 'is_employer', 'is_employee')}
        ),
    )

@admin.register(Employee)
class EmployeeAdmin(BaseUserAdmin):

    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'phone_number')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'middle_name', 'last_name', 'phone_number', 'gender', 'city', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_employee')}),
        ('Important dates', {'fields': ('last_login', 'register_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'middle_name', 'last_name', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
    
    readonly_fields = ('register_date',)

@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer')
    search_fields = ('title',)
    list_filter = ('employer',)

@admin.register(Employer)
class EmployerAdmin(BaseUserAdmin):
    list_display = ('email', 'company_name', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'company_name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Company Info', {'fields': ('company_name', 'phone_number',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'company_name', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

    # def get_job_titles(self, obj):
    #     return ", ".join([jt.title for jt in JobTitle.objects.filter(employer=obj)])

    # get_job_titles.short_description = 'Job Titles'


@admin.register(JobApplication)
class JopApplicationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'job', 'resume')
    search_fields = ('employee',)
    list_filter = ('job',)