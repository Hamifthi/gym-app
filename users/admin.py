from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import PersonCreationForm, PersonChangeForm
from .models import Person, Coach, Athlete, Day

@admin.register(Person)
class PersonAdmin(UserAdmin):
    add_form = PersonCreationForm
    form = PersonChangeForm
    model = Person
    list_display = ('email', 'name', 'last_name', 'is_staff')
    list_filter = ('email', 'is_staff', 'is_active')
    fieldsets = (
        ('Personal_Info', {'fields': ('name', 'last_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        ('Credentials', {
            'classes': ('wide',),
            'fields': ('name', 'last_name', 'email', 'password1', 'password2',
            'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('id',)

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        number_of_days = Day.objects.count()
        if number_of_days >= 7:
            return False
        else:
            return True

# Register your models here.
admin.site.register(Coach)
admin.site.register(Athlete)