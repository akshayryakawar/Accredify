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
from .views import publication_pdf
from .views import participation_4_7_3_pdf
from .views import academic451_pdf
from .views import dashboard
from .views import overview
from .views import about
from .views import global_search

urlpatterns = [
    path("", criterion4_home, name="criterion4_home"),
    path("4-1-enrolment-ratio/", enrolment_ratio_pdf, name="enrolment_ratio_pdf"),
    path("enrolment_ratio_pdf_4_1/", enrolment_ratio_pdf_4_1, name="enrolment_ratio_pdf_4_1"),
    path("4-2-success-rate-no-backlog/", success_rate_nobacklog_pdf, name="success_rate_nobacklog_pdf"),
    path("4-3-success-rate-no-backlog/", students_passed_with_backlogs_pdf, name="students_passed_with_backlogs_pdf"),
    path("4-3-1-academic_performance_pdf_4_3_1/", academic_performance_pdf_4_3_1, name="academic_performance_pdf_4_3_1"),
    path("4-6-placement_higher_studies/", placement_higher_studies_pdf, name="placement_higher_studies_pdf"),
    path("4-6-a- placement/", placement_pdf, name="placement_pdf"),
    path("4-4-academic_performance/", academic_performance_pdf, name="academic_performance_pdf"),
    path("4-2-2-success_rate_combined/", success_rate_combined_pdf, name="success_rate_combined_pdf"),
    path("4-7-professional_activity/", professional_activity_pdf, name="professional_activity_pdf"),
    path("4-7-2-publication-pdf/", publication_pdf, name="publication_pdf"),
    path("4-7-3-participation-pdf/", participation_4_7_3_pdf, name="participation_4_7_3_pdf"),
    path("academic451/pdf/", academic451_pdf, name="academic451_pdf"),
    path("dashboard/", dashboard, name="dashboard"),
    path("overview/", overview, name="overview"),
    path("about/", about, name="about"),
    path("search/", global_search, name="global_search"),
]

# 4.1
from .views import enrolment_ratio_list, enrolment_ratio_add
from .views import enrolment_ratio_edit, enrolment_ratio_delete

urlpatterns += [
    path("enrolment/list/", enrolment_ratio_list, name="enrolment_ratio_list"),
    path("enrolment/add/", enrolment_ratio_add, name="enrolment_ratio_add"),
    path("enrolment/edit/<int:id>/", enrolment_ratio_edit, name="enrolment_ratio_edit"),
    path("enrolment/delete/<int:id>/", enrolment_ratio_delete, name="enrolment_ratio_delete"),
]

#4.1.1
from .views import (
    enrolment_ratio_411_list,
    enrolment_ratio_411_add,
    enrolment_ratio_411_edit,
    enrolment_ratio_411_delete,
)

urlpatterns += [
    path("enrolment411/list/", enrolment_ratio_411_list, name="enrolment_ratio_411_list"),
    path("enrolment411/add/", enrolment_ratio_411_add, name="enrolment_ratio_411_add"),
    path("enrolment411/edit/<int:id>/", enrolment_ratio_411_edit, name="enrolment_ratio_411_edit"),
    path("enrolment411/delete/<int:id>/", enrolment_ratio_411_delete, name="enrolment_ratio_411_delete"),
]

#4.1.2
from .views import (
    enrolment_ratio_412_list,
    enrolment_ratio_412_add,
    enrolment_ratio_412_edit,
    enrolment_ratio_412_delete,
)

urlpatterns += [
    path("enrolment412/list/", enrolment_ratio_412_list, name="enrolment_ratio_412_list"),
    path("enrolment412/add/", enrolment_ratio_412_add, name="enrolment_ratio_412_add"),
    path("enrolment412/edit/<int:id>/", enrolment_ratio_412_edit, name="enrolment_ratio_412_edit"),
    path("enrolment412/delete/<int:id>/", enrolment_ratio_412_delete, name="enrolment_ratio_412_delete"),
]

#4.7.3
from .views import participation_list, participation_add
from .views import participation_edit, participation_delete

urlpatterns += [
    path("participation/list/", participation_list, name="participation_list"),
    path("participation/add/", participation_add, name="participation_add"),
    path("participation/edit/<int:id>/", participation_edit, name="participation_edit"),
    path("participation/delete/<int:id>/", participation_delete, name="participation_delete"),
]

#4.7.3
from .views import professional_activity_list, professional_activity_add
from .views import professional_activity_edit, professional_activity_delete

urlpatterns += [
    path("professional/list/", professional_activity_list, name="professional_activity_list"),
    path("professional/add/", professional_activity_add, name="professional_activity_add"),
    path("professional/edit/<int:id>/", professional_activity_edit, name="professional_activity_edit"),
    path("professional/delete/<int:id>/", professional_activity_delete, name="professional_activity_delete"),
]

