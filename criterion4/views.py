from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from .models import EnrolmentRatio
from .models import EnrolmentRatio4_1_1
from .models import EnrolmentRatioMarksOnly4_1_2
from .models import SuccessRateStipulatedPeriod
from .models import studentspassedwithbacklogs


# ✅ HOME PAGE (Modern Landing Page)
def criterion4_home(request):
    return render(request, "index.html")

def overview(request):
    return render(request, "overview.html")

def about(request):
    return render(request, "about.html")

#search function
# views.py

from django.db.models import Q
from .models import (
    EnrolmentRatio,
    PlacementRecord,
    Publication,
    StudentParticipation,
)

@login_required
def global_search(request):
    query = request.GET.get("q")
    results = {}

    if query:
        results['participation'] = StudentParticipation.objects.filter(
            Q(student_name__icontains=query) |
            Q(type_of_activity__icontains=query) |
            Q(organizing_body__icontains=query) |
            Q(level__icontains=query) |
            Q(assessment_year__icontains=query)
        )

        results['placement'] = PlacementRecord.objects.filter(
            Q(student_name__icontains=query) |
            Q(employer_name__icontains=query)
        )

        results['publication'] = Publication.objects.filter(
            Q(editor_author__icontains=query) |
            Q(publication_description__icontains=query)
        )

    return render(request, "search_results.html", {
        "query": query,
        "results": results
    })

# ✅ PDF GENERATION (Table 4.1 - Enrolment Ratio)
@login_required
@login_required
def enrolment_ratio_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Table_4_1_Intake_Information.pdf"'

    # Set up the document in Landscape
    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------------- TITLE SECTION ----------------
    elements.append(Paragraph("<b>Criterion 4 – Students’ Performance</b>", styles['Title']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Table No. 4.1 : Intake Information</b>", styles['Heading2']))
    elements.append(Spacer(1, 15))

    # ---------------- DATA FETCHING ----------------
    # Fetching last 6 years
    records = list(EnrolmentRatio.objects.order_by('-academic_year')[:6])
    
    # Ensure list is exactly 6 items long to prevent index errors
    while len(records) < 6:
        records.append(None)

    # Helper function to safely get attributes
    def val(index, field):
        if records[index] and hasattr(records[index], field):
            return getattr(records[index], field)
        return "-"

    # ---------------- TABLE DATA STRUCTURE ----------------
    # Row 0 & 1 are headers (Row 1 uses \n for the line break seen in image)
    table_data = [
        ["Item", "Academic Year", "", "", "", "", ""],
        [
            "", 
            "CAY\n(2023-24)", 
            "CAY m1\n(2022-23)", 
            "CAY m2\n(2021-22)", 
            "CAY m3\n(2020-21)", 
            "CAY m4\n(2019-20)", 
            "CAY m5\n(2018-19)"
        ],
        [
            "Sanctioned intake strength of the program (N)",
            val(0, "sanctioned_intake"), val(1, "sanctioned_intake"), val(2, "sanctioned_intake"),
            val(3, "sanctioned_intake"), val(4, "sanctioned_intake"), val(5, "sanctioned_intake")
        ],
        [
            "Students admitted through state level counseling (N1)",
            val(0, "first_year_admitted"), val(1, "first_year_admitted"), val(2, "first_year_admitted"),
            val(3, "first_year_admitted"), val(4, "first_year_admitted"), val(5, "first_year_admitted")
        ],
        [
            "Students admitted through institute level quota (N2)",
            val(0, "lateral_entry"), val(1, "lateral_entry"), val(2, "lateral_entry"),
            val(3, "lateral_entry"), val(4, "lateral_entry"), val(5, "lateral_entry")
        ],
        [
            "Students admitted through lateral entry (N3)",
            val(0, "separate_division"), val(1, "separate_division"), val(2, "separate_division"),
            val(3, "separate_division"), val(4, "separate_division"), val(5, "separate_division")
        ],
        [
            "Total number of students admitted (N1 + N2 + N3)",
            val(0, "total_admitted"), val(1, "total_admitted"), val(2, "total_admitted"),
            val(3, "total_admitted"), val(4, "total_admitted"), val(5, "total_admitted")
        ],
    ]



    # ---------------- TABLE STYLING ----------------
    # Widths: Item column is wider (320), year columns are equal (75 each)
    table = Table(table_data, colWidths=[320, 75, 75, 75, 75, 75, 75])

    style = TableStyle([
        # Merge "Item" vertically
        ('SPAN', (0, 0), (0, 1)),
        # Merge "Academic Year" horizontally across 6 columns
        ('SPAN', (1, 0), (6, 0)),

        # Background Color (matching the Cyan/Light Blue from image)
        ('BACKGROUND', (0, 0), (6, 1), colors.HexColor('#CCFFFF')),
        
        # Grid and Borders
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        
        # Alignment
        ('ALIGN', (0, 0), (-1, 1), 'CENTER'),     # Center headers
        ('ALIGN', (1, 2), (-1, -1), 'CENTER'),    # Center data numbers
        ('ALIGN', (0, 2), (0, -1), 'LEFT'),       # Left align item text
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Font styling
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 1), 10),
        ('FONTSIZE', (0, 2), (-1, -1), 9),
        
        # Padding for readability
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ])
    
    table.setStyle(style)
    elements.append(table)

    footer_text = "<b>Table No. 4.1 : Intake Information </b>"
    elements.append(Paragraph(footer_text, styles['Normal']))

# ---------------- PREVIOUS TABLE ENDS HERE ----------------
    elements.append(Spacer(1, 30)) # Space after the intake table
         
 # ---------------- BUILD PDF ----------------
    doc.build(elements)
    return response

#newwww
from django.shortcuts import render, redirect, get_object_or_404
from .models import EnrolmentRatio
from .forms import EnrolmentRatioForm

# LIST VIEW
@login_required
def enrolment_ratio_list(request):
    data = EnrolmentRatio.objects.all().order_by("-academic_year")
    return render(request, "enrolment/list.html", {"data": data})


# CREATE VIEW
@login_required
def enrolment_ratio_add(request):
    form = EnrolmentRatioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("enrolment_ratio_list")   # ✅ FIXED
    return render(request, "enrolment/form.html", {"form": form})   # ✅ FIXED


# UPDATE VIEW
@login_required
def enrolment_ratio_edit(request, id):
    obj = get_object_or_404(EnrolmentRatio, id=id)
    form = EnrolmentRatioForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("enrolment_ratio_list")
    return render(request, "enrolment/form.html", {"form": form})   # ✅ FIXED


# DELETE VIEW
@login_required
def enrolment_ratio_delete(request, id):
    obj = get_object_or_404(EnrolmentRatio, id=id)
    obj.delete()
    return redirect("enrolment_ratio_list")

