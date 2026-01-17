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
class SuccessRateStipulatedPeriod(models.Model):
    year_of_entry = models.CharField(max_length=20)   # Example: 2018-19
    n1_n2_n3_total = models.IntegerField()

    passed_year_1 = models.IntegerField(null=True, blank=True)
    passed_year_2 = models.IntegerField(null=True, blank=True)
    passed_year_3 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.year_of_entry