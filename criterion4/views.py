from django.shortcuts import render
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from .models import EnrolmentRatio
from .models import EnrolmentRatio4_1_1
from .models import EnrolmentRatioMarksOnly4_1_2
from .models import SuccessRateStipulatedPeriod
from .models import studentspassedwithbacklogs


# ✅ HOME PAGE (No login required)
def criterion4_home(request):
    return render(request, "criterion4_home.html")


# ✅ PDF GENERATION (Table 4.1 - Enrolment Ratio)
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

#4.1.1 PDF GENERATION
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

# ✅ PDF GENERATION (Table 4.2 - Success Rate Without Backlogs)
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

# ✅ PDF GENERATION (Table 4.3 - students passed with backlogs )
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

#---------------------------4.3.1------------------------------
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from .models import AcademicPerformance4_3_1


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



#4.6
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet

from .models import PlacementandHigherStudies


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

#4.6.a
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from .models import PlacementRecord


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

#4.1.1
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet

from .models import AcademicPerformance


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
    records = AcademicPerformance.objects.order_by("-id")[:3]

    if len(records) < 3:
        elements.append(Paragraph("Enter 3 records first.", styles["Normal"]))
        doc.build(elements)
        return response

    r1, r2, r3 = records

    # -------- CALCULATIONS --------
    api1, api2, api3 = r1.api, r2.api, r3.api
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

#4.2.1
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet

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

#4.7.2
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from .models import Publication


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

#4.7.3
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A3
from reportlab.lib.units import inch
from .models import StudentParticipation


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