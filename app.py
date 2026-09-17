import base64
import io
import os
import time
import zipfile
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image as RLImage,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

matplotlib.use("Agg")

# ---------------------------------------------------------
# PAGE CONFIGURATION (MUST BE AT THE VERY TOP)
# ---------------------------------------------------------
st.set_page_config(
    page_title="R/ Theppanawa Kumara Maha Vidyalaya - Portal",
    page_icon="🏫",
    layout="wide",
)

# ---------------------------------------------------------
# 1. TOP HEADER WITH SCHOOL LOGO (LEFT) & TITLE
# ---------------------------------------------------------
LOGO_PATH = os.path.join("images", "logo.png")

col_logo, col_title = st.columns([1, 5])

with col_logo:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)

with col_title:
    st.title("R/ Theppanawa Kumara Maha Vidyalaya")
    st.caption("School Management, Publications & Evaluation Portal")

st.markdown("---")

# ---------------------------------------------------------
# 2. ROTATING TRANSPARENT BACKGROUND SLIDESHOW
# ---------------------------------------------------------
BG_DIR = os.path.join("images", "Backgrounds")
VALID_EXTS = (".jpg", ".jpeg", ".png", ".webp")

if os.path.exists(BG_DIR):
    bg_images = [
        os.path.join(BG_DIR, f)
        for f in os.listdir(BG_DIR)
        if f.lower().endswith(VALID_EXTS)
    ]

    if bg_images:
        if "bg_index" not in st.session_state:
            st.session_state.bg_index = 0
            st.session_state.last_bg_update = time.time()

        current_time = time.time()
        if current_time - st.session_state.last_bg_update > 15:
            st.session_state.bg_index = (
                st.session_state.bg_index + 1
            ) % len(bg_images)
            st.session_state.last_bg_update = current_time
            st.rerun()

        current_bg = bg_images[st.session_state.bg_index]
        with open(current_bg, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        # UPDATED: Lowered white overlay to 0.43 (50% more image visibility)
        bg_css = f"""
        <style>
        .stApp {{
            background: linear-gradient(
                rgba(255, 255, 255, 0.43), 
                rgba(255, 255, 255, 0.43)
            ), 
            url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        </style>
        """
        st.markdown(bg_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# CONFIGURED LINKS & FILE PATHS
# ---------------------------------------------------------
FACEBOOK_URL = "https://www.facebook.com/share/1LigZjJ72q/"
BING_MAPS_URL = (
    "https://www.bing.com/maps?q=To+Teppanawa+Kumara+Maha+Vidyalaya"
)

# Media Files
MAIN_VIDEO_PATH = "school_promo_video.mp4"
STANDARDS_VIDEO_PATH = "school_standards_video.mp4"
RIGHT_BANNER_IMAGE = "school_right_banner.jpg"

# PDF Reports
ANNUAL_REPORT_PATH = "Annual_Performance_Report_2026.pdf"
DEVELOPMENT_REPORT_PATH = "School_Development_Progress_Report.pdf"

# Standard Documents
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
# SAMPLE DATA FOR PUBLICATIONS & NEWS
# ---------------------------------------------------------
PUBLICATIONS_DATA = [
    {
        "id": "pub_1",
        "title": "Annual Academic Research Journal 2025/2026",
        "category": "Research Journal",
        "date": "2026-01-15",
        "author": "Academic Development Committee",
        "summary": "A comprehensive compilation of action research, teaching methodologies, and educational insights contributed by the faculty of R/ Theppanawa KMV.",
        "file_path": "publications/Annual_Journal_2026.pdf",
        "content_text": """
        R/ THEPPANAWA KUMARA MAHA VIDYALAYA
        ANNUAL ACADEMIC RESEARCH JOURNAL (2025/2026)
        
        Executive Summary:
        This volume highlights key pedagogical developments, primary education improvements,
        and student-centered learning strategies implemented across grades 1-11.
        
        Key Topics:
        1. Enhancing Mathematics Literacy in Secondary Grades
        2. Integrating Technology in Rural School Classrooms
        3. Behavioral Economics and Student Engagement Strategies
        """,
    },
    {
        "id": "pub_2",
        "title": "School Magazine - 'Kumara Prabha' (2025 Edition)",
        "category": "School Magazine",
        "date": "2025-12-10",
        "author": "Student Editorial Board",
        "summary": "Features creative writing, poetry, artwork, and sports achievements by students of all grade levels.",
        "file_path": "publications/Kumara_Prabha_2025.pdf",
        "content_text": """
        'KUMARA PRABHA' SCHOOL MAGAZINE
        
        Features:
        - Creative Short Stories and Poems in Sinhala, English, and Tamil
        - Annual Sports Meet Highlights & Records
        - Art Gallery & Cultural Event Showcase
        """,
    },
    {
        "id": "pub_3",
        "title": "School Development Strategic Plan 2024-2028",
        "category": "Policy & Planning",
        "date": "2024-03-01",
        "author": "Principal & School Development Society",
        "summary": "5-year roadmap for infrastructure enhancement, ICT lab expansion, and community engagement.",
        "file_path": "publications/Strategic_Plan_2024_2028.pdf",
        "content_text": """
        STRATEGIC DEVELOPMENT PLAN (2024 - 2028)
        
        Pillars:
        1. Infrastructure Upgrades: New English Activity Room & Science Lab extension.
        2. Teacher Professional Development.
        3. Sustainable Community & Environment Projects.
        """,
    },
]

NEWS_DATA = [
    {
        "id": "news_1",
        "title": "Inauguration of New English Activity Room",
        "date": "2026-08-19",
        "category": "Facilities & Infrastructure",
        "author": "Development Officer",
        "summary": "The newly built English Activity Room was officially declared open, boosting language learning resources for students.",
        "details": """
        The inauguration ceremony for the new English Activity Room was successfully held at R/ Theppanawa Kumara Maha Vidyalaya on August 19, 2026. 
        
        The facility features interactive learning stations, language software equipment, and a curated library of English readers to promote communicative language skills among students from Grade 1 to Grade 11.
        
        Special thanks to the Ministry of Education, Sabaragamuwa Provincial Council, and the School Development Society for their support.
        """,
        "file_path": "news/English_Activity_Room_Opening.pdf",
    },
    {
        "id": "news_2",
        "title": "Post-Flood School Restoration Drive Completed",
        "date": "2026-01-14",
        "category": "Community Service",
        "author": "Welfare Committee",
        "summary": "Teachers, parents, and local volunteers collaborated to complete a comprehensive cleanup operation following heavy rains.",
        "details": """
        Following recent heavy rainfall, an organized cleanup drive took place on January 13, 2026, at R/ Theppanawa Kumara Maha Vidyalaya. 
        
        Thanks to the prompt action of over 80 volunteers—including teachers, parents, past pupils, and community members—the school premises, classrooms, and playgrounds were safely restored and disinfected.
        """,
        "file_path": "news/Cleanup_Drive_Report_2026.pdf",
    },
    {
        "id": "news_3",
        "title": "Second Term Evaluation Examinations Announced",
        "date": "2026-09-01",
        "category": "Academic Announcement",
        "author": "Exam Unit",
        "summary": "Timetable and key guidelines released for Grade 6 to 11 term evaluations.",
        "details": """
        The Second Term Evaluation Examinations for the 2026 academic year are scheduled to begin shortly. 
        
        All students are requested to review their subject study guides. Parents can access student progress reports and timetables directly via the school result generator portal.
        """,
        "file_path": "news/Exam_Notice_Term_2_2026.pdf",
    },
]

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def load_local_bytes(file_path):
    """Safely reads local files for downloads or display."""
    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return f.read()
    return None


def render_video_wall(video_path, caption="School Video Wall"):
    """Displays video wall loop using local file or fallback sample video."""
    video_bytes = load_local_bytes(video_path)
    if video_bytes:
        st.video(video_bytes, format="video/mp4", start_time=0)
    else:
        st.video("https://www.w3schools.com/html/mov_bbb.mp4")
        st.caption(f"ℹ️ Preview Mode - Local video file `{video_path}`.")


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
                use_container_width=True,
            )
        else:
            st.warning(f"File `{pptx_filename}` missing in directory.")
            st.download_button(
                label="⬇️ Download Sample Template (.pptx)",
                data=b"Sample PPTX placeholder content",
                file_name=pptx_filename,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True,
                disabled=True,
            )

    with c2:
        st.subheader("🖼️ Presentation Slideshow Preview")
        slide_no = st.slider(
            f"Slide Viewer - {standard_name}",
            min_value=1,
            max_value=10,
            value=1,
            key=pptx_filename,
        )

        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.set_facecolor("#1a202c")
        ax.text(
            0.5,
            0.6,
            f"{standard_name}",
            color="white",
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
        )
        ax.text(
            0.5,
            0.4,
            f"Slide {slide_no} / 10 Preview",
            color="#63b3ed",
            ha="center",
            va="center",
            fontsize=10,
        )
        ax.text(
            0.5,
            0.2,
            "R/ Theppanawa Kumara Maha Vidyalaya",
            color="#a0aec0",
            ha="center",
            va="center",
            fontsize=8,
        )
        plt.xticks([])
        plt.yticks([])
        st.pyplot(fig)


def render_gallery():
    """Renders the Photo Gallery page with 3-column grid and image uploader."""
    st.header("📸 School Photo Gallery & Media Center")
    
    base_gallery_dir = "images"
    gallery_categories = ["Academic", "Events", "Infrastructure", "Sports"]
    
    if not os.path.exists(base_gallery_dir):
        os.makedirs(base_gallery_dir)
        
    for category in gallery_categories:
        cat_path = os.path.join(base_gallery_dir, category)
        if not os.path.exists(cat_path):
            os.makedirs(cat_path)

    selected_category = st.radio(
        "Select Category", 
        ["All Categories"] + gallery_categories, 
        horizontal=True
    )

    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    image_list = []
    target_categories = gallery_categories if selected_category == "All Categories" else [selected_category]

    for cat in target_categories:
        folder_path = os.path.join(base_gallery_dir, cat)
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.lower().endswith(valid_extensions):
                    img_full_path = os.path.join(folder_path, file)
                    image_list.append((img_full_path, cat, file))

    if image_list:
        st.write(f"Showing **{len(image_list)}** photo(s):")
        cols = st.columns(3)
        for idx, (img_path, cat, img_name) in enumerate(image_list):
            with cols[idx % 3]:
                try:
                    image = PILImage.open(img_path)
                    st.image(image, caption=f"[{cat}] {img_name}", use_container_width=True)
                except Exception:
                    st.error(f"Could not load {img_name}")
    else:
        st.warning(
            f"No photos found in `images/{selected_category if selected_category != 'All Categories' else ''}`. "
            "Add .jpg or .png files to these subfolders or use the uploader below."
        )

    st.markdown("---")
    st.subheader("📤 Upload Photo to Category")
    col_upload, col_select = st.columns([2, 1])
    with col_upload:
        uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg', 'webp'])
    with col_select:
        target_folder = st.selectbox("Select Target Folder", gallery_categories)

    if uploaded_file and st.button("Save Photo to Gallery", type="primary"):
        save_directory = os.path.join(base_gallery_dir, target_folder)
        save_path = os.path.join(save_directory, uploaded_file.name)
        
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        st.success(f"Saved `{uploaded_file.name}` to `images/{target_folder}/`!")
        st.rerun()

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
        "📸 Photo Gallery",
        "📚 Publications & Journals",
        "📰 News & Press Releases",
        "🏆 School Standards (08 Quality Indicators)",
        "📅 Events & Notice Board",
        "📖 School History",
    ],
)

