from django.urls import path
from .views import criterion4_home, enrolment_ratio_pdf
from .views import enrolment_ratio_pdf_4_1
from .views import success_rate_nobacklog_pdf
from .views import students_passed_with_backlogs_pdf
from .views import placement_higher_studies_pdf
from .views import academic_performance_pdf
from .views import success_rate_combined_pdf
from .views import academic_performance_pdf_4_3_1
from .views import placement_pdf
from .views import professional_activity_pdf

urlpatterns = [
    path("", criterion4_home, name="criterion4_home"),
    path("4-1-enrolment-ratio/", enrolment_ratio_pdf, name="enrolment_ratio_pdf"),
    path("enrolment_ratio_pdf_4_1/", enrolment_ratio_pdf_4_1, name="enrolment_ratio_pdf_4_1"),
    path("4-2-success-rate-no-backlog/", success_rate_nobacklog_pdf, name="success_rate_nobacklog_pdf"),
    path("4-3-success-rate-no-backlog/", students_passed_with_backlogs_pdf, name="students_passed_with_backlogs_pdf"),
    path("4-3-1-academic_performance_pdf_4_3_1/", academic_performance_pdf_4_3_1, name="academic_performance_pdf_4_3_1"),
    path("4-6-placement_higher_studies/", placement_higher_studies_pdf, name="placement_higher_studies_pdf"),
    path("4-6-a- placement/",  placement_pdf, name=" placement_pdf"),
    path("4-4-academic_performance/", academic_performance_pdf, name="academic_performance_pdf"),
    path("4-2-2-success_rate_combined/", success_rate_combined_pdf, name="success_rate_combined_pdf"),
    path("4-7-professional_activity/", professional_activity_pdf, name="professional_activity_pdf"),
]
