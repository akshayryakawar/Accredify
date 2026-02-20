from django.db import models

class EnrolmentRatio(models.Model):
    academic_year = models.CharField(max_length=9)  # e.g. 2018-19

    sanctioned_intake = models.IntegerField()  # N
    first_year_admitted = models.IntegerField()  # N1
    lateral_entry = models.IntegerField(default=0)  # N2
    separate_division = models.IntegerField(default=0)  # N3

    total_admitted = models.IntegerField(editable=False)
    enrolment_ratio = models.FloatField(editable=False)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto calculation
        self.total_admitted = (
            self.first_year_admitted
            + self.lateral_entry
            + self.separate_division
        )

        if self.sanctioned_intake > 0:
            self.enrolment_ratio = (
                self.first_year_admitted / self.sanctioned_intake
            ) * 100
        else:
            self.enrolment_ratio = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return self.academic_year
    
#4.1.1
class EnrolmentRatio4_1_1(models.Model):
    # Year label (optional)
    year_label = models.CharField(max_length=50, default="CAY (2023-24)")

    # CAY values
    N1 = models.IntegerField(default=0)
    N2 = models.IntegerField(default=0)
    N  = models.IntegerField(default=0)

    # CAY m1 values
    N1_m1 = models.IntegerField(default=0)
    N2_m1 = models.IntegerField(default=0)
    N_m1  = models.IntegerField(default=0)

    # CAY m2 values
    N1_m2 = models.IntegerField(default=0)
    N2_m2 = models.IntegerField(default=0)
    N_m2  = models.IntegerField(default=0)

    def __str__(self):
        return "Table 4.1.1 Average Enrolment Ratio"  

#4.1.2
from django.db import models

class EnrolmentRatioMarksOnly4_1_2(models.Model):
    marks_90 = models.IntegerField(default=20)   # >=90%
    marks_80 = models.IntegerField(default=18)   # >=80%
    marks_70 = models.IntegerField(default=16)   # >=70%
    marks_60 = models.IntegerField(default=12)   # >=60%
    marks_50 = models.IntegerField(default=8)    # >=50%
    marks_below_50 = models.IntegerField(default=0)  # <50%

    def __str__(self):
        return "Table 4.1.2 Marks"
  

#4.2
class SuccessRateStipulatedPeriod(models.Model):
    year_of_entry = models.CharField(max_length=20)   # Example: 2018-19
    n1_n2_n3_total = models.IntegerField()

    passed_year_1 = models.IntegerField(null=True, blank=True)
    passed_year_2 = models.IntegerField(null=True, blank=True)
    passed_year_3 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.year_of_entry

#4.3    
class studentspassedwithbacklogs(models.Model):
    year_of_entry = models.CharField(max_length=20)   # Example: 2018-19
    n1_n2_n3_total = models.IntegerField()

    passed_year_1 = models.IntegerField(null=True, blank=True)
    passed_year_2 = models.IntegerField(null=True, blank=True)
    passed_year_3 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.year_of_entry
    
#4.3.1
from django.db import models


class AcademicPerformance4_3_1(models.Model):

    year_label = models.CharField(max_length=50, unique=True)
    year = models.IntegerField(null=True, blank=True)

    X = models.FloatField(default=0)
    Y = models.IntegerField(default=0)
    Z = models.IntegerField(default=0)

    # ---------- API ----------
    @property
    def API(self):
        if self.Z == 0:
            return 0
        return round(self.X * (self.Y / self.Z), 2)

    # ---------- LAST 3 RECORDS ----------
    @staticmethod
    def last_three_records():
        return AcademicPerformance4_3_1.objects.exclude(
            year=None
        ).order_by("-year")[:3]

    # ---------- AVERAGE API ----------
    @property
    def average_api(self):
        records = AcademicPerformance4_3_1.last_three_records()

        if len(records) < 3:
            return 0

        return round(sum(r.API for r in records) / 3, 2)

    # ---------- PERFORMANCE LEVEL ----------
    @property
    def academic_performance_level(self):
        return round(2.5 * self.average_api, 2)

    def __str__(self):
        return self.year_label




 #4.6