# ---------------------------------------------------------
# 1. RESULT GENERATOR TAB
# ---------------------------------------------------------
if navigation == "🎓 Result Sheet Generator":
    v_left, v_right = st.columns([2.2, 1], gap="medium")

    with v_left:
        st.markdown("### 🎥 Main Portal Video Wall")
        render_video_wall(MAIN_VIDEO_PATH, caption="School Main Overview Video")

    with v_right:
        st.markdown("### 🏫 School Gallery")
        img_bytes = load_local_bytes(RIGHT_BANNER_IMAGE)
        if img_bytes:
            st.image(
                img_bytes,
                use_container_width=True,
                caption="R/ Theppanawa KMV Campus",
            )
        else:
            st.image(
                "https://images.unsplash.com/photo-1541829070764-84a7d30dd3f3?w=600",
                use_container_width=True,
                caption="R/ Theppanawa KMV Premises",
            )

    st.markdown("---")

    left_col, right_col = st.columns([1, 2.2], gap="large")

    with left_col:
        st.markdown("### 📊 School Overview & Reports")
        st.info(
            "Access official annual performance summaries, school statistics, and administrative downloads."
        )

        annual_pdf_bytes = load_local_bytes(ANNUAL_REPORT_PATH)
        with st.expander("📄 Annual Performance Report (2025/2026)", expanded=True):
            st.write("Summary of term-wise pass rates and batch performance averages.")
            if annual_pdf_bytes:
                st.download_button(
                    label="⬇️ Download Annual Report (PDF)",
                    data=annual_pdf_bytes,
                    file_name="Annual_Performance_Report_2026.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            else:
                st.download_button(
                    label="⬇️ Download Summary Statement (Text)",
                    data="R/ Theppanawa KMV - Annual Performance Report 2026 Summary",
                    file_name="Annual_Report_Summary.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

        dev_pdf_bytes = load_local_bytes(DEVELOPMENT_REPORT_PATH)
        with st.expander("🛠️ School Development Progress"):
            st.write("Overview of infrastructure projects and welfare initiatives.")
            if dev_pdf_bytes:
                st.download_button(
                    label="⬇️ Download Progress Report (PDF)",
                    data=dev_pdf_bytes,
                    file_name="School_Development_Progress_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            else:
                st.download_button(
                    label="⬇️ Download Development Summary (Text)",
                    data="R/ Theppanawa KMV - Development Progress Overview",
                    file_name="Development_Progress.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

    with right_col:
        st.title("🎓 Student Result Sheet Generator")
        st.write(
            "Upload your marksheet CSV file to generate individual student report cards automatically."
        )

        def generate_single_pdf(
            student_row,
            col_map,
            core_subjects,
            elective_candidates,
            student_name,
            student_class,
            student_no,
            total_marks,
            average_val,
            rank_val,
        ):
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                pdf_buffer,
                pagesize=letter,
                rightMargin=36,
                leftMargin=36,
                topMargin=36,
                bottomMargin=36,
            )

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "TitleStyle",
                parent=styles["Heading1"],
                fontSize=14,
                alignment=1,
                spaceAfter=4,
                textColor=colors.HexColor("#1a365d"),
            )
            school_style = ParagraphStyle(
                "SchoolStyle",
                parent=styles["Normal"],
                fontSize=9,
                alignment=1,
                spaceAfter=8,
                textColor=colors.HexColor("#4a5568"),
            )
            section_style = ParagraphStyle(
                "SectionStyle",
                parent=styles["Heading2"],
                fontSize=10,
                spaceBefore=4,
                spaceAfter=3,
                textColor=colors.HexColor("#2c5282"),
            )

            try:
                avg_str = f"{float(average_val):.2f}%"
            except (ValueError, TypeError):
                avg_str = str(average_val)

            story = [
                Paragraph("<b>R/ THEPPANAWA KUMARA MAHA VIDYALAYA</b>", title_style),
                Paragraph(
                    f"Grade {student_class} - Student Performance Report Sheet",
                    school_style,
                ),
            ]

            profile_data = [
                [f"<b>Student Name:</b> {student_name}", f"<b>Class:</b> {student_class}"],
                [f"<b>Student No:</b> {student_no}", f"<b>Class Rank:</b> {rank_val}"],
                [f"<b>Total Marks:</b> {total_marks}", f"<b>Term Average:</b> {avg_str}"],
            ]
            prof_table = Table(profile_data, colWidths=[240, 240])
            prof_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7fafc")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1a202c")),
                    ("PADDING", (0, 0), (-1, -1), 4),
                    ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e0")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ])
            )
            story.append(prof_table)
            story.append(Spacer(1, 6))

            sub_names, current_marks, target_marks = [], [], []
            table_rows = [["Subject Name", "Current Mark", "Grade", "Next Term Target"]]
            all_subjects_to_check = core_subjects + elective_candidates

            for sub in all_subjects_to_check:
                sub_key = sub.lower().strip()
                matched_col = col_map.get(sub_key, None)

                if matched_col and matched_col in student_row.index:
                    val = str(student_row.get(matched_col, "")).strip()
                    if val and val.lower() not in ["nan", "no students", ""]:
                        try:
                            m = float(val)
                            mark_str = str(int(m))
                            grade = (
                                "A" if m >= 75
                                else "B" if m >= 65
                                else "C" if m >= 50
                                else "S" if m >= 35
                                else "W"
                            )
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
            res_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2b5c8f")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("ALIGN", (0, 0), (0, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("PADDING", (0, 0), (-1, -1), 3),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.HexColor("#f8fafc")],
                    ),
                ])
            )

            story.append(
                Paragraph("<b>Subject Marks Breakdown & Future Targets</b>", section_style)
            )
            story.append(res_table)
            story.append(Spacer(1, 4))

            if len(sub_names) > 0:
                x = np.arange(len(sub_names))
                width = 0.35

                fig, ax = plt.subplots(figsize=(6.5, 2.6))
                ax.bar(x - width / 2, current_marks, width, label="Current Marks", color="#2b5c8f")
                ax.bar(x + width / 2, target_marks, width, label="Next Term Target", color="#e07a5f")

                ax.set_ylabel("Marks", fontsize=8)
                ax.set_title("Subject Performance vs Expected Targets", fontsize=10, fontweight="bold")
                ax.set_xticks(x)
                ax.set_xticklabels(sub_names, rotation=20, ha="right", fontsize=8)
                ax.set_ylim(0, 110)
                ax.legend(loc="upper right", fontsize=8)
                ax.grid(axis="y", linestyle="--", alpha=0.4)

                plt.tight_layout()
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format="png", dpi=130)
                plt.close(fig)
                img_buffer.seek(0)

                story.append(Paragraph("<b>Visual Performance Analysis</b>", section_style))
                story.append(RLImage(img_buffer, width=440, height=170))

            doc.build(story)
            pdf_buffer.seek(0)
            return pdf_buffer.getvalue()

        uploaded_file = st.file_uploader("Choose a Marksheet CSV file", type=["csv"])

        if uploaded_file is not None:
            try:
                raw_df = pd.read_csv(uploaded_file, header=None)
                header_rows = []
                for idx, row in raw_df.iterrows():
                    row_str = " ".join(row.astype(str)).lower()
                    if ("name" in row_str or "student" in row_str) and "sinhala" in row_str:
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

            name_col = next(
                (col for col in full_df.columns if "name" in col.lower() or "student" in col.lower()),
                full_df.columns[1] if len(full_df.columns) > 1 else full_df.columns[0],
            )

            col_map = {str(c).strip().lower(): str(c).strip() for c in full_df.columns}
            core_subjects = ["Sinhala", "Mathematics", "Buddhism", "English", "Science", "History"]
            elective_candidates = [
                "Civic Education", "Civics", "Geography", "Tamil", "Commerce",
                "Art", "Dancing", "Music", "Health Education", "Health",
                "I.CT", "ICT", "Agri", "Home Science",
            ]

            valid_rows = [
                row for idx, row in full_df.iterrows()
                if str(row.get(name_col, "")).strip()
                and str(row.get(name_col, "")).strip().lower() != "nan"
                and not str(row.get(name_col, "")).strip().startswith("?")
            ]

            seen_names = set()
            unique_rows = []
            for r in valid_rows:
                s_name = str(r.get(name_col, "")).strip()
                if s_name not in seen_names:
                    seen_names.add(s_name)
                    unique_rows.append(r)

            st.success(f"Loaded {len(unique_rows)} student records!")

            student_names = [str(r.get(name_col, "")).strip() for r in unique_rows]
            selected_student = st.selectbox("Select Student:", student_names)

            if selected_student:
                selected_index = student_names.index(selected_student)
                s_row = unique_rows[selected_index]

                s_class = str(s_row.get("Class", s_row.get("class", "11"))).strip()
                s_no = str(s_row.get("No.", s_row.get("no", selected_index + 1))).strip()
                total = str(s_row.get("Total", s_row.get("total", "N/A"))).strip()
                avg = s_row.get("Average", s_row.get("average", "N/A"))
                rank = str(s_row.get("Rank", s_row.get("rank", "N/A"))).strip()

                single_pdf_bytes = generate_single_pdf(
                    s_row, col_map, core_subjects, elective_candidates,
                    selected_student, s_class, s_no, total, avg, rank
                )

                clean_selected_name = "".join(
                    [c for c in selected_student if c.isalnum() or c in (" ", "_")]
                ).strip()

                st.download_button(
                    label=f"⬇️ Download Report for {selected_student}",
                    data=single_pdf_bytes,
                    file_name=f"{s_no}_{clean_selected_name}.pdf",
                    mime="application/pdf",
                )

                # Batch Export Option for All Students
                st.markdown("---")
                if st.button("📦 Batch Generate All Class PDF Reports (.zip)"):
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                        for idx, r in enumerate(unique_rows):
                            cur_name = str(r.get(name_col, "")).strip()
                            cur_class = str(r.get("Class", r.get("class", "11"))).strip()
                            cur_no = str(r.get("No.", r.get("no", idx + 1))).strip()
                            cur_total = str(r.get("Total", r.get("total", "N/A"))).strip()
                            cur_avg = r.get("Average", r.get("average", "N/A"))
                            cur_rank = str(r.get("Rank", r.get("rank", "N/A"))).strip()

                            pdf_data = generate_single_pdf(
                                r, col_map, core_subjects, elective_candidates,
                                cur_name, cur_class, cur_no, cur_total, cur_avg, cur_rank
                            )
                            clean_filename = "".join([c for c in cur_name if c.isalnum() or c in (" ", "_")]).strip()
                            zf.writestr(f"{cur_no}_{clean_filename}.pdf", pdf_data)

                    zip_buffer.seek(0)
                    st.download_button(
                        label="⬇️ Download Batch Zip File",
                        data=zip_buffer.getvalue(),
                        file_name="All_Student_Reports.zip",
                        mime="application/zip",
                    )

