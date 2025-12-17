from django.contrib import admin
from .models import Seminar, SeminarRegistration

class RegistrationInline(admin.TabularInline):
    model = SeminarRegistration
    extra = 0
    readonly_fields = ('total_amount', 'payment_status', 'reference')
    can_delete = False

@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'registration_fee', 'is_active')
    inlines = [RegistrationInline]

@admin.register(SeminarRegistration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'seminar', 'participant_type', 'origin', 'total_amount', 'payment_status')
    list_filter = ('seminar', 'payment_status', 'origin', 'needs_accommodation')
    search_fields = ('full_name', 'email', 'reference')