#4.1.1 PDF GENERATION
@login_required
def enrolment_ratio_pdf_4_1(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="Table_4_1_1_4_1_2.pdf"'

    # PDF Document Setup
    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------------- TITLE SECTION ----------------
    elements.append(Paragraph("<b>Criterion 4 – Students’ Performance</b>", styles["Title"]))
    elements.append(Spacer(1, 10))

    # ---------------- FORMULA SECTION ----------------
    elements.append(Paragraph("<b>Enrolment Ratio Formula:</b>", styles["Heading3"]))
    elements.append(Spacer(1, 8))

    fraction_table = Table([
        ["Enrolment Ratio =", "(N1 + N2)"],
        ["", ""],
        ["", "N"],
    ], colWidths=[140, 80])

    fraction_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('LINEABOVE', (1, 2), (1, 2), 1, colors.black),
        ('SPAN', (0, 0), (0, 2)),
    ]))

    elements.append(fraction_table)
    elements.append(Spacer(1, 15))

    # ---------------- TABLE 4.1.1 TITLE ----------------
    elements.append(Paragraph("<b>Following Table No. 4.1 shows Average Enrolment Ratio</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    # ---------------- FETCH DATA ----------------
    record = EnrolmentRatio4_1_1.objects.last()

    # ---------------- CALCULATIONS ----------------
    if record:
        total_cay = record.N1 + record.N2
        total_m1 = record.N1_m1 + record.N2_m1
        total_m2 = record.N1_m2 + record.N2_m2

        ratio_cay = round((total_cay / record.N) * 100, 2) if record.N != 0 else 0
        ratio_m1 = round((total_m1 / record.N_m1) * 100, 2) if record.N_m1 != 0 else 0
        ratio_m2 = round((total_m2 / record.N_m2) * 100, 2) if record.N_m2 != 0 else 0

        average_enrolment = round((ratio_cay + ratio_m1 + ratio_m2) / 3, 2)
    else:
        total_cay = total_m1 = total_m2 = "-"
        ratio_cay = ratio_m1 = ratio_m2 = "-"
        average_enrolment = "-"

    # ---------------- TABLE 4.1.1 DATA ----------------
    table_data_4_1_1 = [
        ["Item", "No. of students", "", ""],
        [
            "(Students enrolled at the First Year Level\non average basis during the previous three academic\nyears including the current academic year)",
            "CAY\n(2023-24)",
            "CAY m1\n(2022-23)",
            "CAY m2\n(2021-22)",
        ],
        ["N1", record.N1 if record else "-", record.N1_m1 if record else "-", record.N1_m2 if record else "-"],
        ["N2", record.N2 if record else "-", record.N2_m1 if record else "-", record.N2_m2 if record else "-"],
        ["N",  record.N  if record else "-", record.N_m1  if record else "-", record.N_m2  if record else "-"],
        ["Total (N1+N2)", total_cay, total_m1, total_m2],
        ["Enrolment Ratio  [((N1+N2)/N)*100]", ratio_cay, ratio_m1, ratio_m2],
        ["Average Enrolment", average_enrolment, "", ""],
    ]

    table_4_1_1 = Table(table_data_4_1_1, colWidths=[320, 110, 110, 110])

    style_4_1_1 = TableStyle([
        ('SPAN', (1, 0), (3, 0)),  # Merge "No. of students"

        ('BACKGROUND', (0, 0), (3, 1), colors.HexColor("#CCFFFF")),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('ALIGN', (0, 0), (-1, 1), 'CENTER'),
        ('ALIGN', (1, 2), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 2), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 1), 10),
        ('FONTSIZE', (0, 2), (-1, -1), 9),

        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ])

    table_4_1_1.setStyle(style_4_1_1)
    elements.append(table_4_1_1)

    elements.append(Spacer(1, 8))
    elements.append(Paragraph("<b>Table No. 4.1.1 : Average Enrolment Ratio</b>", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # ---------------- TABLE 4.1.2 TITLE ----------------
    elements.append(Paragraph("<b>Following Table No. 4.1.2 shows Enrolment Ratio.</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    # ---------------- TABLE 4.1.2 DATA FROM ADMIN (ONLY MARKS) ----------------
    marks_obj = EnrolmentRatioMarksOnly4_1_2.objects.last()

    table_4_1_2_data = [
        ["Item\n(Students enrolled at the First Year Level on average basis during the\nprevious three academic years including the current academic year)", "Marks"],
        [">=90% Students", str(marks_obj.marks_90 if marks_obj else 20)],
        [">=80% Students", str(marks_obj.marks_80 if marks_obj else 18)],
        [">=70% Students", str(marks_obj.marks_70 if marks_obj else 16)],
        [">=60% Students", str(marks_obj.marks_60 if marks_obj else 12)],
        [">=50% Students", str(marks_obj.marks_50 if marks_obj else 8)],
        ["<50% Students", str(marks_obj.marks_below_50 if marks_obj else 0)],
    ]

    table_4_1_2 = Table(table_4_1_2_data, colWidths=[520, 120])

    style_4_1_2 = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#CCFFFF")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('FONTSIZE', (0, 0), (-1, -1), 10),

        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ])

    table_4_1_2.setStyle(style_4_1_2)
    elements.append(table_4_1_2)

    elements.append(Spacer(1, 8))
    elements.append(Paragraph("<b>Table No. 4.1.2 : Enrolment Ratio</b>", styles["Normal"]))

    # ---------------- BUILD PDF ----------------
    doc.build(elements)
    return response

##----------4.1.1---------------------##
from .forms import EnrolmentRatio411Form
from django.shortcuts import get_object_or_404

# LIST
@login_required
def enrolment_ratio_411_list(request):
    data = EnrolmentRatio4_1_1.objects.all().order_by("-id")
    return render(request, "enrolment411/list.html", {"data": data})


# ADD
@login_required
def enrolment_ratio_411_add(request):
    form = EnrolmentRatio411Form(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("enrolment_ratio_411_list")
    return render(request, "enrolment411/form.html", {"form": form})


# EDIT
@login_required
def enrolment_ratio_411_edit(request, id):
    obj = get_object_or_404(EnrolmentRatio4_1_1, id=id)
    form = EnrolmentRatio411Form(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("enrolment_ratio_411_list")
    return render(request, "enrolment411/form.html", {"form": form})


# DELETE
@login_required
def enrolment_ratio_411_delete(request, id):
    obj = get_object_or_404(EnrolmentRatio4_1_1, id=id)
    obj.delete()
    return redirect("enrolment_ratio_411_list")

#----------4.1.2------------------------
from .forms import EnrolmentRatio412Form
from django.shortcuts import get_object_or_404

# LIST
@login_required
def enrolment_ratio_412_list(request):
    data = EnrolmentRatioMarksOnly4_1_2.objects.all().order_by("-id")
    return render(request, "enrolment412/list.html", {"data": data})


# ADD
@login_required
def enrolment_ratio_412_add(request):
    form = EnrolmentRatio412Form(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("enrolment_ratio_412_list")
    return render(request, "enrolment412/form.html", {"form": form})


# EDIT
@login_required
def enrolment_ratio_412_edit(request, id):
    obj = get_object_or_404(EnrolmentRatioMarksOnly4_1_2, id=id)
    form = EnrolmentRatio412Form(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("enrolment_ratio_412_list")
    return render(request, "enrolment412/form.html", {"form": form})


# DELETE
@login_required
def enrolment_ratio_412_delete(request, id):
    obj = get_object_or_404(EnrolmentRatioMarksOnly4_1_2, id=id)
    obj.delete()
    return redirect("enrolment_ratio_412_list")

# marks_obj = EnrolmentRatioMarksOnly4_1_2.objects.last()


# ✅ PDF GENERATION (Table 4.2 - Success Rate Without Backlogs)
@login_required
def success_rate_nobacklog_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Table_4_2_No_Backlog.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------------- TITLE ----------------
    elements.append(Paragraph("<b>4.2. Success Rate in the stipulated period of the program</b>", styles["Title"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        "<b>Following Table No. 4.2 Number of students passed without backlogs in stipulated year of study</b>",
        styles["Heading2"]
    ))
    elements.append(Spacer(1, 10))

    # ---------------- FETCH DATA (LAST 6 YEARS) ----------------
    records = list(SuccessRateStipulatedPeriod.objects.all().order_by("-id")[:6])
    records.reverse()  # old to new

    # ---------------- TABLE HEADER ----------------
    table_data = [
        [
            "Year of entry",
            "N1 + N2 + N3\n(As defined above)",
            "Number of students who have successfully\npassed without backlogs in any year of study",
            "",
            ""
        ],
        ["", "", "I Year", "II Year", "III Year"]
    ]

    # ---------------- TABLE ROWS ----------------
    for r in records:
        table_data.append([
            r.year_of_entry,
            r.n1_n2_n3_total,
            r.passed_year_1 if r.passed_year_1 is not None else "-",
            r.passed_year_2 if r.passed_year_2 is not None else "-",
            r.passed_year_3 if r.passed_year_3 is not None else "-",
        ])

    # ---------------- CREATE TABLE ----------------
    table = Table(table_data, colWidths=[170, 120, 150, 150, 150])

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 0), (-1, 1), colors.lightblue),
        ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        # Merge header cells
        ("SPAN", (0, 0), (0, 1)),
        ("SPAN", (1, 0), (1, 1)),
        ("SPAN", (2, 0), (4, 0)),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "<b>Table No. 4.2 : Number of students passed without backlogs in stipulated year of study</b>",
        styles["Heading3"]
    ))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("LYG : Last Year Graduate", styles["Normal"]))
    elements.append(Paragraph("LYG 1 : Last Year Graduate minus 1", styles["Normal"]))
    elements.append(Paragraph("LYG 2 : Last Year Graduate minus 2", styles["Normal"]))

    doc.build(elements)
    return response

#---------------4.2-----------------#
from .forms import SuccessRateStipulatedPeriodForm
from django.shortcuts import get_object_or_404

# LIST
@login_required
def success_rate_stipulated_list(request):
    data = SuccessRateStipulatedPeriod.objects.all().order_by("-id")
    return render(request, "successrate/list.html", {"data": data})


# ADD
@login_required
def success_rate_stipulated_add(request):
    form = SuccessRateStipulatedPeriodForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("success_rate_stipulated_list")
    return render(request, "successrate/form.html", {"form": form})


# EDIT
@login_required
def success_rate_stipulated_edit(request, id):
    obj = get_object_or_404(SuccessRateStipulatedPeriod, id=id)
    form = SuccessRateStipulatedPeriodForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("success_rate_stipulated_list")
    return render(request, "successrate/form.html", {"form": form})


# DELETE
@login_required
def success_rate_stipulated_delete(request, id):
    obj = get_object_or_404(SuccessRateStipulatedPeriod, id=id)
    obj.delete()
    return redirect("success_rate_stipulated_list")

# SuccessRateStipulatedPeriod.objects.all()

# ✅ PDF GENERATION (Table 4.3 - students passed with backlogs )
@login_required
def students_passed_with_backlogs_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Table_4_2_No_Backlog.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------------- TITLE ----------------

    elements.append(Paragraph(
        "<b>Following Table No. 4.3 shows number of students passed with backlogs in stipulated year of study.</b>",
        styles["Heading2"]
    ))
    elements.append(Spacer(1, 10))

    # ---------------- FETCH DATA (LAST 6 YEARS) ----------------
    records = list(studentspassedwithbacklogs.objects.all().order_by("-id")[:6])
    records.reverse()  # old to new

    # ---------------- TABLE HEADER ----------------
    table_data = [
        [
            "Year of entry",
            "N1 + N2 + N3\n(As defined above)",
            "Number of students who have successfully passed\n(Students with backlog in stipulated period of study)",
            "",
            ""
        ],
        ["", "", "I Year", "II Year", "III Year"]
    ]

    # ---------------- TABLE ROWS ----------------
    for r in records:
        table_data.append([
            r.year_of_entry,
            r.n1_n2_n3_total,
            r.passed_year_1 if r.passed_year_1 is not None else "-",
            r.passed_year_2 if r.passed_year_2 is not None else "-",
            r.passed_year_3 if r.passed_year_3 is not None else "-",
        ])

    # ---------------- CREATE TABLE ----------------
    table = Table(table_data, colWidths=[170, 120, 150, 150, 150])

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 0), (-1, 1), colors.lightblue),
        ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        # Merge header cells
        ("SPAN", (0, 0), (0, 1)),
        ("SPAN", (1, 0), (1, 1)),
        ("SPAN", (2, 0), (4, 0)),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "<b>Table No. 4.3 : Number of students passed with backlogs in stipulated year of study</b>",
        styles["Heading3"]
    ))

    doc.build(elements)
    return response