# ---------------------------------------------------------
# 2. PHOTO GALLERY TAB
# ---------------------------------------------------------
elif navigation == "📸 Photo Gallery":
    render_gallery()

# ---------------------------------------------------------
# 3. PUBLICATIONS & JOURNALS TAB
# ---------------------------------------------------------
elif navigation == "📚 Publications & Journals":
    st.title("📚 School Publications & Academic Journals")
    st.caption("Read official school magazines, research journals, and policy plans online or download them.")

    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 Search publications by title, author, or keyword...", "")
    with col_filter:
        categories = ["All"] + list(set([p["category"] for p in PUBLICATIONS_DATA]))
        selected_cat = st.selectbox("Filter Category:", categories)

    filtered_pubs = PUBLICATIONS_DATA
    if selected_cat != "All":
        filtered_pubs = [p for p in filtered_pubs if p["category"] == selected_cat]
    if search_query:
        filtered_pubs = [
            p for p in filtered_pubs
            if search_query.lower() in p["title"].lower()
            or search_query.lower() in p["summary"].lower()
            or search_query.lower() in p["author"].lower()
        ]

    st.markdown("---")

    if not filtered_pubs:
        st.info("No publications match your search criteria.")
    else:
        for pub in filtered_pubs:
            with st.container():
                st.markdown(f"### 📄 {pub['title']}")
                c_meta1, c_meta2, c_meta3 = st.columns(3)
                c_meta1.caption(f"📅 **Date:** {pub['date']}")
                c_meta2.caption(f"✍️ **Author:** {pub['author']}")
                c_meta3.caption(f"🏷️ **Category:** `{pub['category']}`")

                st.write(pub["summary"])

                with st.expander("📖 Read Online & View Details", expanded=False):
                    st.markdown("#### Document Preview & Excerpt")
                    st.text_area(
                        "Document Content Preview",
                        value=pub["content_text"],
                        height=160,
                        disabled=True,
                        key=f"text_{pub['id']}",
                    )

                pub_bytes = load_local_bytes(pub["file_path"])
                if pub_bytes:
                    st.download_button(
                        label=f"⬇️ Download Full Document ({pub['title']}.pdf)",
                        data=pub_bytes,
                        file_name=os.path.basename(pub["file_path"]),
                        mime="application/pdf",
                        key=f"dl_{pub['id']}",
                    )
                else:
                    fallback_text = f"{pub['title']}\nAuthor: {pub['author']}\nDate: {pub['date']}\n\n{pub['summary']}\n\n{pub['content_text']}"
                    st.download_button(
                        label="⬇️ Download Summary Article (.txt)",
                        data=fallback_text.encode("utf-8"),
                        file_name=f"{pub['id']}_summary.txt",
                        mime="text/plain",
                        key=f"dl_txt_{pub['id']}",
                    )

                st.markdown("---")