class PlacementandHigherStudies(models.Model):

    year_label = models.CharField(max_length=50, unique=True)

    # Data fields
    N = models.IntegerField(default=0)
    X = models.IntegerField(default=0)
    Y = models.IntegerField(default=0)
    Z = models.IntegerField(default=0)

    # ---------- Placement Index ----------
    @property
    def P(self):
        if self.N == 0:
            return 0
        return round(((1.25*self.X)+self.Y+self.Z)/self.N,2)

    # ---------- Fetch last 3 year P values ----------
    @staticmethod
    def last_three_records():
        return PlacementandHigherStudies.objects.order_by("-id")[:3]

    @staticmethod
    def get_P_values():
        records = PlacementandHigherStudies.last_three_records()

        if len(records) < 3:
            return (0,0,0)

        return (records[0].P, records[1].P, records[2].P)

    # ---------- Average Placement ----------
    @property
    def average_placement(self):
        P1,P2,P3 = PlacementandHigherStudies.get_P_values()
        return round((P1+P2+P3)/3,2)

    # ---------- Assessment ----------
    @property
    def assessment(self):
        return round(40*self.average_placement,2)

    def __str__(self):
        return self.year_label
    
 #4.6.a
from django.db import models


class PlacementRecord(models.Model):

    assessment_year = models.CharField(max_length=50)
    # Example:
    # 2022-23 (CAYm1)
    # 2023-24 (CAY)
    # You type manually in admin

    student_name = models.CharField(max_length=200)
    enrollment_no = models.CharField(max_length=20)

    employer_name = models.CharField(max_length=200)
    appointment_no = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student_name} - {self.assessment_year}"
   

#4.4.1
from django.db import models

class AcademicPerformance(models.Model):

    year_label = models.CharField(max_length=50, unique=True)

    # ---- Table Fields ----
    X = models.FloatField(default=0)   # Mean CGPA / %
    Y = models.IntegerField(default=0) # Successful students
    Z = models.IntegerField(default=0) # Appeared students

    # ---------- API ----------
    @property
    def api(self):
        if self.Z == 0:
            return 0
        return round(self.X * (self.Y / self.Z), 2)

    # ---------- Last 3 records ----------
    @staticmethod
    def last_three_records():
        return AcademicPerformance.objects.order_by("-id")[:3]

    @staticmethod
    def get_api_values():
        records = AcademicPerformance.last_three_records()

        if len(records) < 3:
            return (0,0,0)

        return (records[0].api, records[1].api, records[2].api)

    # ---------- Average API ----------
    @property
    def average_api(self):
        a1,a2,a3 = AcademicPerformance.get_api_values()
        return round((a1+a2+a3)/3, 2)

    # ---------- Academic Performance Level ----------
    @property
    def academic_performance_level(self):
        return round(2 * self.average_api, 2)

    def __str__(self):
        return self.year_label

#4.2.2
from django.db import models
from django.db.models import Avg


# =========================================
# TABLE 4.2.1 — WITHOUT BACKLOGS
# =========================================
class SuccessRate(models.Model):

    year_label = models.CharField(max_length=20, unique=True)

    # Data
    X = models.IntegerField(default=0)  # Total students
    Y = models.IntegerField(default=0)  # Passed without backlog

    # ---------- Success Index ----------
    @property
    def SI(self):
        if self.X == 0:
            return 0
        return round(self.Y / self.X, 2)

    # ---------- Average of last 3 years ----------
    @classmethod
    def last_three_avg_si(cls):
        last3 = cls.objects.all().order_by("-year_label")[:3]

        if not last3:
            return 0

        avg = sum([obj.SI for obj in last3]) / len(last3)
        return round(avg, 2)

    @property
    def avg_si(self):
        return self.last_three_avg_si()

    # ---------- Success Rate ----------
    @property
    def success_rate(self):
        return round(20 * self.avg_si, 2)  # NBA formula

    def __str__(self):
        return self.year_label


# =========================================
# TABLE 4.2.2 — WITH BACKLOGS
# =========================================
class SuccessRateWithBacklogs(models.Model):

    year_label = models.CharField(max_length=20, unique=True)

    # Data
    X = models.IntegerField(default=0)  # Total students
    Y = models.IntegerField(default=0)  # Passed with backlog

    # ---------- Success Index ----------
    @property
    def SI(self):
        if self.X == 0:
            return 0
        return round(self.Y / self.X, 2)

    # ---------- Average of last 3 years ----------
    @classmethod
    def last_three_avg_si(cls):
        last3 = cls.objects.all().order_by("-year_label")[:3]

        if not last3:
            return 0

        avg = sum([obj.SI for obj in last3]) / len(last3)
        return round(avg, 2)

    @property
    def avg_si(self):
        return self.last_three_avg_si()

    # ---------- Success Rate ----------
    @property
    def success_rate(self):
        return round(20 * self.avg_si, 2)  # NBA formula

    def __str__(self):
        return self.year_label

#4.7
from django.db import models


class ProfessionalActivity(models.Model):

    assessment_year = models.CharField(max_length=50)

    date = models.DateField()

    event_name = models.CharField(max_length=300)

    details = models.TextField()

    professional_society = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.event_name} - {self.assessment_year}"