from .forms import StudentsPassedWithBacklogsForm
from .models import studentspassedwithbacklogs
from django.shortcuts import get_object_or_404


# ==========================
# 4.3 Students With Backlogs
# ==========================

@login_required
def backlog_list(request):
    data = studentspassedwithbacklogs.objects.all().order_by("-id")
    return render(request, "backlog43/list.html", {"data": data})


@login_required
def backlog_add(request):
    form = StudentsPassedWithBacklogsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("backlog_list")
    return render(request, "backlog43/form.html", {"form": form})


@login_required
def backlog_edit(request, id):
    obj = get_object_or_404(studentspassedwithbacklogs, id=id)
    form = StudentsPassedWithBacklogsForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("backlog_list")
    return render(request, "backlog43/form.html", {"form": form})


@login_required
def backlog_delete(request, id):
    obj = get_object_or_404(studentspassedwithbacklogs, id=id)
    obj.delete()
    return redirect("backlog_list")

#---------------------------4.3.1------------------------------
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from .models import AcademicPerformance4_3_1


@login_required
def academic_performance_pdf_4_3_1(request):

    from django.http import HttpResponse
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="Table_4_3_1.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("<b>Table No. 4.3.1 : Academic Performance in First Year</b>", styles["Title"])
    )
    elements.append(Spacer(1, 20))

    # -------- Get Last 3 Years ----------
    records = AcademicPerformance4_3_1.last_three_records()

    if len(records) < 3:
        elements.append(Paragraph("Not enough data (Need 3 years).", styles["Normal"]))
        doc.build(elements)
        return response

    r1, r2, r3 = records

    records = AcademicPerformance4_3_1.last_three_records()

    r1, r2, r3 = records


    # -------- Table Data ----------
    table_data = [

        ["Academic Performance", r1.year_label, r2.year_label, r3.year_label],

        ["Mean of CGPA / % (X)", r1.X, r2.X, r3.X],

        ["Total successful students (Y)", r1.Y, r2.Y, r3.Y],

        ["Total appeared (Z)", r1.Z, r2.Z, r3.Z],

        ["API = X × (Y/Z)", r1.API, r2.API, r3.API],

        ["Average API", r1.average_api, "", ""],

        ["Academic Performance Level (2.5 × Avg API)",
         r1.academic_performance_level, "", ""],
    ]

    table = Table(table_data, colWidths=[320, 140, 140, 140])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#CCFFFF")),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('SPAN', (1, 5), (3, 5)),
        ('SPAN', (1, 6), (3, 6)),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))

    elements.append(table)

    doc.build(elements)
    return response

# AcademicPerformance4_3_1.objects.order_by("-year_label")

from .forms import AcademicPerformance431Form
from .models import AcademicPerformance4_3_1
from django.shortcuts import get_object_or_404


# ==========================
# 4.3.1 Academic Performance
# ==========================

@login_required
def academic431_list(request):
    data = AcademicPerformance4_3_1.objects.all().order_by("-year_label")
    
    avg_api = 0
    performance_level = 0

    if data.count() >= 3:
        records = AcademicPerformance4_3_1.last_three_records()
        avg_api = round(sum(r.API for r in records) / 3, 2)
        performance_level = round(2.5 * avg_api, 2)

    return render(request, "academic431/list.html", {
        "data": data,
        "avg_api": avg_api,
        "performance_level": performance_level,
    })


@login_required
def academic431_add(request):
    form = AcademicPerformance431Form(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("academic431_list")
    return render(request, "academic431/form.html", {"form": form})


@login_required
def academic431_edit(request, id):
    obj = get_object_or_404(AcademicPerformance4_3_1, id=id)
    form = AcademicPerformance431Form(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("academic431_list")
    return render(request, "academic431/form.html", {"form": form})


@login_required
def academic431_delete(request, id):
    obj = get_object_or_404(AcademicPerformance4_3_1, id=id)
    obj.delete()
    return redirect("academic431_list")

# AcademicPerformance4_3_1.objects.all()

#4.6
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet

from .models import PlacementandHigherStudies


@login_required
def placement_higher_studies_pdf(request):

    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet
    from django.http import HttpResponse
    from .models import PlacementandHigherStudies

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="placement.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))

    styles = getSampleStyleSheet()

    # ✅ CREATE ELEMENTS FIRST
    elements = []

    # -------- TITLE --------
    elements.append(Paragraph(
        "<b>Table 4.6.1 Placement and Higher Studies</b>",
        styles["Title"]
    ))

    elements.append(Spacer(1,12))

    # -------- YOUR TEXT --------
    elements.append(Paragraph(
        "<b>Assessment Points = 40 × Average Placement</b>",
        styles["Heading2"]
    ))

    elements.append(Spacer(1,8))

    elements.append(Paragraph("Where,", styles["Normal"]))
    elements.append(Paragraph(
        "X = No. of students placed in companies/Government sector",
        styles["Normal"]
    ))
    elements.append(Paragraph(
        "Y = Number of students admitted to higher studies",
        styles["Normal"]
    ))
    elements.append(Paragraph(
        "N = Total number of final year students",
        styles["Normal"]
    ))

    elements.append(Spacer(1,15))

    # -------- FETCH DATA --------
    records = PlacementandHigherStudies.objects.order_by("-id")[:3]

    if len(records) < 3:
        elements.append(Paragraph("Enter 3 records first.", styles["Normal"]))
        doc.build(elements)
        return response

    r1,r2,r3 = records

    P1,P2,P3 = r1.P, r2.P, r3.P
    avg = round((P1+P2+P3)/3,2)
    assess = round(40*avg,2)

    # -------- TABLE --------
    data = [
        ["Item", r1.year_label, r2.year_label, r3.year_label],
        ["N", r1.N, r2.N, r3.N],
        ["X", r1.X, r2.X, r3.X],
        ["Y", r1.Y, r2.Y, r3.Y],
        ["Z", r1.Z, r2.Z, r3.Z],
        ["Placement Index (P)", P1,P2,P3],
        ["Average Placement", avg,"",""],
        ["Assessment", assess,"",""],
    ]

    table = Table(
    data,
    colWidths=[170,110,110,110],   # 👈 column size
    rowHeights=25                 # 👈 row height
)


    table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("BACKGROUND",(0,0),(-1,0),colors.lightblue),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
    ]))

    elements.append(table)

    doc.build(elements)

    return response

from .models import PlacementandHigherStudies
from .forms import PlacementandHigherStudiesForm
from django.shortcuts import render, redirect, get_object_or_404


from django.shortcuts import render, redirect, get_object_or_404

# LIST
@login_required
def placement_list(request):
    data = PlacementandHigherStudies.objects.all().order_by("-id")
    return render(request, "placement/list.html", {"data": data})

# ADD
@login_required
def placement_add(request):
    form = PlacementandHigherStudiesForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("placement_list")
    return render(request, "placement/form.html", {"form": form})

# EDIT
@login_required
def placement_edit(request, id):
    obj = get_object_or_404(PlacementandHigherStudies, id=id)
    form = PlacementandHigherStudiesForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("placement_list")
    return render(request, "placement/form.html", {"form": form})

# DELETE
@login_required
def placement_delete(request, id):
    obj = get_object_or_404(PlacementandHigherStudies, id=id)
    obj.delete()
    return redirect("placement_list")

#4.6.a
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from .models import PlacementRecord


@login_required
def placement_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="placement_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    years = PlacementRecord.objects.values_list(
        "assessment_year", flat=True
    ).distinct()

    for year in years:

        records = PlacementRecord.objects.filter(
            assessment_year=year
        )

        # Heading
        heading = Paragraph(
            f"<b>Assessment Year : {year}</b>",
            styles["Heading2"]
        )
        elements.append(heading)
        elements.append(Spacer(1, 12))

        data = [
            ["Sr. No.", "Student Name", "Enrollment No.", "Employer Name", "Appointment No."]
        ]

        for index, record in enumerate(records, start=1):
            data.append([
                index,
                record.student_name,
                record.enrollment_no,
                record.employer_name,
                record.appointment_no,
            ])

        table = Table(data, repeatRows=1)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))

        elements.append(table)
        elements.append(PageBreak())

    doc.build(elements)
    return response

from .forms import PlacementRecordForm
from .models import PlacementRecord
from django.shortcuts import get_object_or_404


# ==========================
# 4.6.a Placement Records
# ==========================

@login_required
def placement_list1(request):
    data = PlacementRecord.objects.all().order_by("-assessment_year")
    return render(request, "placement46a/list.html", {"data": data})


@login_required
def placement_add1(request):
    form = PlacementRecordForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("placement_list1")
    return render(request, "placement46a/form.html", {"form": form})


@login_required
def placement_edit1(request, id):
    obj = get_object_or_404(PlacementRecord, id=id)
    form = PlacementRecordForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("placement_list1")
    return render(request, "placement46a/form.html", {"form": form})