# ---------------------------------------------------------
# 4. NEWS & PRESS RELEASES TAB
# ---------------------------------------------------------
elif navigation == "📰 News & Press Releases":
    st.title("📰 School News & Official Announcements")
    st.caption("Stay updated with recent school developments, community activities, and notices.")

    news_col, archive_col = st.columns([2.2, 1], gap="large")

    with news_col:
        st.subheader("🔥 Latest News Updates")

        for news in NEWS_DATA:
            with st.container():
                st.markdown(f"### {news['title']}")
                st.caption(f"🗓️ Published: **{news['date']}** | ✍️ **{news['author']}** | 🏷️ `{news['category']}`")
                st.write(news["summary"])

                with st.expander("📖 Read Full News Article"):
                    st.markdown(news["details"])

                news_bytes = load_local_bytes(news["file_path"])
                if news_bytes:
                    st.download_button(
                        label="⬇️ Download News Release PDF",
                        data=news_bytes,
                        file_name=os.path.basename(news["file_path"]),
                        mime="application/pdf",
                        key=f"news_dl_{news['id']}",
                    )
                else:
                    news_text_download = f"{news['title']}\nDate: {news['date']}\nAuthor: {news['author']}\nCategory: {news['category']}\n\n{news['summary']}\n\n{news['details']}"
                    st.download_button(
                        label="⬇️ Download News Notice (.txt)",
                        data=news_text_download.encode("utf-8"),
                        file_name=f"{news['id']}_notice.txt",
                        mime="text/plain",
                        key=f"news_dl_txt_{news['id']}",
                    )

                st.markdown("---")

    with archive_col:
        st.subheader("🗂️ News Categories")
        st.markdown("- 🏫 **Facilities & Infrastructure**")
        st.markdown("- 🤝 **Community Service**")
        st.markdown("- 📝 **Academic Announcements**")
        st.markdown("- 🏆 **Sports & Co-curricular**")

        st.markdown("---")
        st.subheader("📌 Contact Press Unit")
        st.info("For official press queries or updates, contact the School Media and Communications Committee.")

