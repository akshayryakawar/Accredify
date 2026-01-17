from django.shortcuts import render
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from .models import EnrolmentRatio
from .models import SuccessRateStipulatedPeriod


# ✅ HOME PAGE (No login required)
def criterion4_home(request):
    return render(request, "criterion4_home.html")


# ✅ PDF GENERATION (Table 4.1 - Enrolment Ratio)
def enrolment_ratio_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Table_4_1_Intake_Information.pdf"'

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
    elements.append(Paragraph("<b>Criterion 4 – Students’ Performance</b>", styles['Title']))
    elements.append(Paragraph("<b>Table No. 4.1 : Intake Information</b>", styles['Heading2']))
    elements.append(Spacer(1, 15))

    # ---------------- FETCH LAST 6 YEARS ----------------
    records = list(EnrolmentRatio.objects.order_by('-academic_year')[:6])

    # Ensure exactly 6 columns
    while len(records) < 6:
        records.append(None)

    # ---------------- TABLE HEADER (LIKE IMAGE) ----------------
    table_data = [
        ["Item", "Academic Year", "", "", "", "", ""],
        ["", "CAY (2023-24)", "CAY (2022-23)", "CAY (2021-22)", "CAY (2020-21)", "CAY (2019-20)", "CAY (2018-19)"],
    ]

    # ---------------- DATA HELPER ----------------
    def val(index, field):
        if records[index]:
            return getattr(records[index], field)
        return "-"

    # ---------------- TABLE ROWS ----------------
    table_data.extend([
        [
            "Sanctioned intake strength of the program (N)",
            val(0, "sanctioned_intake"),
            val(1, "sanctioned_intake"),
            val(2, "sanctioned_intake"),
            val(3, "sanctioned_intake"),
            val(4, "sanctioned_intake"),
            val(5, "sanctioned_intake"),
        ],
        [
            "Students admitted through state level counseling (N1)",
            val(0, "first_year_admitted"),
            val(1, "first_year_admitted"),
            val(2, "first_year_admitted"),
            val(3, "first_year_admitted"),
            val(4, "first_year_admitted"),
            val(5, "first_year_admitted"),
        ],
        [
            "Students admitted through institute level quota (N2)",
            val(0, "lateral_entry"),
            val(1, "lateral_entry"),
            val(2, "lateral_entry"),
            val(3, "lateral_entry"),
            val(4, "lateral_entry"),
            val(5, "lateral_entry"),
        ],
        [
            "Students admitted through lateral entry (N3)",
            val(0, "separate_division"),
            val(1, "separate_division"),
            val(2, "separate_division"),
            val(3, "separate_division"),
            val(4, "separate_division"),
            val(5, "separate_division"),
        ],
        [
            "Total number of students admitted (N1 + N2 + N3)",
            val(0, "total_admitted"),
            val(1, "total_admitted"),
            val(2, "total_admitted"),
            val(3, "total_admitted"),
            val(4, "total_admitted"),
            val(5, "total_admitted"),
        ],
    ])

    # ---------------- CREATE TABLE ----------------
    table = Table(
        table_data,
        colWidths=[320, 80, 80, 80, 80, 80, 80],
        rowHeights=[30, 30, 35, 35, 35, 35, 35]  # ✅ 2 header + 5 rows
    )

    table.setStyle(TableStyle([
        # ✅ MERGE CELLS LIKE IMAGE
        ('SPAN', (0, 0), (0, 1)),   # Item column merge (row 0-1)
        ('SPAN', (1, 0), (6, 0)),   # Academic Year merge across 6 columns

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        # Header Background (2 rows)
        ('BACKGROUND', (0, 0), (-1, 1), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)

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
