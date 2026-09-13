import os
import io
import zipfile
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image as PILImage

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="R/ Theppanawa Kumara Maha Vidyalaya - Portal",
    page_icon="🏫",
    layout="wide"
)

# ---------------------------------------------------------
# CONFIGURED LINKS & FILE PATHS
# ---------------------------------------------------------
FACEBOOK_URL = "https://www.facebook.com/share/1LigZjJ72q/"
BING_MAPS_URL = "https://www.bing.com/maps?q=To+Teppanawa+Kumara+Maha+Vidyalaya"

# Media Files
MAIN_VIDEO_PATH = "school_promo_video.mp4"
STANDARDS_VIDEO_PATH = "school_standards_video.mp4"
RIGHT_BANNER_IMAGE = "school_right_banner.jpg"

# PDF Reports
ANNUAL_REPORT_PATH = "Annual_Performance_Report_2026.pdf"
DEVELOPMENT_REPORT_PATH = "School_Development_Progress_Report.pdf"

# PPTX Standard Documents (8 Standards)
STANDARD_FILES = {
    "Standard 1: Basic Information & Context": "Standard_1_Basic_Information.pptx",
    "Standard 2: Student Achievements": "Standard_2_Student_Achievements.pptx",
    "Standard 3: Teaching & Learning Process": "Standard_3_Teaching_Learning.pptx",
    "Standard 4: Curriculum Management": "Standard_4_Curriculum_Management.pptx",
    "Standard 5: School Leadership & Governance": "Standard_5_Leadership_Governance.pptx",
    "Standard 6: Physical & Human Resources": "Standard_6_Resources_Infrastructure.pptx",
    "Standard 7: Student Welfare & Ethics": "Standard_7_Welfare_Ethics.pptx",
    "Standard 8: School & Community Partnership": "Standard_8_Community_Partnership.pptx",
}

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def load_local_bytes(file_path):
    """Safely reads local files for downloads or display."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return f.read()
    return None

def render_video_wall(video_path, caption="School Video Wall"):
    """Displays video wall loop using local file or fallback sample video."""
    video_bytes = load_local_bytes(video_path)
    if video_bytes:
        st.video(video_bytes, format="video/mp4", start_time=0)
    else:
        # Fallback public sample video loop if local file isn't uploaded yet
        st.video("https://www.w3schools.com/html/mov_bbb.mp4")
        st.caption(f"ℹ️ Local file `{video_path}` not found. Displaying fallback preview.")

def render_pptx_slideshow_tab(standard_name, pptx_filename):
    """Renders a download button and slide viewer for PPTX files."""
    st.markdown(f"### 📋 {standard_name}")
    pptx_bytes = load_local_bytes(pptx_filename)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.info("📄 Standard Presentation Document (.pptx)")
        if pptx_bytes:
            st.download_button(
                label=f"⬇️ Download {standard_name} (.pptx)",
                data=pptx_bytes,
                file_name=pptx_filename,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )
        else:
            st.warning(f"File `{pptx_filename}` missing in working directory.")
            st.download_button(
                label="⬇️ Download Sample Template (.pptx)",
                data=b"Sample PPTX placeholder content",
                file_name=pptx_filename,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True,
                disabled=True
            )

    with c2:
        st.subheader("🖼️ Presentation Slideshow Preview")
        if pptx_bytes:
            st.write("Below is the document slide viewer interface:")
            # Display interactive container simulating slide navigation
            slide_no = st.slider(f"Slide Viewer - {standard_name}", min_value=1, max_value=10, value=1, key=pptx_filename)
            
            # Interactive Slide Mock Canvas
            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.set_facecolor('#1a202c')
            ax.text(0.5, 0.6, f"{standard_name}", color='white', ha='center', va='center', fontsize=12, fontweight='bold')
            ax.text(0.5, 0.4, f"Slide {slide_no} / 10 Preview", color='#63b3ed', ha='center', va='center', fontsize=10)
            ax.text(0.5, 0.2, "R/ Theppanawa Kumara Maha Vidyalaya", color='#a0aec0', ha='center', va='center', fontsize=8)
            plt.xticks([])
            plt.yticks([])
            st.pyplot(fig)
        else:
            st.info("Upload your `.pptx` file to activate real-time slide viewing.")

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/school.png", width=80)
st.sidebar.title("R/ Theppanawa KMV")
st.sidebar.caption("Kuruwita, Sabaragamuwa Province")
st.sidebar.markdown("---")

st.sidebar.subheader("📌 Quick Links & Location")
st.sidebar.markdown(f"👉 [Official Facebook Page]({FACEBOOK_URL})")
st.sidebar.markdown(f"📍 [Find School Location on Bing Maps]({BING_MAPS_URL})")

st.sidebar.markdown("---")
navigation = st.sidebar.radio(
    "Navigate To:", 
    [
        "🎓 Result Sheet Generator",
        "🏆 School Standards (08 Quality Indicators)",
        "📅 Events & Notice Board", 
        "📖 School History"
    ]
)

# ---------------------------------------------------------
# 1. RESULT GENERATOR TAB (MAIN PORTAL WITH VIDEO WALL & RIGHT IMAGE)
# ---------------------------------------------------------
if navigation == "🎓 Result Sheet Generator":
    
    # ---------------------------------------------------------
    # MAIN PORTAL HEADER VIDEO WALL & RIGHT SIDE IMAGE
    # ---------------------------------------------------------
    v_left, v_right = st.columns([2.2, 1], gap="medium")
    
    with v_left:
        st.markdown("### 🎥 Main Portal Video Wall")
        render_video_wall(MAIN_VIDEO_PATH, caption="School Main Overview Video")
        
    with v_right:
        st.markdown("### 🏫 School Gallery")
        img_bytes = load_local_bytes(RIGHT_BANNER_IMAGE)
        if img_bytes:
            st.image(img_bytes, use_column_width=True, caption="R/ Theppanawa KMV Campus")
        else:
            st.image("https://images.unsplash.com/photo-1541829070764-84a7d30dd3f3?w=600", use_column_width=True, caption="R/ Theppanawa KMV Premises")

    st.markdown("---")

    # ---------------------------------------------------------
    # 2-COLUMN LOWER FRONT-END LAYOUT
    # ---------------------------------------------------------
    left_col, right_col = st.columns([1, 2.2], gap="large")

    with left_col:
        st.markdown("### 📊 School Overview & Reports")
        st.info("Access official annual performance summaries, school statistics, and administrative downloads.")

        annual_pdf_bytes = load_local_bytes(ANNUAL_REPORT_PATH)
        with st.expander("📄 Annual Performance Report (2025/2026)", expanded=True):
            st.write("Summary of term-wise pass rates and batch performance averages.")
            if annual_pdf_bytes:
                st.download_button(
                    label="⬇️ Download Annual Report (PDF)",
                    data=annual_pdf_bytes,
                    file_name="Annual_Performance_Report_2026.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.warning(f"⚠️ `{ANNUAL_REPORT_PATH}` file missing.")

        dev_pdf_bytes = load_local_bytes(DEVELOPMENT_REPORT_PATH)
        with st.expander("🛠️ School Development Progress"):
            st.write("Overview of infrastructure projects and welfare initiatives.")
            if dev_pdf_bytes:
                st.download_button(
                    label="⬇️ Download Progress Report (PDF)",
                    data=dev_pdf_bytes,
                    file_name="School_Development_Progress_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.warning(f"⚠️ `{DEVELOPMENT_REPORT_PATH}` file missing.")

        st.markdown("---")
        st.markdown("### 🏫 Quick Access")
        st.markdown(f"👉 **[Official Facebook Page]({FACEBOOK_URL})**")
        st.markdown(f"📍 **[To Teppanawa Kumara Maha Vidyalaya - Bing Maps]({BING_MAPS_URL})**")

    with right_col:
        st.title("🎓 Student Result Sheet Generator")
        st.subheader("R/ Theppanawa Kumara Maha Vidyalaya")
        st.write("Upload your marksheet CSV file to generate individual student report cards automatically.")

        # PDF REPORTLAB GENERATION FUNCTION
        def generate_single_pdf(student_row, col_map, core_subjects, elective_candidates, student_name, student_class, student_no, total_marks, average_val, rank_val):
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                pdf_buffer, 
                pagesize=letter, 
                rightMargin=36, 
                leftMargin=36, 
                topMargin=36, 
                bottomMargin=36
            )

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'TitleStyle', 
                parent=styles['Heading1'], 
                fontSize=14, 
                alignment=1, 
                spaceAfter=4, 
                textColor=colors.HexColor('#1a365d')
            )
            school_style = ParagraphStyle(
                'SchoolStyle', 
                parent=styles['Normal'], 
                fontSize=9, 
                alignment=1, 
                spaceAfter=8, 
                textColor=colors.HexColor('#4a5568')
            )
            section_style = ParagraphStyle(
                'SectionStyle', 
                parent=styles['Heading2'], 
                fontSize=10, 
                spaceBefore=4, 
                spaceAfter=3, 
                textColor=colors.HexColor('#2c5282')
            )

            try:
                avg_str = f"{float(average_val):.2f}%"
            except (ValueError, TypeError):
                avg_str = str(average_val)

            story = []
            story.append(Paragraph("<b>R/ THEPPANAWA KUMARA MAHA VIDYALAYA</b>", title_style))
            story.append(Paragraph(f"Grade {student_class} - Student Performance Report Sheet", school_style))

            profile_data = [
                [f"<b>Student Name:</b> {student_name}", f"<b>Class:</b> {student_class}"],
                [f"<b>Student No:</b> {student_no}", f"<b>Class Rank:</b> {rank_val}"],
                [f"<b>Total Marks:</b> {total_marks}", f"<b>Term Average:</b> {avg_str}"]
            ]
            prof_table = Table(profile_data, colWidths=[240, 240])
            prof_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a202c')),
                ('PADDING', (0, 0), (-1, -1), 4),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ]))
            story.append(prof_table)
            story.append(Spacer(1, 6))

            sub_names, current_marks, target_marks = [], [], []
            table_rows = [["Subject Name", "Current Mark", "Grade", "Next Term Target"]]
            all_subjects_to_check = core_subjects + elective_candidates

            for sub in all_subjects_to_check:
                sub_key = sub.lower().strip()
                matched_col = col_map.get(sub_key, None)

                if matched_col and matched_col in student_row.index:
                    val = str(student_row.get(matched_col, '')).strip()
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

            res_table = Table(table_rows, colWidths=[160, 90, 70, 160])
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

            if len(sub_names) > 0:
                x = np.arange(len(sub_names))
                width = 0.35

                fig, ax = plt.subplots(figsize=(6.5, 2.6))
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
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=130)
                plt.close(fig)
                img_buffer.seek(0)

                story.append(Paragraph("<b>Visual Performance & Target Analysis</b>", section_style))
                story.append(RLImage(img_buffer, width=440, height=170))

            doc.build(story)
            pdf_buffer.seek(0)
            return pdf_buffer.getvalue()

        # CSV Upload Section
        uploaded_file = st.file_uploader("Choose a Marksheet CSV file", type=["csv"])

        if uploaded_file is not None:
            try:
                raw_df = pd.read_csv(uploaded_file, header=None)
                header_rows = []
                for idx, row in raw_df.iterrows():
                    row_str = " ".join(row.astype(str)).lower()
                    if ('name' in row_str or 'student' in row_str) and 'sinhala' in row_str:
                        header_rows.append(idx)
                if not header_rows:
                    header_rows = [0]

                uploaded_file.seek(0)
                dfs = []
                for h_idx in header_rows:
                    sub_df = pd.read_csv(uploaded_file, skiprows=h_idx)
                    sub_df.columns = [str(c).strip() for c in sub_df.columns]
                    dfs.append(sub_df)

                full_df = pd.concat(dfs, ignore_index=True)
            except Exception as e:
                st.error(f"Error reading CSV file: {e}")
                st.stop()

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

            valid_rows = []
            for idx, row in full_df.iterrows():
                val = str(row.get(name_col, '')).strip()
                if val and val.lower() != 'nan' and not val.startswith('?') and '100-75' not in val and 'total' not in val.lower():
                    valid_rows.append(row)

            seen_names = set()
            unique_rows = []
            for r in valid_rows:
                s_name = str(r.get(name_col, '')).strip()
                if s_name not in seen_names:
                    seen_names.add(s_name)
                    unique_rows.append(r)

            st.success(f"Loaded {len(unique_rows)} student records!")

            m1, m2 = st.columns(2)
            with m1:
                st.metric(label="Processed Students", value=len(unique_rows))
            with m2:
                classes = list(set([str(r.get('Class', r.get('class', '11'))).strip() for r in unique_rows]))
                st.metric(label="Classes", value=", ".join(classes) if classes else "11")

            # Single Student Download Selector
            st.markdown("### 📄 Download Single Student PDF")
            student_names = [str(r.get(name_col, '')).strip() for r in unique_rows]
            selected_student = st.selectbox("Select Student:", student_names)

            if selected_student:
                selected_index = student_names.index(selected_student)
                s_row = unique_rows[selected_index]

                s_class = str(s_row.get('Class', s_row.get('class', '11'))).strip()
                s_no = str(s_row.get('No.', s_row.get('no', selected_index + 1))).strip()
                total = str(s_row.get('Total', s_row.get('total', 'N/A'))).strip()
                avg = s_row.get('Average', s_row.get('average', 'N/A'))
                rank = str(s_row.get('Rank', s_row.get('rank', 'N/A'))).strip()

                single_pdf_bytes = generate_single_pdf(
                    s_row, col_map, core_subjects, elective_candidates, 
                    selected_student, s_class, s_no, total, avg, rank
                )
                
                clean_selected_name = "".join([c for c in selected_student if c.isalnum() or c in (' ', '_')]).strip()
                st.download_button(
                    label=f"⬇️ Download Report for {selected_student}",
                    data=single_pdf_bytes,
                    file_name=f"{s_no}_{clean_selected_name}.pdf",
                    mime="application/pdf"
                )

# ---------------------------------------------------------
# 2. SCHOOL STANDARDS TAB (08 SUB-TABS & STANDARDS VIDEO WALL)
# ---------------------------------------------------------
elif navigation == "🏆 School Standards (08 Quality Indicators)":
    st.title("🏆 Institutional Quality & School Standards")
    st.write("Official documentation, evaluations, and presentation slide decks for Sabaragamuwa Province Education Quality Assurance.")

    # Dedicated Standards Video Wall
    st.markdown("### 🎥 School Standards Video Wall")
    render_video_wall(STANDARDS_VIDEO_PATH, caption="Quality Standard Implementation Video")
    st.markdown("---")

    st.subheader("📑 Select School Standard Indicator")

    # Create 08 Sub-Tabs for each Standard
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Std 1: Context", 
        "Std 2: Achievement", 
        "Std 3: Teaching", 
        "Std 4: Curriculum", 
        "Std 5: Governance", 
        "Std 6: Resources", 
        "Std 7: Welfare", 
        "Std 8: Community"
    ])

    standard_keys = list(STANDARD_FILES.keys())

    with tab1:
        render_pptx_slideshow_tab(standard_keys[0], STANDARD_FILES[standard_keys[0]])
    with tab2:
        render_pptx_slideshow_tab(standard_keys[1], STANDARD_FILES[standard_keys[1]])
    with tab3:
        render_pptx_slideshow_tab(standard_keys[2], STANDARD_FILES[standard_keys[2]])
    with tab4:
        render_pptx_slideshow_tab(standard_keys[3], STANDARD_FILES[standard_keys[3]])
    with tab5:
        render_pptx_slideshow_tab(standard_keys[4], STANDARD_FILES[standard_keys[4]])
    with tab6:
        render_pptx_slideshow_tab(standard_keys[5], STANDARD_FILES[standard_keys[5]])
    with tab7:
        render_pptx_slideshow_tab(standard_keys[6], STANDARD_FILES[standard_keys[6]])
    with tab8:
        render_pptx_slideshow_tab(standard_keys[7], STANDARD_FILES[standard_keys[7]])

# ---------------------------------------------------------
# 3. EVENTS & NOTICE BOARD TAB
# ---------------------------------------------------------
elif navigation == "📅 Events & Notice Board":
    st.title("📅 Events & Public Notice Board")
    st.subheader("R/ Theppanawa Kumara Maha Vidyalaya")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("### 📢 Upcoming School Events & Notices")
        st.markdown("#### 📝 Second Term Evaluation Examinations")
        st.write("All Grade 6 to Grade 11 term evaluation exams will commence shortly.")
        st.markdown("---")
        st.markdown("#### 🧹 Community & School Welfare Cleaning Drive")
        st.write("Joint initiative organized by the School Welfare Association and Development Office.")
    with c2:
        st.markdown("### 🔗 Quick Links")
        st.markdown(f"👉 **[Official Facebook Page]({FACEBOOK_URL})**")
        st.markdown(f"📍 **[To Teppanawa Kumara Maha Vidyalaya - Bing Maps]({BING_MAPS_URL})**")

# ---------------------------------------------------------
# 4. SCHOOL HISTORY TAB
# ---------------------------------------------------------
elif navigation == "📖 School History":
    st.title("📖 School History & Heritage")
    st.subheader("R/ Theppanawa Kumara Maha Vidyalaya")
    st.markdown("""
    **R/ Theppanawa Kumara Maha Vidyalaya** is located in Kuruwita, Sabaragamuwa Province, Sri Lanka. 
    Dedicated to fostering academic excellence, moral values, and community development.
    """)
    st.markdown("---")
    st.markdown(f"📍 Map Location: **[To Teppanawa Kumara Maha Vidyalaya - Bing Maps]({BING_MAPS_URL})**")