# ---------------------------------------------------------
# 5. SCHOOL STANDARDS TAB
# ---------------------------------------------------------
elif navigation == "🏆 School Standards (08 Quality Indicators)":
    st.title("🏆 School Quality Evaluation Standards")
    st.caption("Review official evaluation presentations and standard criteria across the 08 quality indicators.")

    st.markdown("### 🎥 Standards Framework Presentation")
    render_video_wall(STANDARDS_VIDEO_PATH, caption="School Standards Overview Video")

    st.markdown("---")
    tabs = st.tabs(list(STANDARD_FILES.keys()))

    for idx, (std_name, pptx_file) in enumerate(STANDARD_FILES.items()):
        with tabs[idx]:
            render_pptx_slideshow_tab(std_name, pptx_file)

# ---------------------------------------------------------
# 6. EVENTS & NOTICE BOARD TAB
# ---------------------------------------------------------
elif navigation == "📅 Events & Notice Board":
    st.title("📅 School Calendar & Notice Board")
    st.caption("Upcoming term schedules, examinations, and institutional events.")

    e1, e2 = st.columns(2)

    with e1:
        st.subheader("📌 Upcoming Events")
        st.markdown("""
        - **August 19, 2026:** Inauguration of New English Activity Room
        - **September 22, 2026:** Second Term Evaluation Examinations Commence
        - **October 15, 2026:** Annual Educational Field Excursion
        - **November 10, 2026:** Inter-House Athletic Meet
        """)

    with e2:
        st.subheader("🔔 General Notices")
        st.warning("⚠️ **Notice:** All teachers must submit term marksheets in standard CSV format to the evaluation portal by Friday.")
        st.info("ℹ️ **Parent-Teacher Meetings:** Scheduled at the end of each term valuation. Individual performance reports will be issued digitally.")

