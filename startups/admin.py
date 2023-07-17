from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
import openpyxl
from import_export import resources
from django.http import HttpResponse

# Register your models here.

from .models import Profile, Grievance, Request, Post, Category, Tag
from django.contrib.auth.admin import UserAdmin


def export_selected_objects(modeladmin, request, queryset):
    # Get all field names for the model
    fields = ['email','username', 'is_paid' ,'state','district','startup_idea','startup_type','startup_name','is_registered','is_accepted','is_validated','is_investor','registered_address','area_of_operation', 'pan_no', 'tan_no','officer_authorized', 'designation','service_tax_no',]

    # Create a new workbook and get the active sheet
    wb = openpyxl.Workbook()
    sheet = wb.active

    # Write the header row
    sheet.append(fields)

    # Write data rows
    for obj in queryset:
        row = [getattr(obj, field) for field in fields]
        sheet.append(row)

    # Create a response object with Excel content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="exported_objects.xlsx"'

    # Save the workbook to the response
    wb.save(response)

    return response

admin.site.add_action(export_selected_objects)

class ProfileAdmin(UserAdmin):
    list_display = ('username','startup_name','email', 'is_paid','is_validated', 'is_investor','phone', 'pan_no', 'tan_no', 'service_tax_no')
    search_fields = ('username', 'email','startup_name')
    readonly_fields = ('date_joined', 'last_login','startup_name','username', 'email')
    filter_horizontal = ()
    list_filter = ('is_validated','is_accepted','is_paid','is_registered','is_investor')
    fieldsets = ()
    actions = [export_selected_objects,'validate_users']
    actions_description = "Export selected objects"
    actions_selection_counter = True

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile

admin.site.register(Profile, ProfileAdmin)

@admin.register(Post)
class CustomPostAdmin(UserAdmin):
    list_display = ('id','author', 'category', 'date')
    search_fields = ('id','author', 'title', 'category','tags')
    ordering = ['-id']
    readonly_fields = ('username','author','id')
    filter_horizontal = ()
    list_filter = ('author','category','tags')
    fieldsets = ()
    actions = [export_selected_objects]
    actions_description = "Export selected objects"
    actions_selection_counter = True

admin.site.register(Category)
admin.site.register(Tag)

@admin.register(Request)
class CustomRequestAdmin(UserAdmin):
    list_display = ('id','username', 'status', 'created_at')
    search_fields = ('id','username', 'status')
    ordering = ['-id']
    readonly_fields = ('username','id')
    filter_horizontal = ()
    list_filter = ('status','username')
    fieldsets = ()
    actions = [export_selected_objects]
    actions_description = "Export selected objects"
    actions_selection_counter = True


@admin.register(Grievance)
class CustomGrievanceAdmin(UserAdmin):
    list_display = ('username', 'email', 'complain_date', 'phone', 'complain_type', 'complain_startup', 'complainXfeedback')
    search_fields = ('username', 'email', 'complain_type', 'complain_startup')
    ordering = ['username']  # Update with a valid field name from the Grievance model
    readonly_fields = ('username',)  # Update with valid fields from the Grievance model
    filter_horizontal = ()
    list_filter = ('complain_type', 'complain_startup')
    fieldsets = ()
    actions = [export_selected_objects]
    actions_description = "Export selected objects"
    actions_selection_counter = True