#4.2
from .views import (
    success_rate_stipulated_list,
    success_rate_stipulated_add,
    success_rate_stipulated_edit,
    success_rate_stipulated_delete,
)

urlpatterns += [
    path("successrate/list/", success_rate_stipulated_list, name="success_rate_stipulated_list"),
    path("successrate/add/", success_rate_stipulated_add, name="success_rate_stipulated_add"),
    path("successrate/edit/<int:id>/", success_rate_stipulated_edit, name="success_rate_stipulated_edit"),
    path("successrate/delete/<int:id>/", success_rate_stipulated_delete, name="success_rate_stipulated_delete"),
]

#4.2.1 and 4.2.2
from .views import (
    success_rate_list,
    success_rate_add,
    success_rate_edit,
    success_rate_delete,
    success_rate_backlog_list,
    success_rate_backlog_add,
    success_rate_backlog_edit,
    success_rate_backlog_delete,
)

urlpatterns += [
    path("success421/list/", success_rate_list, name="success_rate_list"),
    path("success421/add/", success_rate_add, name="success_rate_add"),
    path("success421/edit/<int:id>/", success_rate_edit, name="success_rate_edit"),
    path("success421/delete/<int:id>/", success_rate_delete, name="success_rate_delete"),
]

urlpatterns += [
    path("success422/list/", success_rate_backlog_list, name="success_rate_backlog_list"),
    path("success422/add/", success_rate_backlog_add, name="success_rate_backlog_add"),
    path("success422/edit/<int:id>/", success_rate_backlog_edit, name="success_rate_backlog_edit"),
    path("success422/delete/<int:id>/", success_rate_backlog_delete, name="success_rate_backlog_delete"),
]

#4.3
from .views import (
    backlog_list,
    backlog_add,
    backlog_edit,
    backlog_delete,
)

urlpatterns += [
    path("backlog43/list/", backlog_list, name="backlog_list"),
    path("backlog43/add/", backlog_add, name="backlog_add"),
    path("backlog43/edit/<int:id>/", backlog_edit, name="backlog_edit"),
    path("backlog43/delete/<int:id>/", backlog_delete, name="backlog_delete"),
]

#4.3.1
from .views import (
    academic431_list,
    academic431_add,
    academic431_edit,
    academic431_delete,
)

urlpatterns += [
    path("academic431/list/", academic431_list, name="academic431_list"),
    path("academic431/add/", academic431_add, name="academic431_add"),
    path("academic431/edit/<int:id>/", academic431_edit, name="academic431_edit"),
    path("academic431/delete/<int:id>/", academic431_delete, name="academic431_delete"),
]

#4.4.1
from .views import (
    second_year_list,
    second_year_add,
    second_year_edit,
    second_year_delete,
)

urlpatterns += [
    path("academic44/list/", second_year_list, name="second_year_list"),
    path("academic44/add/", second_year_add, name="second_year_add"),
    path("academic44/edit/<int:id>/", second_year_edit, name="second_year_edit"),
    path("academic44/delete/<int:id>/", second_year_delete, name="second_year_delete"),
]

#4.5
from .views import academic451_list1, academic451_add1,  academic451_edit1,academic451_delete1

urlpatterns += [
    path("academic451/list/", academic451_list1, name="academic451_list1"),
    path("academic451/add/", academic451_add1, name="academic451_add1"),
    path("academic451/edit/<int:id>/", academic451_edit1, name="academic451_edit1"),
    path("academic451/delete/<int:id>/", academic451_delete1, name="academic451_delete1"),
]

#4.6
from .views import placement_list, placement_add, placement_edit, placement_delete

urlpatterns += [
    path("4-6-placement/", placement_list, name="placement_list"),
    path("4-6-placement/add/", placement_add, name="placement_add"),
    path("4-6-placement/edit/<int:id>/", placement_edit, name="placement_edit"),
    path("4-6-placement/delete/<int:id>/", placement_delete, name="placement_delete"),
]


#4.6.a
from .views import placement_list1, placement_add1, placement_edit1, placement_delete1

urlpatterns += [
    path("placement46a/list/", placement_list1, name="placement_list1"),
    path("placement46a/add/", placement_add1, name="placement_add1"),
    path("placement46a/edit/<int:id>/", placement_edit1, name="placement_edit1"),
    path("placement46a/delete/<int:id>/", placement_delete1, name="placement_delete1"),
]

#4.72
from .views import publication_list1, publication_add1, publication_edit1, publication_delete1

urlpatterns += [
    path("publication472/list/", publication_list1, name="publication_list1"),
    path("publication472/add/", publication_add1, name="publication_add1"),
    path("publication472/edit/<int:id>/", publication_edit1, name="publication_edit1"),
    path("publication472/delete/<int:id>/", publication_delete1, name="publication_delete1"),
]
