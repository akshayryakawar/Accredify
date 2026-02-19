from django.contrib import admin
from .models import EnrolmentRatio
from django.contrib import admin


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

#4.1.1
from .models import EnrolmentRatio4_1_1
@admin.register(EnrolmentRatio4_1_1)
class EnrolmentRatioAdmin1(admin.ModelAdmin):
    list_display = (
        "id",
        "total_cay", "ratio_cay",
        "total_m1", "ratio_m1",
        "total_m2", "ratio_m2",
        "average_enrolment",
    )

    # ---------- TOTALS ----------
    def total_cay(self, obj):
        return obj.N1 + obj.N2
    total_cay.short_description = "Total (CAY)"

    def total_m1(self, obj):
        return obj.N1_m1 + obj.N2_m1
    total_m1.short_description = "Total (CAY m1)"

    def total_m2(self, obj):
        return obj.N1_m2 + obj.N2_m2
    total_m2.short_description = "Total (CAY m2)"


    # ---------- RATIOS ----------
    def ratio_cay(self, obj):
        if obj.N == 0:
            return 0
        return round(((obj.N1 + obj.N2) / obj.N) * 100, 2)
    ratio_cay.short_description = "Enrolment Ratio (CAY %)"

    def ratio_m1(self, obj):
        if obj.N_m1 == 0:
            return 0
        return round(((obj.N1_m1 + obj.N2_m1) / obj.N_m1) * 100, 2)
    ratio_m1.short_description = "Enrolment Ratio (m1 %)"

    def ratio_m2(self, obj):
        if obj.N_m2 == 0:
            return 0
        return round(((obj.N1_m2 + obj.N2_m2) / obj.N_m2) * 100, 2)
    ratio_m2.short_description = "Enrolment Ratio (m2 %)"


    # ---------- AVERAGE ----------
    def average_enrolment(self, obj):
        r1 = self.ratio_cay(obj)
        r2 = self.ratio_m1(obj)
        r3 = self.ratio_m2(obj)
        return round((r1 + r2 + r3) / 3, 2)
    average_enrolment.short_description = "Average Enrolment"

#4.1.1
from .models import EnrolmentRatioMarksOnly4_1_2

@admin.register(EnrolmentRatioMarksOnly4_1_2)
class EnrolmentRatioMarksOnlyAdmin(admin.ModelAdmin):
    list_display = (
        "marks_90", "marks_80", "marks_70",
        "marks_60", "marks_50", "marks_below_50"
    )

from .models import SuccessRateStipulatedPeriod
@admin.register(SuccessRateStipulatedPeriod)
class SuccessRateStipulatedPeriodAdmin(admin.ModelAdmin):
    list_display = (
        "year_of_entry", 
        "n1_n2_n3_total",
        "passed_year_1", 
        "passed_year_2", 
        "passed_year_3"
                    )

# ==============================
# 4.3.
# # ==============================
    
from .models import studentspassedwithbacklogs
@admin.register(studentspassedwithbacklogs)
class studentspassedwithbacklogsAdmin(admin.ModelAdmin):
    list_display = (
        "year_of_entry", 
        "n1_n2_n3_total",
        "passed_year_1", 
        "passed_year_2", 
        "passed_year_3"
                    )

# ==============================
# 4.3.1
# # ==============================
from django.contrib import admin
from .models import AcademicPerformance4_3_1


@admin.register(AcademicPerformance4_3_1)
class AcademicPerformanceAdminFY(admin.ModelAdmin):

    list_display = (
        "year_label",
        "X",
        "Y",
        "Z",
        "API",
        "average_api",
        "academic_performance_level",
    )

    search_fields = ("year_label",)
    ordering = ("-year",)

    # Optional: Make calculated fields read-only
    readonly_fields = (
        "API",
        "average_api",
        "academic_performance_level",
    )




#4.6    
from django.contrib import admin
from .models import PlacementandHigherStudies

@admin.register(PlacementandHigherStudies)
class PlacementandHigherStudiesAdmin(admin.ModelAdmin):

    list_display = (
        "year_label",
        "N","X","Y","Z",
        "show_P",
        "show_avg",
        "show_assessment",
    )

    

    def show_P(self,obj):
        return obj.P
    show_P.short_description = "Placement Index (P)"

    def show_avg(self,obj):
        return obj.average_placement
    show_avg.short_description = "Average Placement"

    def show_assessment(self,obj):
        return obj.assessment
    show_assessment.short_description = "Assessment"

#4.4.1
from django.contrib import admin
from .models import AcademicPerformance


@admin.register(AcademicPerformance)
class AcademicPerformanceAdmin(admin.ModelAdmin):

    list_display = (
        "year_label",
        "X",
        "Y",
        "Z",
        "show_api",
        "show_avg_api",
        "show_apl",
    )

    # -------- API --------
    def show_api(self, obj):
        return obj.api
    show_api.short_description = "API"

    # -------- Average API --------
    def show_avg_api(self, obj):
        return obj.average_api
    show_avg_api.short_description = "Average API"

    # -------- Academic Performance Level --------
    def show_apl(self, obj):
        return obj.academic_performance_level
    show_apl.short_description = "Academic Performance Level"


# ==============================
#4.2.2
# ==============================
from django.contrib import admin
from .models import SuccessRate, SuccessRateWithBacklogs
# ==============================
# TABLE 4.2.1 (WITHOUT BACKLOG)
# ==============================
@admin.register(SuccessRate)
class SuccessRateAdmin(admin.ModelAdmin):

    list_display = (
        "year_label",
        "X",
        "Y",
        "get_SI",
        "get_avg",
        "get_rate",
    )

    def get_SI(self, obj):
        return obj.SI
    get_SI.short_description = "Success Index (SI)"

    def get_avg(self, obj):
        return obj.avg_si
    get_avg.short_description = "Average SI"

    def get_rate(self, obj):
        return obj.success_rate
    get_rate.short_description = "Success Rate"


# ==============================
# TABLE 4.2.2 (WITH BACKLOG)
# ==============================
@admin.register(SuccessRateWithBacklogs)
class SuccessRateWithBacklogsAdmin(admin.ModelAdmin):

    list_display = (
        "year_label",
        "X",
        "Y",
        "get_SI",
        "get_avg",
        "get_rate",
    )

    def get_SI(self, obj):
        return obj.SI
    get_SI.short_description = "Success Index (SI)"

    def get_avg(self, obj):
        return obj.avg_si
    get_avg.short_description = "Average SI"

    def get_rate(self, obj):
        return obj.success_rate
    get_rate.short_description = "Success Rate"
