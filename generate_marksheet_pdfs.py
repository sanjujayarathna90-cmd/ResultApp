import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. SETUP OUTPUT DIRECTORIES
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
base_output_dir = os.path.join(desktop_path, "Grade11_Student_Reports")

dir_11a = os.path.join(base_output_dir, "Class_11-A")
dir_11b = os.path.join(base_output_dir, "Class_11-B")

os.makedirs(dir_11a, exist_ok=True)
os.makedirs(dir_11b, exist_ok=True)

# 2. READ CSV FILE SAFELY
csv_filename = 'Grade11_Marks.csv'

if not os.path.exists(csv_filename):
    print(f"Error: Could not find '{csv_filename}' in current directory.")
    exit()

# Read raw file without assumptions
try:
    raw_df = pd.read_csv(csv_filename, header=None)
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

# Locate header rows (columns containing subject/student headers)
header_rows = []
for idx, row in raw_df.iterrows():
    row_str = " ".join(row.astype(str)).lower()
    if ('name' in row_str or 'student' in row_str) and 'sinhala' in row_str:
        header_rows.append(idx)

# Fallback header search
if not header_rows:
    for idx, row in raw_df.iterrows():
        row_str = " ".join(row.astype(str)).lower()
        if 'name' in row_str or 'student' in row_str:
            header_rows.append(idx)

if not header_rows:
    header_rows = [0]

# Combine data tables across section headers (captures both 11-A and 11-B)
dfs = []
for h_idx in header_rows:
    sub_df = pd.read_csv(csv_filename, skiprows=h_idx)
    sub_df.columns = [str(c).strip() for c in sub_df.columns]
    dfs.append(sub_df)

full_df = pd.concat(dfs, ignore_index=True)

# Auto-detect key columns
name_col = None
for col in full_df.columns:
    if 'name' in col.lower() or 'student' in col.lower():
        name_col = col
        break

if not name_col:
    name_col = full_df.columns[1] if len(full_df.columns) > 1 else full_df.columns[0]

col_map = {str(c).strip().lower(): str(c).strip() for c in full_df.columns}

core_subjects = ['Sinhala', 'Mathematics', 'Buddhism', 'English', 'Science', 'History']
elective_candidates = [
    'Civic Education', 'Civics', 'Geography', 'Tamil', 'Commerce', 'Art', 
    'Dancing', 'Music', 'Health Education', 'Health', 'I.CT', 'ICT', 'Agri', 'Home Science'
]

# Extract and validate all student rows
valid_rows = []
for idx, row in full_df.iterrows():
    val = str(row.get(name_col, '')).strip()
    if val and val.lower() != 'nan' and not val.startswith('?') and '100-75' not in val and 'total' not in val.lower():
        valid_rows.append(row)

# Deduplicate rows by student name
seen_names = set()
unique_student_rows = []
for r in valid_rows:
    s_name = str(r.get(name_col, '')).strip()
    if s_name not in seen_names:
        seen_names.add(s_name)
        unique_student_rows.append(r)

print(f"Total students identified across 11-A & 11-B: {len(unique_student_rows)}")

# 3. REPORTLAB CONFIGURATION
styles = getSampleStyleSheet()
title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=14, alignment=1, spaceAfter=4, textColor=colors.HexColor('#1a365d'))
school_style = ParagraphStyle('SchoolStyle', parent=styles['Normal'], fontSize=9, alignment=1, spaceAfter=8, textColor=colors.HexColor('#4a5568'))
section_style = ParagraphStyle('SectionStyle', parent=styles['Heading2'], fontSize=10, spaceBefore=4, spaceAfter=3, textColor=colors.HexColor('#2c5282'))

count_11a = 0
count_11b = 0

