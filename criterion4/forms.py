#4.1
from django import forms
from .models import EnrolmentRatio

class EnrolmentRatioForm(forms.ModelForm):
    class Meta:
        model = EnrolmentRatio
        fields = "__all__"

#4.1.1
from .models import EnrolmentRatio4_1_1

class EnrolmentRatio411Form(forms.ModelForm):
    class Meta:
        model = EnrolmentRatio4_1_1
        fields = "__all__"        

#4.1.2
from .models import EnrolmentRatioMarksOnly4_1_2

class EnrolmentRatio412Form(forms.ModelForm):
    class Meta:
        model = EnrolmentRatioMarksOnly4_1_2
        fields = "__all__"



#4.2
from .models import SuccessRateStipulatedPeriod

class SuccessRateStipulatedPeriodForm(forms.ModelForm):
    class Meta:
        model = SuccessRateStipulatedPeriod
        fields = "__all__"        

#4.2.1 and #4.2.2
from .models import SuccessRate, SuccessRateWithBacklogs


class SuccessRateForm(forms.ModelForm):
    class Meta:
        model = SuccessRate
        fields = "__all__"


class SuccessRateWithBacklogsForm(forms.ModelForm):
    class Meta:
        model = SuccessRateWithBacklogs
        fields = "__all__"
 
#4.3
from .models import studentspassedwithbacklogs

class StudentsPassedWithBacklogsForm(forms.ModelForm):
    class Meta:
        model = studentspassedwithbacklogs
        fields = "__all__"

#4.3.1
from .models import AcademicPerformance4_3_1

class AcademicPerformance431Form(forms.ModelForm):
    class Meta:
        model = AcademicPerformance4_3_1
        fields = "__all__"

#4.4.1
from .models import AcademicPerformanceSecondYear
from django import forms

class AcademicPerformanceSecondYearForm(forms.ModelForm):
    class Meta:
        model = AcademicPerformanceSecondYear
        fields = "__all__"

#4.5
from django import forms
from .models import AcademicPerformance4_5_1


class AcademicPerformance451Form(forms.ModelForm):
    class Meta:
        model = AcademicPerformance4_5_1
        fields = "__all__"


#4.6
from django import forms
from .models import PlacementandHigherStudies

class PlacementandHigherStudiesForm(forms.ModelForm):
    class Meta:
        model = PlacementandHigherStudies
        fields = "__all__"

#4.6.a
from .models import PlacementRecord

class PlacementRecordForm(forms.ModelForm):
    class Meta:
        model = PlacementRecord
        fields = "__all__"

#---------------------4.7------------------------------#
#4.7.1
from .models import ProfessionalActivity

class ProfessionalActivityForm(forms.ModelForm):
    class Meta:
        model = ProfessionalActivity
        fields = "__all__"

#4.7.2
from .models import Publication

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = "__all__"                

#4.7.3
from django import forms
from .models import StudentParticipation

class StudentParticipationForm(forms.ModelForm):
    class Meta:
        model = StudentParticipation
        fields = "__all__"        
