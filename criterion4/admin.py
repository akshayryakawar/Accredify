from django.contrib import admin
from .models import EnrolmentRatio
from .models import SuccessRateStipulatedPeriod

@admin.register(EnrolmentRatio)
class EnrolmentRatioAdmin(admin.ModelAdmin):
    list_display = (
        'academic_year',
        'sanctioned_intake',
        'first_year_admitted',
        'lateral_entry',
        'separate_division',
        'total_admitted',
        'enrolment_ratio',
    )

@admin.register(SuccessRateStipulatedPeriod)
class SuccessRateStipulatedPeriodAdmin(admin.ModelAdmin):
    list_display = (
        "year_of_entry", 
        "n1_n2_n3_total",
        "passed_year_1", 
        "passed_year_2", 
        "passed_year_3"
                    )