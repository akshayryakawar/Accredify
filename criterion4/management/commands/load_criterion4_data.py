import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from criterion4.models import (
    EnrolmentRatio4_1_1, EnrolmentRatioMarksOnly4_1_2,
    SuccessRate, SuccessRateWithBacklogs,
    AcademicPerformance4_3_1, AcademicPerformanceSecondYear, AcademicPerformance4_5_1,
    PlacementandHigherStudies, PlacementRecord,
    ProfessionalActivity, Publication, StudentParticipation
)

class Command(BaseCommand):
    help = 'Dynamically load ALL data from the Criterion 4 ODT file'

    def handle(self, *args, **options):
        file_path = r"c:\Users\AKSHAY RYAKAWAR\OneDrive\Desktop\naac_portal\Criteria No. 4. Students’ Performance.odt"
        self.stdout.write(f"Reading {file_path}...")
        
        try:
            with zipfile.ZipFile(file_path, 'r') as z:
                content = z.read('content.xml')
                root = ET.fromstring(content)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to read ODT: {e}"))
            return

        ns = {
            'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
            'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
            'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
        }

        def get_text(elem):
            return "".join(elem.itertext()).strip()

        tables = []
        for body in root.findall('.//office:body', ns):
            for text_body in body.findall('.//office:text', ns):
                for child in text_body:
                    if child.tag == '{' + ns['table'] + '}table':
                        rows = []
                        for row in child.findall('.//table:table-row', ns):
                            cells = []
                            for cell in row.findall('.//table:table-cell', ns):
                                cell_text = " ".join([get_text(p) for p in cell.findall('.//text:p', ns)]).strip()
                                cells.append(cell_text)
                            rows.append(cells)
                        tables.append(rows)

        self.stdout.write(f"Found {len(tables)} tables. Starting migration...")

        with transaction.atomic():
            # Clear all relevant tables first
            EnrolmentRatio4_1_1.objects.all().delete()
            EnrolmentRatioMarksOnly4_1_2.objects.all().delete()
            SuccessRate.objects.all().delete()
            SuccessRateWithBacklogs.objects.all().delete()
            AcademicPerformance4_3_1.objects.all().delete()
            AcademicPerformanceSecondYear.objects.all().delete()
            AcademicPerformance4_5_1.objects.all().delete()
            PlacementandHigherStudies.objects.all().delete()
            PlacementRecord.objects.all().delete()
            ProfessionalActivity.objects.all().delete()
            Publication.objects.all().delete()
            StudentParticipation.objects.all().delete()

            # --- Table 4.1 Intake (Manual mapping based on extracted data) ---
            EnrolmentRatio4_1_1.objects.create(
                N=120, N1=102, N2=0,
                N_m1=120, N1_m1=115, N2_m1=0,
                N_m2=120, N1_m2=111, N2_m2=0
            )

            # --- Table 4.1.2 Marks ---
            EnrolmentRatioMarksOnly4_1_2.objects.create(
                marks_90=20, marks_80=18, marks_70=16,
                marks_60=12, marks_50=8, marks_below_50=0
            )

            # --- Placement Records (Table 4.6.a) ---
            for table in tables:
                if any("Student Name" in cell for row in table for cell in row):
                    year_label = "Unknown"
                    for row in table:
                        if "Assessment Year" in " ".join(row):
                            year_label = " ".join(row).split(":")[-1].strip()
                            continue
                        if len(row) >= 5 and row[0].isdigit():
                             PlacementRecord.objects.create(
                                assessment_year=year_label,
                                student_name=row[1],
                                enrollment_no=row[2],
                                employer_name=row[3],
                                appointment_no=row[4]
                            )

            # --- Professional Activities (4.7.1) ---
            pa_count = 0
            for table in tables:
                if any("Event Name" in cell for row in table for cell in row) and any("Society" in cell for row in table for cell in row):
                    current_year = "Unknown"
                    for row in table:
                        if "(20" in " ".join(row) and len(row) == 1:
                            current_year = " ".join(row).strip()
                            continue
                        if len(row) >= 5 and row[0].isdigit():
                            date_str = row[1]
                            try:
                                if "/" in date_str:
                                    d = datetime.strptime(date_str, "%d/%m/%Y").date()
                                elif "-" in date_str:
                                    d = datetime.strptime(date_str, "%d-%m-%Y").date()
                                else: d = datetime.now().date()
                            except: d = datetime.now().date()
                            ProfessionalActivity.objects.create(
                                assessment_year=current_year, date=d,
                                event_name=row[2], details=row[3], professional_society=row[4]
                            )
                            pa_count += 1
            self.stdout.write(f"Loaded {pa_count} Professional Activities.")

            # --- Student Participation (4.7.3) ---
            sp_count = 0
            for table in tables:
                if any("Type of Activity" in cell for row in table for cell in row):
                    current_year = "Unknown"
                    for row in table:
                        if "(20" in " ".join(row) and len(row) == 1:
                            current_year = " ".join(row).strip()
                            continue
                        if len(row) >= 8 and row[0].isdigit():
                            StudentParticipation.objects.create(
                                assessment_year=current_year,
                                type_of_activity=row[1], date=row[2],
                                student_name=row[3], organizing_body=row[4],
                                awards=row[5], level=row[6], relevance_peos_pos=row[7]
                            )
                            sp_count += 1
            self.stdout.write(f"Loaded {sp_count} Student Participations.")

            # --- Publications (4.7.2) ---
            for table in tables:
                if any("Publication Description" in cell for row in table for cell in row):
                    for row in table:
                        if len(row) >= 4 and "Description" not in row[0]:
                            Publication.objects.create(
                                publication_description=row[0], year_of_publication=row[1],
                                issue_no=row[2], editor_author=row[3]
                            )

            # --- Success Rates & Academic Performance ---
            sr_data = [
                {'year_label': '2020-21 (LYG m2)', 'X': 130, 'Y': 59},
                {'year_label': '2021-22 (LYG m1)', 'X': 138, 'Y': 41},
                {'year_label': '2022-23 (LYG)', 'X': 135, 'Y': 6},
            ]
            for d in sr_data: SuccessRate.objects.create(**d)

            swb_data = [
                {'year_label': '2018-19 (LYG m2)', 'X': 130, 'Y': 93},
                {'year_label': '2019-20 (LYG m1)', 'X': 138, 'Y': 43},
                {'year_label': '2020-21 (LYG)', 'X': 135, 'Y': 23},
            ]
            for d in swb_data: SuccessRateWithBacklogs.objects.create(**d)

            ap_fy_data = [
                {'year_label': '2020-21 (CAY m3)', 'year': 2020, 'X': 68.71, 'Y': 98, 'Z': 106},
                {'year_label': '2021-22 (CAY m2)', 'year': 2021, 'X': 64.13, 'Y': 45, 'Z': 111},
                {'year_label': '2022-23 (CAY m1)', 'year': 2022, 'X': 66.44, 'Y': 63, 'Z': 115},
            ]
            for d in ap_fy_data: AcademicPerformance4_3_1.objects.create(**d)

            ap_sy_data = [
                {'year_label': '2019-20 (CAY m3)', 'year': 2019, 'X': 75.32, 'Y': 115, 'Z': 138},
                {'year_label': '2020-21 (CAY m2)', 'year': 2020, 'X': 67.38, 'Y': 42, 'Z': 127},
                {'year_label': '2021-22 (CAY m1)', 'year': 2021, 'X': 70.42, 'Y': 20, 'Z': 78},
            ]
            for d in ap_sy_data: AcademicPerformanceSecondYear.objects.create(**d)

            ap_ty_data = [
                {'year_label': '2018-19 (LYG m2)', 'year': 2018, 'X': 83.86, 'Y': 93, 'Z': 104},
                {'year_label': '2019-20 (LYG m1)', 'year': 2019, 'X': 76.49, 'Y': 43, 'Z': 115},
                {'year_label': '2020-21 (LYG)', 'year': 2020, 'X': 74.9, 'Y': 23, 'Z': 42},
            ]
            for d in ap_ty_data: AcademicPerformance4_5_1.objects.create(**d)

            phs_data = [
                {'year_label': '2018-19 (LYG m2)', 'N': 104, 'X': 4, 'Y': 68, 'Z': 1},
                {'year_label': '2019-20 (LYG m1)', 'N': 115, 'X': 5, 'Y': 37, 'Z': 0},
                {'year_label': '2020-21 (LYG)', 'N': 42, 'X': 6, 'Y': 16, 'Z': 0},
            ]
            for d in phs_data: PlacementandHigherStudies.objects.create(**d)

        self.stdout.write(self.style.SUCCESS("Full Data Load Complete!"))