# ---------------------------------------------------------
# 7. SCHOOL HISTORY TAB
# ---------------------------------------------------------
elif navigation == "📖 School History":
    st.title("📖 History of R/ Theppanawa Kumara Maha Vidyalaya")
    st.caption("Rooted in educational excellence and community service in Sabaragamuwa Province.")

    st.markdown("""
    **R/ Theppanawa Kumara Maha Vidyalaya** stands as a pivotal educational institution in Kuruwita, Sabaragamuwa Province. 
    Over decades, the school has nurtured generations of students, instilling high academic values, civic responsibility, and cultural heritage.

    #### Key Milestones:
    
---

### **HISTORY**

Due to the religious educational revival that took place in the late 19th century, the **"Theppanawa Government Vernacular Boys' School"** was established in 1894. It was donated to the government with the support of the village council by Mr. Uyankumarage Harmanis Appuhamy, who was the village headman at the time. Started as a boys' school with the participation of 68 male students, its first principal was Mr. M. Thinnarachchi. As a result of gradual development, a girls' school was also started on the same school grounds in 1920, and the boys' and girls' schools were maintained separately. The first principal of the girls' school was Mrs. M. Herath.

The two separate schools for boys and girls were merged on January 1, 1953, and established as a mixed school under the name **"Government Dual-Type School."** Historical source evidence shows that on March 1, 1961, this school was named a Maha Vidyalaya and designated as **"R/Kumara Maha Vidyalaya."** Located in a region centered around a rural economic background, the school—as a rural institution with a large student population in the Kuruwita Education Division of the Ratnapura Education Zone—is currently making great progress. Since a group of teachers and children who inherited the legacy of past traditional dance generations are attached to the school, a special feature is that the school has been able to display exceptional abilities at the all-island level in the aesthetic field, both in the past and present. The school has also achieved various victories in sports, mathematics, and social science sectors. Furthermore, a large number of scholars who completed their primary education at this school are currently employed in various fields across the country, which is a exceptional achievement of the school.

Located in a very picturesque environment in the Kurugam Valley, the main challenge this school faces is being subject to annual flood disasters. Most recently, following the flood disaster on May 26, 2017, the school premises remained submerged under about 6 feet of water continuously for about a week. Consequently, resources in the computer lab, library, dance unit, science laboratory, and many classrooms in the primary section were heavily damaged. To bring a permanent solution to this situation, the current principal, Mr. H.D.M. Sanath M. Wickramaratne, with the help of the School Management Committee, the School Development Executive Committee, education officers, and political authorities, prepared foundational plans to develop the school under a 10-year long-term plan.

Accordingly, as the first phase, steps were taken to begin constructing a building for the primary section on the Pathanwatta school land, which includes the school sports ground (located in a area not affected by flood disasters). The $70 \times 25$ two-story building, which had been abandoned and in disrepair for nearly 20 years, was renovated in a very short time with financial allocations from the Sabaragamuwa Provincial Ministry of Education, allowing over 200 children in Grades 3 and 4 to be relocated there. Under the "Nearest School is the Best School" concept, in addition to the principal's official quarters and teacher quarters built in 2018, a new toilet system was constructed for the children. A $90 \times 25$ three-story building is proposed to be constructed in front of this site for Grades 1, 2, and 5 children, with plans to fully establish the primary section on this new grounds by 2027.

On the main Maha Vidyalaya grounds, plans have been made to construct a three-story building featuring English activity rooms, computers, a library, administrative units, and a lecture hall for the students, as well as another $90 \times 25$ three-story building for Grades 6–13 students. Every construction is planned to be designed above flood water levels, with the goal of creating the most attractive school equipped with technological facilities to guide thousands of children from feeder schools in the region. This is the sole wish of the school, which has over a thousand students, an academic and non-academic staff of nearly 60, and a large body of parents and alumni..
    """)