@login_required
def placement_delete1(request, id):
    obj = get_object_or_404(PlacementRecord, id=id)
    obj.delete()
    return redirect("placement_list1")

# PlacementRecord.objects.filter(assessment_year=...)


#4.4.1
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet

from .models import AcademicPerformanceSecondYear

@login_required
def academic_performance_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="academic_performance.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    elements = []

    # -------- TITLE --------
    elements.append(Paragraph(
        "<b>Table 4.4.1 Academic Performance in Second Year</b>",
        styles["Title"]
    ))
    elements.append(Spacer(1,12))

    # -------- FORMULA TEXT --------
    elements.append(Paragraph(
        "<b>API = X × (Y/Z)</b>",
        styles["Heading2"]
    ))

    elements.append(Paragraph(
        "<b>Academic Performance Level = 2 × Average API</b>",
        styles["Heading2"]
    ))

    elements.append(Spacer(1,10))

    elements.append(Paragraph("Where,", styles["Normal"]))
    elements.append(Paragraph("X = Mean CGPA / Mean Percentage", styles["Normal"]))
    elements.append(Paragraph("Y = Number of successful students", styles["Normal"]))
    elements.append(Paragraph("Z = Number of students appeared", styles["Normal"]))

    elements.append(Spacer(1,15))

    # -------- FETCH LAST 3 YEARS --------
    records = AcademicPerformanceSecondYear.objects.order_by("-id")[:3]

    if len(records) < 3:
        elements.append(Paragraph("Enter 3 records first.", styles["Normal"]))
        doc.build(elements)
        return response

    r1, r2, r3 = records

    # -------- CALCULATIONS --------
    api1, api2, api3 = r1.API, r2.API, r3.API
    avg_api = round((api1 + api2 + api3) / 3, 2)
    apl = round(2 * avg_api, 2)

    # -------- TABLE DATA --------
    data = [
        ["Academic Performance", r1.year_label, r2.year_label, r3.year_label],

        ["Mean CGPA / % (X)", r1.X, r2.X, r3.X],
        ["Successful Students (Y)", r1.Y, r2.Y, r3.Y],
        ["Appeared Students (Z)", r1.Z, r2.Z, r3.Z],

        ["API = X*(Y/Z)", api1, api2, api3],

        ["Average API", avg_api, "", ""],
        ["Academic Performance Level", apl, "", ""],
    ]

    table = Table(
        data,
        colWidths=[220,110,110,110],
        rowHeights=25
    )

    table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("BACKGROUND",(0,0),(-1,0),colors.lightblue),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))

    elements.append(table)

    doc.build(elements)

    return response

from .models import AcademicPerformanceSecondYear
from .forms import AcademicPerformanceSecondYearForm
from django.shortcuts import render, redirect, get_object_or_404


# ==========================
# 4.4 Academic Performance (Second Year)
# ==========================

@login_required
def second_year_list(request):
    data = AcademicPerformanceSecondYear.objects.all().order_by("-year")

    avg_api = 0
    performance_level = 0

    if data.count() >= 3:
        records = AcademicPerformanceSecondYear.last_three_records()
        avg_api = round(sum(r.API for r in records) / 3, 2)
        performance_level = round(2.0 * avg_api, 2)

    return render(request, "academic44/list.html", {
        "data": data,
        "avg_api": avg_api,
        "performance_level": performance_level,
    })


@login_required
def second_year_add(request):
    form = AcademicPerformanceSecondYearForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("second_year_list")
    return render(request, "academic44/form.html", {"form": form})


@login_required
def second_year_edit(request, id):
    obj = get_object_or_404(AcademicPerformanceSecondYear, id=id)
    form = AcademicPerformanceSecondYearForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("second_year_list")
    return render(request, "academic44/form.html", {"form": form})


@login_required
def second_year_delete(request, id):
    obj = get_object_or_404(AcademicPerformanceSecondYear, id=id)
    obj.delete()
    return redirect("second_year_list")
#4.2.1
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet

@login_required
def success_rate_combined_pdf(request):

    from django.http import HttpResponse
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,PageBreak
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet

    from .models import SuccessRate, SuccessRateWithBacklogs

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="Success_Rate.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    elements = []

    
    # =========================
    # TABLE 4.2.1 (NO BACKLOG)
    # =========================

    # ---------------- FORMULA SECTION ----------------
    elements.append(Paragraph("<b>4.2.1. Success rate without backlogs in any year of study (40)</b>", styles["Heading3"]))
    elements.append(Spacer(1, 8))

    fraction_table = Table([
        ["SI  =", "Number of students who have passed from the program without backlog"],
        ["", "________________________________________________________________________________________"],
        ["", "No. of students admitted in the first year of that batch + actual admitted in 2nd year via lateral entry"],
    ], colWidths=[160, 450])

    fraction_table.setStyle(TableStyle([
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
    ]))
   
    # ✅ THIS LINE WAS MISSING
    elements.append(fraction_table)
    elements.append(Paragraph("Average SI = Mean of success index (SI) for past three batches",))
    elements.append(Paragraph("Success rate without backlogs in any year of study =<b> 40 × Average SI</b>",))
    elements.append(Spacer(1,15))

    rec = SuccessRate.objects.order_by("-id")[:3]

    if len(rec) == 3:
        r1,r2,r3 = rec

        data1 = [
            ["Item", r1.year_label, r2.year_label, r3.year_label],
            ["Total students (X)", r1.X, r2.X, r3.X],
            ["Passed (Y)", r1.Y, r2.Y, r3.Y],
            ["Success Index", r1.SI, r2.SI, r3.SI],
            ["Average SI", r1.avg_si,"",""],
            ["Success Rate (40×Avg)", r1.success_rate,"",""],
        ]

        t1 = Table(data1,colWidths=[220,110,110,110],rowHeights=25)
        t1.setStyle(TableStyle([
            ("GRID",(0,0),(-1,-1),1,colors.black),
            ("BACKGROUND",(0,0),(-1,0),colors.lightblue),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ]))

        elements.append(t1)
        elements.append(Paragraph("<b>Table No. 4.2.1 : Success rate without backlogs in any year of study</b>", styles["Heading3"]))
        elements.append(Paragraph("Success rate without backlogs in any year of study	=	40 × Average SI"))
        elements.append(Paragraph("Success rate without backlogs in any year of study	=	40 x 0.26"))
        elements.append(Paragraph("<b>Success Rate	=	10.4</b>"))
    # SPACE BETWEEN TABLES
    elements.append(PageBreak())

    # =========================
    # TABLE 4.2.2 (WITH BACKLOG)
    # =========================

    elements.append(Paragraph(
        "<b>Table 4.2.2 Success rate with backlogs</b>",
        styles["Title"]
    ))
    elements.append(Spacer(1,10))

    rec2 = SuccessRateWithBacklogs.objects.order_by("-id")[:3]

    if len(rec2) == 3:
        r1,r2,r3 = rec2

        data2 = [
            ["Item", r1.year_label, r2.year_label, r3.year_label],
            ["Total students (X)", r1.X, r2.X, r3.X],
            ["Passed (Y)", r1.Y, r2.Y, r3.Y],
            ["Success Index", r1.SI, r2.SI, r3.SI],
            ["Average SI", r1.avg_si,"",""],
            ["Success Rate (20×Avg)", r1.success_rate,"",""],
        ]

        t2 = Table(data2, colWidths=[220,110,110,110],rowHeights=25)
        t2.setStyle(TableStyle([
            ("GRID",(0,0),(-1,-1),1,colors.black),
            ("BACKGROUND",(0,0),(-1,0),colors.lightblue),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ]))

        elements.append(t2)

    doc.build(elements)
    return response

from .forms import SuccessRateForm, SuccessRateWithBacklogsForm
from django.shortcuts import get_object_or_404
from .models import SuccessRate, SuccessRateWithBacklogs

# ==========================
# 4.2.1 – WITHOUT BACKLOG
# ==========================

@login_required
def success_rate_list(request):
    data = SuccessRate.objects.all().order_by("-year_label")
    return render(request, "success421/list.html", {"data": data})


@login_required
def success_rate_add(request):
    form = SuccessRateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("success_rate_list")
    return render(request, "success421/form.html", {"form": form})


@login_required
def success_rate_edit(request, id):
    obj = get_object_or_404(SuccessRate, id=id)
    form = SuccessRateForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("success_rate_list")
    return render(request, "success421/form.html", {"form": form})


@login_required
def success_rate_delete(request, id):
    obj = get_object_or_404(SuccessRate, id=id)
    obj.delete()
    return redirect("success_rate_list")

# ==========================
# 4.2.2 – WITH BACKLOG
# ==========================

@login_required
def success_rate_backlog_list(request):
    data = SuccessRateWithBacklogs.objects.all().order_by("-year_label")
    return render(request, "success422/list.html", {"data": data})


@login_required
def success_rate_backlog_add(request):
    form = SuccessRateWithBacklogsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("success_rate_backlog_list")
    return render(request, "success422/form.html", {"form": form})


@login_required
def success_rate_backlog_edit(request, id):
    obj = get_object_or_404(SuccessRateWithBacklogs, id=id)
    form = SuccessRateWithBacklogsForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("success_rate_backlog_list")
    return render(request, "success422/form.html", {"form": form})


@login_required
def success_rate_backlog_delete(request, id):
    obj = get_object_or_404(SuccessRateWithBacklogs, id=id)
    obj.delete()
    return redirect("success_rate_backlog_list")

#4.7
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from .models import ProfessionalActivity


from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from .models import ProfessionalActivity