for idx, row in enumerate(unique_student_rows):
    student_name = str(row.get(name_col, '')).strip()
    student_class = str(row.get('Class', row.get('class', '11'))).strip()
    student_no = str(row.get('No.', row.get('no', idx + 1))).strip()
    total_marks = str(row.get('Total', row.get('total', 'N/A'))).strip()
    average_val = row.get('Average', row.get('average', 'N/A'))
    rank_val = str(row.get('Rank', row.get('rank', 'N/A'))).strip()

    # Route output folder based on class tag
    if 'A' in student_class.upper():
        target_folder = dir_11a
        count_11a += 1
    elif 'B' in student_class.upper():
        target_folder = dir_11b
        count_11b += 1
    else:
        # Alternating fallback if Class column is omitted
        if idx % 2 == 0:
            target_folder = dir_11a
            student_class = "11-A"
            count_11a += 1
        else:
            target_folder = dir_11b
            student_class = "11-B"
            count_11b += 1

    clean_name = "".join([c for c in student_name if c.isalnum() or c in (' ', '_')]).strip()
    if not clean_name:
        clean_name = f"Student_{idx+1}"

    pdf_path = os.path.join(target_folder, f"{student_no}_{clean_name}.pdf")

    try:
        avg_str = f"{float(average_val):.2f}%"
    except (ValueError, TypeError):
        avg_str = str(average_val)

    story = []

    # Header
    story.append(Paragraph("<b>R/ THEPPANAWA KUMARA MAHA VIDYALAYA</b>", title_style))
    story.append(Paragraph(f"Grade 11 ({student_class}) - Second Term Student Result Sheet (2026)", school_style))

    # Profile Table
    profile_data = [
        [f"<b>Student Name:</b> {student_name}", f"<b>Class:</b> {student_class}"],
        [f"<b>Student No:</b> {student_no}", f"<b>Class Rank:</b> {rank_val}"],
        [f"<b>Total Marks:</b> {total_marks}", f"<b>Term Average:</b> {avg_str}"]
    ]
    prof_table = Table(profile_data, colWidths=[270, 270])
    prof_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a202c')),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(prof_table)
    story.append(Spacer(1, 6))

    # Parse Marks
    sub_names = []
    current_marks = []
    target_marks = []
    table_rows = [["Subject Name", "Current Mark", "Grade", "Next Term Target"]]

    all_subjects_to_check = core_subjects + elective_candidates

    for sub in all_subjects_to_check:
        sub_key = sub.lower().strip()
        matched_col = col_map.get(sub_key, None)

        if matched_col and matched_col in full_df.columns:
            val = str(row.get(matched_col, '')).strip()

            if val and val.lower() not in ['nan', 'no students', '']:
                try:
                    m = float(val)
                    mark_str = str(int(m))
                    grade = "A" if m >= 75 else "B" if m >= 65 else "C" if m >= 50 else "S" if m >= 35 else "W"
                    target = min(100.0, m + 5.0)
                except ValueError:
                    if val.upper() == "AB":
                        m = 0.0
                        mark_str = "AB"
                        grade = "AB"
                        target = 40.0
                    else:
                        continue

                sub_names.append(sub)
                current_marks.append(m)
                target_marks.append(target)
                table_rows.append([sub, mark_str, grade, str(int(target))])

    res_table = Table(table_rows, colWidths=[180, 100, 80, 180])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b5c8f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('PADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))

    story.append(Paragraph("<b>Subject Marks Breakdown & Future Target Row</b>", section_style))
    story.append(res_table)
    story.append(Spacer(1, 4))

    # Bar Chart
    if len(sub_names) > 0:
        chart_filename = f"temp_chart_{idx}.png"
        x = np.arange(len(sub_names))
        width = 0.35

        fig, ax = plt.subplots(figsize=(7.0, 2.8))
        ax.bar(x - width/2, current_marks, width, label='Current Marks', color='#2b5c8f')
        ax.bar(x + width/2, target_marks, width, label='Next Term Target', color='#e07a5f')

        ax.set_ylabel('Marks', fontsize=8)
        ax.set_title('Subject Performance vs Next Term Expected Targets', fontsize=10, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(sub_names, rotation=20, ha='right', fontsize=8)
        ax.set_ylim(0, 110)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(axis='y', linestyle='--', alpha=0.4)

        for i in range(len(sub_names)):
            if current_marks[i] > 0:
                ax.text(i - width/2, current_marks[i] + 1, str(int(current_marks[i])), ha='center', fontsize=7, fontweight='bold')
            ax.text(i + width/2, target_marks[i] + 1, str(int(target_marks[i])), ha='center', fontsize=7)

        plt.tight_layout()
        plt.savefig(chart_filename, dpi=130)
        plt.close('all')

        story.append(Paragraph("<b>Visual Performance & Target Analysis</b>", section_style))
        story.append(Image(chart_filename, width=460, height=180))

    # Build PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    doc.build(story)

    if len(sub_names) > 0 and os.path.exists(chart_filename):
        os.remove(chart_filename)

print(f"\nProcessing Complete!")
print(f"Generated {count_11a} PDFs for Class 11-A in: {dir_11a}")
print(f"Generated {count_11b} PDFs for Class 11-B in: {dir_11b}")