@login_required
def professional_activity_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="professional_activities.pdf"'

    doc = SimpleDocTemplate(response, pagesize=pagesizes.A4)
    elements = []

    styles = getSampleStyleSheet()

    # Custom style for wrapping text
    normal_style = ParagraphStyle(
        name='NormalWrap',
        parent=styles['Normal'],
        fontSize=9,
        leading=12
    )

    years = ProfessionalActivity.objects.values_list(
        "assessment_year", flat=True
    ).distinct()

    for year in years:

        records = ProfessionalActivity.objects.filter(
            assessment_year=year
        ).order_by("date")

        # ===== BLUE HEADER BAR =====
        header_data = [[f"{year}"]]

        header_table = Table(header_data, colWidths=[7.5 * inch])
        header_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#A7D3D3")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))

        elements.append(header_table)
        elements.append(Spacer(1, 10))

        # ===== TABLE DATA =====
        data = [
            ["Sr. No.", "Date", "Event Name", "Details", "Professional Society"]
        ]

        for index, record in enumerate(records, start=1):
            data.append([
                index,
                record.date.strftime("%d/%m/%Y"),
                Paragraph(record.event_name, normal_style),
                Paragraph(record.details, normal_style),
                record.professional_society,
            ])

        table = Table(
            data,
            colWidths=[
                0.6 * inch,
                1 * inch,
                2 * inch,
                2.8 * inch,
                1.4 * inch
            ],
            repeatRows=1
        )

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ]))

        

        elements.append(table)
        elements.append(PageBreak())

    doc.build(elements)
    return response

#############
from .forms import ProfessionalActivityForm
from django.shortcuts import get_object_or_404

# LIST
@login_required
def professional_activity_list(request):
    data = ProfessionalActivity.objects.all().order_by("-assessment_year")
    return render(request, "professional/list.html", {"data": data})

# ADD
@login_required
def professional_activity_add(request):
    form = ProfessionalActivityForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("professional_activity_list")
    return render(request, "professional/form.html", {"form": form})

# EDIT
@login_required
def professional_activity_edit(request, id):
    obj = get_object_or_404(ProfessionalActivity, id=id)
    form = ProfessionalActivityForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("professional_activity_list")
    return render(request, "professional/form.html", {"form": form})

# DELETE
@login_required
def professional_activity_delete(request, id):
    obj = get_object_or_404(ProfessionalActivity, id=id)
    obj.delete()
    return redirect("professional_activity_list")

#4.7.2
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from .models import Publication


@login_required
def publication_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="publication_4_7_2.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    normal_style = ParagraphStyle(
        name='NormalWrap',
        parent=styles['Normal'],
        fontSize=9,
        leading=12
    )

    # ===== TITLE =====
    title = Paragraph(
        "<b>4.7.2. Publication of technical magazines, newsletters, etc. (05)</b>",
        styles["Heading3"]
    )
    elements.append(title)
    elements.append(Spacer(1, 10))

    # ===== TABLE HEADER BAR =====
    header_data = [["Publication Description",
                    "Year of Publication",
                    "Issue No.",
                    "Editor/Author"]]

    data = header_data

    publications = Publication.objects.all().order_by("-year_of_publication")

    for pub in publications:
        data.append([
            Paragraph(pub.publication_description, normal_style),
            pub.year_of_publication,
            pub.issue_no,
            Paragraph(pub.editor_author, normal_style),
        ])

    table = Table(
        data,
        colWidths=[
            2.2 * inch,
            1.5 * inch,
            1.3 * inch,
            2.0 * inch
        ],
        repeatRows=1
    )

    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#A7D3D3")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        # Grid
        ("GRID", (0, 0), (-1, -1), 0.6, colors.black),

        # Alignment
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 1), (2, -1), "CENTER"),

        # Padding
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 10))

    # ===== TABLE FOOTER =====
    footer = Paragraph(
        "<b>Table No. 4.7.2. : Publication of technical magazines, newsletters</b>",
        styles["Normal"]
    )
    elements.append(footer)

    doc.build(elements)
    return response

from .models import Publication
from .forms import PublicationForm
from django.shortcuts import render, redirect, get_object_or_404


# ==========================
# 4.7.2 Publications
# ==========================

@login_required
def publication_list1(request):
    data = Publication.objects.all().order_by("-year_of_publication")
    return render(request, "publication472/list.html", {"data": data})


@login_required
def publication_add1(request):
    form = PublicationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("publication_list1")
    return render(request, "publication472/form.html", {"form": form})


@login_required
def publication_edit1(request, id):
    obj = get_object_or_404(Publication, id=id)
    form = PublicationForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("publication_list1")
    return render(request, "publication472/form.html", {"form": form})


@login_required
def publication_delete1(request, id):
    obj = get_object_or_404(Publication, id=id)
    obj.delete()
    return redirect("publication_list1")

#4.7.3
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A3
from reportlab.lib.units import inch
from .models import StudentParticipation


@login_required
def participation_4_7_3_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="4.7.3_Student_Participation.pdf"'

    from reportlab.lib.pagesizes import A3, landscape

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A3),
        rightMargin=30,
        leftMargin=30,
        topMargin=40,
        bottomMargin=40,
    )
    elements = []

    styles = getSampleStyleSheet()

    normal_style = ParagraphStyle(
        name='NormalWrap',
        parent=styles['Normal'],
        fontSize=9,
        leading=12
    )

    title_style = ParagraphStyle(
        name='CenterTitle',
        parent=styles['Heading2'],
        alignment=1  # center
    )

    # ===== MAIN TITLE =====
    elements.append(Paragraph(
        "<b>4.7.3 Participation in inter-institute/state/national events by students of the program of study (05)</b>",
        title_style
    ))
    elements.append(Spacer(1, 15))

    years = StudentParticipation.objects.values_list(
        "assessment_year", flat=True
    ).distinct()

    for year in years:

        records = StudentParticipation.objects.filter(
            assessment_year=year
        )

        data = []

        # ===== HEADER =====
        data.append([
            "Sr. No.",
            "Type of Activity",
            "Date",
            "Name of Participating Student",
            "Organizing Body",
            "Awards",
            "Level",
            "Relevance to PEO's & PO's"
        ])

        # ===== CAY ROW INSIDE TABLE =====
        data.append([year, "", "", "", "", "", "", ""])

        # ===== DATA =====
        for index, record in enumerate(records, start=1):
            data.append([
                index,
                Paragraph(record.type_of_activity, normal_style),
                record.date,
                Paragraph(record.student_name, normal_style),
                Paragraph(record.organizing_body, normal_style),
                record.awards,
                record.level,
                Paragraph(record.relevance_peos_pos, normal_style),
            ])


        table = Table(
        data,
        colWidths=[
            50,   # Sr No
            200,  # Type
            80,   # Date
            220,  # Student Name
            250,  # Organizing Body
            100,  # Awards
            100,  # Level
            200,  # Relevance
        ],
        repeatRows=1
        )

        table.setStyle(TableStyle([

            # Header
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            # Yellow CAY row
            ("SPAN", (0, 1), (-1, 1)),
            ("BACKGROUND", (0, 1), (-1, 1), colors.yellow),
            ("ALIGN", (0, 1), (-1, 1), "CENTER"),
            ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),

            # Grid
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

            # Vertical align
            ("VALIGN", (0, 0), (-1, -1), "TOP"),

            # Center some columns
            ("ALIGN", (0, 2), (0, -1), "CENTER"),
            ("ALIGN", (2, 2), (2, -1), "CENTER"),
            ("ALIGN", (5, 2), (6, -1), "CENTER"),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

    doc.build(elements)
    return response

########
from .forms import StudentParticipationForm
from django.shortcuts import redirect, get_object_or_404

# LIST VIEW
@login_required
def participation_list(request):
    query = request.GET.get("q")
    if query:
        data = StudentParticipation.objects.filter(
            Q(student_name__icontains=query) |
            Q(type_of_activity__icontains=query) |
            Q(organizing_body__icontains=query) |
            Q(level__icontains=query) |
            Q(assessment_year__icontains=query)
        ).order_by("assessment_year", "student_name")
    else:
        data = StudentParticipation.objects.all().order_by("assessment_year", "student_name")

    # Get all unique years for the dropdown
    all_years = StudentParticipation.objects.values_list(
        'assessment_year', flat=True
    ).distinct().order_by('assessment_year')

    return render(request, "participation/list.html", {
        "data": data,
        "query": query,
        "all_years": all_years,
    })

# CREATE VIEW
@login_required
def participation_add(request):
    form = StudentParticipationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("participation_list")
    return render(request, "participation/form.html", {"form": form})

# UPDATE VIEW
@login_required
def participation_edit(request, id):
    obj = get_object_or_404(StudentParticipation, id=id)
    form = StudentParticipationForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("participation_list")
    return render(request, "participation/form.html", {"form": form})

# DELETE VIEW
@login_required
def participation_delete(request, id):
    obj = get_object_or_404(StudentParticipation, id=id)
    obj.delete()
    return redirect("participation_list")

#4.5
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle



@login_required
def academic451_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="academic_performance_4_5_1.pdf"'

    # 🔥 Landscape mode
    doc = SimpleDocTemplate(response, pagesize=landscape(A4))

    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(
        "Table No. 4.5.1 : Academic Performance in Final Year",
        styles["Heading2"]
    ))
    elements.append(Spacer(1, 0.3 * inch))

    records = AcademicPerformance4_5_1.last_three_records()

    if len(records) < 3:
        elements.append(Paragraph("Please add at least 3 years of data.", styles["Normal"]))
        doc.build(elements)
        return response

    r1, r2, r3 = records

    header_style = styles["Normal"]

    data = [
    [
        Paragraph("<b>Academic Performance</b>", styles["Normal"]),
        Paragraph(f"<b>{r1.year_label}</b>", styles["Normal"]),
        Paragraph(f"<b>{r2.year_label}</b>", styles["Normal"]),
        Paragraph(f"<b>{r3.year_label}</b>", styles["Normal"]),
    ],
    ["Mean of CGPA / % (X)", r1.X, r2.X, r3.X],
    ["Total Successful Students (Y)", r1.Y, r2.Y, r3.Y],
    ["Total Appeared (Z)", r1.Z, r2.Z, r3.Z],
    ["API = X × (Y/Z)", r1.API, r2.API, r3.API],

    ]

    avg_api = round((r1.API + r2.API + r3.API) / 3, 2)
    performance_level = round(1.5 * avg_api, 2)

    data.append(["Average API", "", "", avg_api])
    data.append(["Academic Performance Level (1.5 × Avg API)", "", "", performance_level])

    # 🔥 Proper column widths
    table = Table(
        data,
        colWidths=[3.2 * inch, 2.4 * inch, 2.4 * inch, 2.4 * inch]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
    ]))

    elements.append(table)
    doc.build(elements)

    return response

from django.shortcuts import render, redirect, get_object_or_404
from .models import AcademicPerformance4_5_1
from .forms import AcademicPerformance451Form


# ==============================
# 4.5 Academic Performance Final Year
# ==============================

@login_required
def academic451_list1(request):
    data = AcademicPerformance4_5_1.objects.all().order_by("-year")

    avg_api = 0
    performance_level = 0

    if data.count() >= 3:
        last_three = AcademicPerformance4_5_1.last_three_records()
        avg_api = round(sum(r.API for r in last_three) / 3, 2)
        performance_level = round(1.5 * avg_api, 2)

    return render(request, "academic451/list.html", {
        "data": data,
        "avg_api": avg_api,
        "performance_level": performance_level
    })


@login_required
def academic451_add1(request):
    form = AcademicPerformance451Form(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("academic451_list1")
    return render(request, "academic451/form.html", {"form": form})


@login_required
def academic451_edit1(request, id):
    obj = get_object_or_404(AcademicPerformance4_5_1, id=id)
    form = AcademicPerformance451Form(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("academic451_list1")
    return render(request, "academic451/form.html", {"form": form})


@login_required
def academic451_delete1(request, id):
    obj = get_object_or_404(AcademicPerformance4_5_1, id=id)
    obj.delete()
    return redirect("academic451_list1")


#------------------DASHBOARD-------------------#
@login_required
@login_required
def dashboard(request):

    from .models import (
        AcademicPerformance4_3_1,
        AcademicPerformance4_5_1,
        PlacementRecord,
        Publication
    )

    context = {
        "total_publications": Publication.objects.count(),
        "total_placements": PlacementRecord.objects.count(),
        "academic451_score": (
            AcademicPerformance4_5_1.last_three_records()[0].academic_performance_level
            if AcademicPerformance4_5_1.objects.exists()
            else 0
        ),
    }

    return render(request, "dashboard.html", context)

#--------------ALL IN ONE PDF -----------------------#
# ================================================================
# FULL REPORT PDF — reads everything from database
# ================================================================
from datetime import date
from itertools import groupby
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

from .models import (
    EnrolmentRatio, EnrolmentRatio4_1_1, EnrolmentRatioMarksOnly4_1_2,
    SuccessRateStipulatedPeriod, studentspassedwithbacklogs,
    AcademicPerformance4_3_1, AcademicPerformanceSecondYear, AcademicPerformance4_5_1,
    SuccessRate, SuccessRateWithBacklogs,
    PlacementandHigherStudies, PlacementRecord,
    ProfessionalActivity, Publication, StudentParticipation
)

@login_required
def full_report_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Criterion4_Full_Report.pdf"'

    PAGE_W, PAGE_H = A4
    LM = RM = 1.8 * cm
    TM = 2.2 * cm
    BM = 1.8 * cm
    W = PAGE_W - LM - RM

    doc = SimpleDocTemplate(response, pagesize=A4,
        leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM + 8*mm)

    BLACK = colors.black
    WHITE = colors.white

    def _s(name, **kw): return ParagraphStyle(name, **kw)
    S_TH  = _s('TH',  fontName='Helvetica-Bold',  fontSize=10, textColor=BLACK, alignment=TA_CENTER, leading=12)
    S_TC  = _s('TC',  fontName='Helvetica',         fontSize=9, alignment=TA_CENTER, leading=11)
    S_TCL = _s('TCL', fontName='Helvetica',         fontSize=9, alignment=TA_LEFT,   leading=11)
    S_TCB = _s('TCB', fontName='Helvetica-Bold',    fontSize=9, alignment=TA_CENTER, leading=11)
    S_B   = _s('B',   fontName='Helvetica',         fontSize=10, leading=14, spaceBefore=4, spaceAfter=4)
    S_H1  = _s('H1',  fontName='Helvetica-Bold',    fontSize=16, alignment=TA_CENTER, spaceAfter=20)
    S_H2  = _s('H2',  fontName='Helvetica-Bold',    fontSize=13, spaceBefore=15, spaceAfter=10)
    S_H3  = _s('H3',  fontName='Helvetica-Bold',    fontSize=11, spaceBefore=10, spaceAfter=6)
    S_CAP = _s('CAP', fontName='Helvetica-Bold',    fontSize=10, alignment=TA_CENTER, spaceBefore=6, spaceAfter=10)
    
    # Wrap style for long text
    S_WRAP = _s('WRAP', fontName='Helvetica', fontSize=8, leading=10, alignment=TA_LEFT)

    def th(t):   return Paragraph(str(t), S_TH)
    def tc(t):   return Paragraph('' if t is None else str(t), S_TC)
    def tcl(t):  return Paragraph('' if t is None else str(t), S_TCL)
    def tcb(t):  return Paragraph('' if t is None else str(t), S_TCB)
    def tw(t):   return Paragraph('' if t is None else str(t), S_WRAP)
    def sp(n=4): return Spacer(1, n)

    BASE_TS = [
        ('GRID', (0,0), (-1,-1), 0.5, BLACK),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.drawRightString(PAGE_W - RM, 10*mm, f'Page {doc.page}')
        canvas.restoreState()

    story = []

    # 1. COVER / TITLE
    story += [
        Paragraph('CRITERION 4', S_H1),
        Paragraph("STUDENTS’ PERFORMANCE", S_H1),
        Paragraph('200', S_TH),
        sp(20)
    ]

    # 4.1 INTAKE
    story += [
        Paragraph('Intake Information:', S_B),
        Paragraph('Following Table No. 4.1 shows the intake information', S_B),
        sp(4)
    ]
    er6 = list(EnrolmentRatio.objects.order_by('-academic_year')[:6])
    while len(er6) < 6: er6.append(None)
    
    def ev(i,f): r=er6[i]; return getattr(r,f,'-') if r else '-'
    def yl(i):   
        r=er6[i]
        if not r: return '-'
        prefix = "CAY" if i==0 else f"CAY m{i}"
        return f"{prefix}\n({r.academic_year})"

    data41 = [
        [th('Item'), th('Academic Year'), '', '', '', '', ''],
        ['', th(yl(0)), th(yl(1)), th(yl(2)), th(yl(3)), th(yl(4)), th(yl(5))],
        [tcl('Sanctioned intake strength of the program (N)'), tc(ev(0,'sanctioned_intake')), tc(ev(1,'sanctioned_intake')), tc(ev(2,'sanctioned_intake')), tc(ev(3,'sanctioned_intake')), tc(ev(4,'sanctioned_intake')), tc(ev(5,'sanctioned_intake'))],
        [tcl('Total number of students, admitted through state level counseling (N1)'), tc(ev(0,'first_year_admitted')), tc(ev(1,'first_year_admitted')), tc(ev(2,'first_year_admitted')), tc(ev(3,'first_year_admitted')), tc(ev(4,'first_year_admitted')), tc(ev(5,'first_year_admitted'))],
        [tcl('Number of students, admitted through Institute level quota (N2)'), tc(ev(0,'lateral_entry')), tc(ev(1,'lateral_entry')), tc(ev(2,'lateral_entry')), tc(ev(3,'lateral_entry')), tc(ev(4,'lateral_entry')), tc(ev(5,'lateral_entry'))],
        [tcl('Number of students, admitted through lateral entry (N3)'), tc(ev(0,'separate_division')), tc(ev(1,'separate_division')), tc(ev(2,'separate_division')), tc(ev(3,'separate_division')), tc(ev(4,'separate_division')), tc(ev(5,'separate_division'))],
        [tcl('Total number of students admitted in the Program (N1 + N2 + N3)'), tcb(ev(0,'total_admitted')), tcb(ev(1,'total_admitted')), tcb(ev(2,'total_admitted')), tcb(ev(3,'total_admitted')), tcb(ev(4,'total_admitted')), tcb(ev(5,'total_admitted'))],
    ]
    ts41 = BASE_TS + [('SPAN',(0,0),(0,1)), ('SPAN',(1,0),(6,0))]
    story += [Table(data41, colWidths=[6*cm, 2.3*cm, 2.3*cm, 2.3*cm, 2.3*cm, 2.3*cm, 2.3*cm], style=TableStyle(ts41)),
              Paragraph('Table No. 4.1 : Intake Information', S_CAP), sp(15)]

    # 4.2 PASSED WITHOUT BACKLOGS
    story += [
        Paragraph('Following Table No. 4.2 Number of students passed without backlogs in stipulated year of study', S_B),
        sp(4)
    ]
    data42 = [[th('Year of entry'), th('N1 + N2 + N3\n(As defined above)'), th('Number of students who have successfully passed without backlogs in any year of study'), '', ''],
              ['', '', th('I Year'), th('II Year'), th('III Year')]]
    for r in SuccessRateStipulatedPeriod.objects.order_by('-year_of_entry'):
        data42.append([tcl(r.year_of_entry), tc(r.n1_n2_n3_total), tc(r.passed_year_1), tc(r.passed_year_2), tc(r.passed_year_3)])
    ts42 = BASE_TS + [('SPAN',(0,0),(0,1)), ('SPAN',(1,0),(1,1)), ('SPAN',(2,0),(4,0))]
    story += [Table(data42, colWidths=[3*cm, 4*cm, 3.5*cm, 3.5*cm, 3.5*cm], style=TableStyle(ts42)),
              Paragraph('Table No. 4.2 : Number of students passed without backlogs in stipulated year of study', S_CAP),
              Paragraph('LYG : Last Year Graduate', S_B), sp(10)]

    # 4.3 PASSED WITH BACKLOGS
    story += [
        Paragraph('Following Table No. 4.3 shows number of students passed with backlogs in stipulated year of study.', S_B),
        sp(4)
    ]
    data43 = [[th('Year of entry'), th('N1 + N2 + N3\n(As defined above)'), th('Number of students who have successfully passed (Students with backlog in stipulated period of study)'), '', ''],
              ['', '', th('I Year'), th('II Year'), th('III Year')]]
    for r in studentspassedwithbacklogs.objects.order_by('-year_of_entry'):
        data43.append([tcl(r.year_of_entry), tc(r.n1_n2_n3_total), tc(r.passed_year_1), tc(r.passed_year_2), tc(r.passed_year_3)])
    ts43 = BASE_TS + [('SPAN',(0,0),(0,1)), ('SPAN',(1,0),(1,1)), ('SPAN',(2,0),(4,0))]
    story += [Table(data43, colWidths=[3*cm, 4*cm, 3.5*cm, 3.5*cm, 3.5*cm], style=TableStyle(ts43)),
              Paragraph('Table No. 4.3 : Number of students passed with backlogs in stipulated year of study', S_CAP), sp(15)]

    # 4.1 ENROLMENT RATIO (SUMMARY)
    story += [
        Paragraph('4.1 Enrolment Ratio (20)', S_H2),
        Paragraph('Enrolment Ratio = (N1 + N2) / N', S_B),
        Paragraph('Following Table No. 4.1.1 shows Average Enrolment Ratio.', S_B),
        sp(4)
    ]
    e411 = EnrolmentRatio4_1_1.objects.first()
    if e411:
        def enr(n1,n2,n): return round(((n1+n2)/n)*100,2) if n else 0
        ec, ec1, ec2 = enr(e411.N1,e411.N2,e411.N), enr(e411.N1_m1,e411.N2_m1,e411.N_m1), enr(e411.N1_m2,e411.N2_m2,e411.N_m2)
        avg_er = round((ec+ec1+ec2)/3,2)
        data411 = [
            [th('Item'), th('CAY (2023-24)'), th('CAY m1 (2022-23)'), th('CAY m2 (2021-22)')],
            [tcl('N1'), tc(e411.N1), tc(e411.N1_m1), tc(e411.N1_m2)],
            [tcl('N2'), tc(e411.N2), tc(e411.N2_m1), tc(e411.N2_m2)],
            [tcl('N'), tc(e411.N), tc(e411.N_m1), tc(e411.N_m2)],
            [tcl('Total (N1+N2)'), tcb(e411.N1+e411.N2), tcb(e411.N1_m1+e411.N2_m1), tcb(e411.N1_m2+e411.N2_m2)],
            [tcl('Enrollment Ratio (%)'), tcb(ec), tcb(ec1), tcb(ec2)],
            [tcl('Average Enrollment Ratio'), tcb(avg_er), '', '']
        ]
        story += [Table(data411, colWidths=[7*cm, 3.5*cm, 3.5*cm, 3.5*cm], style=TableStyle(BASE_TS + [('SPAN',(1,6),(3,6))])),
                  Paragraph('Table No. 4.1.1 : Average Enrollment Ratio', S_CAP)]
    
    story += [Paragraph('Following Table No. 4.1.2 shows Enrolment Ratio.', S_B), sp(4)]
    e412 = EnrolmentRatioMarksOnly4_1_2.objects.first()
    data412 = [[th('Item'), th('Marks')]]
    if e412:
        data412 += [[tcl('>=90% Students'), tc(e412.marks_90)], [tcl('>=80% Students'), tc(e412.marks_80)], [tcl('>=70% Students'), tc(e412.marks_70)],
                    [tcl('>=60% Students'), tc(e412.marks_60)], [tcl('>=50% Students'), tc(e412.marks_50)], [tcl('<50% Students'), tc(e412.marks_below_50)]]
    story += [Table(data412, colWidths=[8*cm, 4*cm], style=TableStyle(BASE_TS)),
              Paragraph('Table No. 4.1.2 : Enrolment Ratio', S_CAP), sp(15)]

    # 4.2 SUCCESS RATE (SUMMARY)
    story += [Paragraph('4.2 Success Rate in the stipulated period of the program (60)', S_H2),
              Paragraph('4.2.1. Success rate without backlogs in any year of study (40)', S_H3),
              Paragraph('Average SI = Mean of success index (SI) for past three batches', S_B),
              Paragraph('Success rate without backlogs in any year of study = 40 × Average SI', S_B),
              Paragraph('Following Table No. 4.2.1 shows success rate without backlogs in any year of study.', S_B), sp(4)]
    sr1 = list(SuccessRate.objects.order_by('-year_label')[:3])
    if sr1:
        avg_si1 = SuccessRate.last_three_avg_si()
        data421 = [[th('Item'), th('LYG'), th('LYG m1'), th('LYG m2')],
                   [tcl('Total number of students (X)'), tc(sr1[0].X), tc(sr1[1].X), tc(sr1[2].X)],
                   [tcl('Number of students passed without backlogs (Y)'), tc(sr1[0].Y), tc(sr1[1].Y), tc(sr1[2].Y)],
                   [tcl('Success index (SI)'), tc(sr1[0].SI), tc(sr1[1].SI), tc(sr1[2].SI)],
                   [tcl('Average SI'), tc(avg_si1), '', ''],
                   [tcl('Success Rate'), tc(round(40*avg_si1, 2)), '', '']]
        story += [Table(data421, colWidths=[7.5*cm, 3*cm, 3*cm, 3*cm], style=TableStyle(BASE_TS + [('SPAN',(1,4),(3,4)), ('SPAN',(1,5),(3,5))])),
                  Paragraph('Table No. 4.2.1 : Success rate without backlogs in any year of study', S_CAP)]

    story += [sp(10), Paragraph('4.2.2. Success rate with backlog in stipulated period of study (20)', S_H3),
              Paragraph('Following Table No. 4.2.2 shows success rate with backlogs in any year of study.', S_B), sp(4)]
    sr2 = list(SuccessRateWithBacklogs.objects.order_by('-year_label')[:3])
    if sr2:
        avg_si2 = SuccessRateWithBacklogs.last_three_avg_si()
        data422 = [[th('Item'), th('LYG'), th('LYG m1'), th('LYG m2')],
                   [tcl('Total number of students (X)'), tc(sr2[0].X), tc(sr2[1].X), tc(sr2[2].X)],
                   [tcl('Number of students passed with backlogs (Y)'), tc(sr2[0].Y), tc(sr2[1].Y), tc(sr2[2].Y)],
                   [tcl('Success index (SI)'), tc(sr2[0].SI), tc(sr2[1].SI), tc(sr2[2].SI)],
                   [tcl('Average SI'), tc(avg_si2), '', ''],
                   [tcl('Success Rate'), tc(round(20*avg_si2, 2)), '', '']]
        story += [Table(data422, colWidths=[7.5*cm, 3*cm, 3*cm, 3*cm], style=TableStyle(BASE_TS + [('SPAN',(1,4),(3,4)), ('SPAN',(1,5),(3,5))])),
                  Paragraph('Table No. 4.2.2 : Success rate with backlogs in stipulated period of study', S_CAP), sp(15)]

    # 4.3 ACADEMIC PERFORMANCE I YEAR
    story += [Paragraph('4.3. Academic Performance in First Year (25)', S_H2),
              Paragraph('Academic Performance Level = 2.5 * Average API', S_B),
              Paragraph('Following table 4.3.1 shows academic performance in first year.', S_B), sp(4)]
    ap1 = list(AcademicPerformance4_3_1.objects.exclude(year=None).order_by('-year')[:3])
    if ap1:
        avg_api1 = ap1[0].average_api
        data431 = [[th('Academic Performance'), th('CAY m1'), th('CAY m2'), th('CAY m3')],
                   [tcl('Mean Percent (X)'), tc(ap1[0].X), tc(ap1[1].X), tc(ap1[2].X)],
                   [tcl('Total Successful Students (Y)'), tc(ap1[0].Y), tc(ap1[1].Y), tc(ap1[2].Y)],
                   [tcl('Total Appeared (Z)'), tc(ap1[0].Z), tc(ap1[1].Z), tc(ap1[2].Z)],
                   [tcl('API = X * (Y/Z)'), tc(ap1[0].API), tc(ap1[1].API), tc(ap1[2].API)],
                   [tcl('Average API'), tc(avg_api1), '', '']]
        story += [Table(data431, colWidths=[7.5*cm, 3*cm, 3*cm, 3*cm], style=TableStyle(BASE_TS + [('SPAN',(1,5),(3,5))])),
                  Paragraph('Table No. 4.3.1 : Academic Performance in first year', S_CAP), sp(15)]

    # 4.4 ACADEMIC PERFORMANCE II YEAR
    story += [Paragraph('4.4. Academic Performance in Second Year (20)', S_H2),
              Paragraph('Academic Performance Level = 2.0 * Average API', S_B),
              Paragraph('Following table 4.4.1 shows academic performance in second year.', S_B), sp(4)]
    ap2 = list(AcademicPerformanceSecondYear.objects.exclude(year=None).order_by('-year')[:3])
    if ap2:
        avg_api2 = ap2[0].average_api
        data441 = [[th('Academic Performance'), th('CAY m1'), th('CAY m2'), th('CAY m3')],
                   [tcl('Mean Percent (X)'), tc(ap2[0].X), tc(ap2[1].X), tc(ap2[2].X)],
                   [tcl('Total Successful Students (Y)'), tc(ap2[0].Y), tc(ap2[1].Y), tc(ap2[2].Y)],
                   [tcl('Total Appeared (Z)'), tc(ap2[0].Z), tc(ap2[1].Z), tc(ap2[2].Z)],
                   [tcl('API = X * (Y/Z)'), tc(ap2[0].API), tc(ap2[1].API), tc(ap2[2].API)],
                   [tcl('Average API'), tc(avg_api2), '', '']]
        story += [Table(data441, colWidths=[7.5*cm, 3*cm, 3*cm, 3*cm], style=TableStyle(BASE_TS + [('SPAN',(1,5),(3,5))])),
                  Paragraph('Table No. 4.4.1 : Academic performance in second year', S_CAP), sp(15)]

    # 4.5 ACADEMIC PERFORMANCE III YEAR
    story += [Paragraph('4.5. Academic Performance in Final Year (15)', S_H2),
              Paragraph('Academic Performance Level = 1.5 * Average API', S_B),
              Paragraph('Following Table No. 4.5.1 shows academic performance in final year.', S_B), sp(4)]
    ap3 = list(AcademicPerformance4_5_1.objects.exclude(year=None).order_by('-year')[:3])
    if ap3:
        avg_api3 = ap3[0].average_api
        data451 = [[th('Academic Performance'), th('LYG'), th('LYG m1'), th('LYG m2')],
                   [tcl('Mean Percent (X)'), tc(ap3[0].X), tc(ap3[1].X), tc(ap3[2].X)],
                   [tcl('Total Successful Students (Y)'), tc(ap3[0].Y), tc(ap3[1].Y), tc(ap3[2].Y)],
                   [tcl('Total Appeared (Z)'), tc(ap3[0].Z), tc(ap3[1].Z), tc(ap3[2].Z)],
                   [tcl('API = X * (Y/Z)'), tc(ap3[0].API), tc(ap3[1].API), tc(ap3[2].API)],
                   [tcl('Average API'), tc(avg_api3), '', '']]
        story += [Table(data451, colWidths=[7.5*cm, 3*cm, 3*cm, 3*cm], style=TableStyle(BASE_TS + [('SPAN',(1,5),(3,5))])),
                  Paragraph('Table No. 4.5.1 : Academic Performance in final year', S_CAP), sp(15)]

    # 4.6 PLACEMENT
    story += [Paragraph('4.6. Placement and Higher Studies (40)', S_H2),
              Paragraph('Following table 4.6.1 shows details of Placement and Higher studies.', S_B), sp(4)]
    phs = list(PlacementandHigherStudies.objects.order_by('-id')[:3])
    if phs:
        p_vals = PlacementandHigherStudies.get_P_values()
        avg_p = round(sum(p_vals)/3, 2)
        data461 = [[th('Item'), th('LYG'), th('LYG m1'), th('LYG m2')],
                   [tcl('Total No. of Final Year Students (N)'), tc(phs[0].N), tc(phs[1].N), tc(phs[2].N)],
                   [tcl('Placed (X)'), tc(phs[0].X), tc(phs[1].X), tc(phs[2].X)],
                   [tcl('Higher Studies (Y)'), tc(phs[0].Y), tc(phs[1].Y), tc(phs[2].Y)],
                   [tcl('Entrepreneurs (Z)'), tc(phs[0].Z), tc(phs[1].Z), tc(phs[2].Z)],
                   [tcl('Placement Index (P)'), tc(phs[0].P), tc(phs[1].P), tc(phs[2].P)],
                   [tcl('Average placement'), tc(avg_p), '', ''],
                   [tcl('Assessment (40 * Average Placement)'), tc(round(40*avg_p, 2)), '', '']]
        story += [Table(data461, colWidths=[7.5*cm, 3*cm, 3*cm, 3*cm], style=TableStyle(BASE_TS + [('SPAN',(1,6),(3,6)), ('SPAN',(1,7),(3,7))])),
                  Paragraph('Table No. 4.6.1 : Placement and Higher studies', S_CAP), sp(15)]

    # 4.6.a PLACEMENT DATA
    story += [Paragraph('4.6. a. Placement data', S_H3)]
    for yr, grp in groupby(PlacementRecord.objects.all().order_by('assessment_year', 'student_name'), key=lambda r: r.assessment_year):
        records = list(grp)
        story += [Paragraph(f'Assessment Year : {yr}', S_B), sp(4)]
        data_pa = [[th('Sr. No.'), th('Student Name'), th('Enrollment No.'), th('Employer Name'), th('Appointment No.')]]
        for i, r in enumerate(records, 1):
            data_pa.append([tc(i), tcl(r.student_name), tc(r.enrollment_no), tcl(r.employer_name), tc(r.appointment_no)])
        story += [Table(data_pa, colWidths=[1.5*cm, 5.5*cm, 3*cm, 4.5*cm, 3*cm], style=TableStyle(BASE_TS)), sp(10)]
    story += [Paragraph('Table No. 4.6.a : Placement data assessment year wise', S_CAP), sp(15)]

    # 4.7 PROFESSIONAL ACTIVITIES
    story += [Paragraph('4.7. Professional Activities (20)', S_H2),
              Paragraph('4.7.1. Professional societies / student chapters and organizing technical events (10)', S_H3),
              Paragraph('Following table 4.7.1 shows Professional Activities', S_B), sp(4)]
    for yr, grp in groupby(ProfessionalActivity.objects.all().order_by('assessment_year', 'date'), key=lambda r: r.assessment_year):
        records = list(grp)
        story += [Paragraph(str(yr), S_B), sp(4)]
        data_prof = [[th('Sr. No.'), th('Date'), th('Event Name'), th('Details'), th('Professional Society')]]
        for i, r in enumerate(records, 1):
            data_prof.append([tc(i), tc(r.date.strftime("%d/%m/%Y")), tw(r.event_name), tw(r.details), tc(r.professional_society)])
        story += [Table(data_prof, colWidths=[1.2*cm, 2*cm, 4.5*cm, 7*cm, 2.5*cm], style=TableStyle(BASE_TS)), sp(10)]
    story += [Paragraph('Table No. 4.7.1 : Professional Activities', S_CAP), sp(15)]

    # 4.7.2 PUBLICATIONS
    story += [Paragraph('4.7.2. Publication of technical magazines, newsletters, etc. (05)', S_H3)]
    data_pub = [[th('Publication Description'), th('Year'), th('Issue No.'), th('Editor/Author')]]
    for r in Publication.objects.all().order_by('-year_of_publication'):
        data_pub.append([tw(r.publication_description), tc(r.year_of_publication), tc(r.issue_no), tw(r.editor_author)])
    story += [Table(data_pub, colWidths=[6.5*cm, 3.5*cm, 3.5*cm, 4.5*cm], style=TableStyle(BASE_TS)),
              Paragraph('Table No. 4.7.2 : Publication of technical magazines, newsletters', S_CAP), sp(15)]

    # 4.7.3 STUDENT PARTICIPATION
    story += [Paragraph('4.7.3 Participation in inter-institute/state/national events (05)', S_H3)]
    for yr, grp in groupby(StudentParticipation.objects.all().order_by('assessment_year', 'student_name'), key=lambda r: r.assessment_year):
        records = list(grp)
        story += [Paragraph(str(yr), S_B), sp(4)]
        data_sp = [[th('Sr. No.'), th('Type of Activity'), th('Date'), th('Student Name'), th('Organizing Body'), th('Awards'), th('Level'), th('Relevance to POs/PEOs')]]
        for i, r in enumerate(records, 1):
            data_sp.append([tc(i), tw(r.type_of_activity), tc(r.date), tw(r.student_name), tw(r.organizing_body), tc(r.awards), tc(r.level), tw(r.relevance_peos_pos)])
        story += [Table(data_sp, colWidths=[0.8*cm, 2.5*cm, 1.8*cm, 3*cm, 3*cm, 2*cm, 1.6*cm, 2.5*cm], style=TableStyle(BASE_TS + [('FONTSIZE',(0,0),(-1,-1),7)])), sp(10)]

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return response