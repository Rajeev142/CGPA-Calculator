import streamlit as st
from datetime import date
import tempfile
from reportlab.pdfgen import canvas

# --------------------------
# Page Configuration
# --------------------------
st.set_page_config(page_title="🎓 CGPA & SGPA Calculator", layout="centered")

# --------------------------
# Custom CSS for Light Theme & Visibility Fix
# --------------------------
st.markdown("""
    <style>
    /* Input Fields */
    .stTextInput input, .stDateInput input, .stNumberInput input,
    .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        color: black !important;
        background-color: white !important;
        border: 1px solid #ccc !important;
        border-radius: 5px !important;
    }

    input, textarea, select {
        color: black !important;
        background-color: white !important;
    }

    .stButton button {
        background-color: #1E88E5 !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* Centered Title Styling */
    .title-box {
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .title-text {
        font-size: 32px;
        font-weight: bold;
        color: #2c3e50;
        text-shadow: 2px 2px 5px #aaa;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# Centered Title Block
# --------------------------
st.markdown("""
    <div class="title-box">
        <h1 class="title-text">🎓 CGPA & SGPA Calculator</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center;'>Designed with ❤️ using Streamlit</p>", unsafe_allow_html=True)

# --------------------------
# Tab Layout
# --------------------------
tab1, tab2 = st.tabs(["📘 SGPA Calculator", "📗 CGPA Calculator"])

# --------------------------
# SGPA Calculator Tab
# --------------------------
with tab1:
    st.header("📘 SGPA Calculator")
    st.subheader("Student Information")
    student_name = st.text_input("👨‍🎓 Student Name")
    branch = st.text_input("🏫 Branch")
    semester = st.text_input("📚 Semester")
    publish_date = st.date_input("📅 Result Publish Date", value=date.today())

    st.subheader("📄 Subject Details")
    num_subjects = st.number_input("Enter number of subjects", min_value=1, max_value=20, step=1)

    grades_map = {
        "O (10)": 10,
        "E (9)": 9,
        "A (8)": 8,
        "B (7)": 7,
        "C (6)": 6,
        "D (5)": 5,
        "F (0)": 0
    }

    subjects = []
    total_credits = 0
    total_points = 0

    for i in range(num_subjects):
        st.markdown(f"### Subject {i+1}")
        code = st.text_input(f"📌 Subject Code", key=f"code_{i}")
        name = st.text_input(f"📚 Subject Name", key=f"name_{i}")
        credit = st.number_input(f"🔢 Credit", min_value=0, max_value=10, step=1, key=f"credit_{i}")
        grade = st.selectbox("🎯 Grade", list(grades_map.keys()), key=f"grade_{i}")
        tp = st.selectbox("📘 T/P", ["T", "P"], key=f"tp_{i}")

        grade_point = grades_map[grade]
        total_credits += credit
        total_points += grade_point * credit
        subjects.append((code, name, tp, credit, grade))

    if st.button("🎓 Calculate SGPA"):
        if total_credits == 0:
            st.error("Please enter at least one subject with credit > 0.")
        else:
            sgpa = total_points / total_credits
            st.success(f"✅ Your SGPA is: **{sgpa:.2f}**")

            st.subheader("Marksheet Summary")
            st.markdown(f"**Student Name:** {student_name}")
            st.markdown(f"**Branch:** {branch}")
            st.markdown(f"**Semester:** {semester}")
            st.markdown(f"**Date of Result Publication:** {publish_date.strftime('%d/%m/%Y')}")

            st.table({
                "S.No": list(range(1, num_subjects+1)),
                "Subject Code": [s[0] for s in subjects],
                "Subject Name": [s[1] for s in subjects],
                "T/P": [s[2] for s in subjects],
                "Credit": [s[3] for s in subjects],
                "Grade": [s[4] for s in subjects],
            })
            st.markdown(f"**Total Credits:** {total_credits} &nbsp;&nbsp;|&nbsp;&nbsp; **SGPA:** {sgpa:.2f}")

            # --------------- PDF Generation using reportlab ----------------
            def generate_pdf():
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    c = canvas.Canvas(tmp.name)
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(200, 800, "GIFT Autonomous, Bhubaneswar")
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(200, 780, "Student Result Summary")

                    y = 750
                    c.setFont("Helvetica", 11)
                    c.drawString(50, y, f"Student Name: {student_name}")
                    y -= 20
                    c.drawString(50, y, f"Branch: {branch}")
                    y -= 20
                    c.drawString(50, y, f"Semester: {semester}")
                    y -= 20
                    c.drawString(50, y, f"Date of Result Publication: {publish_date.strftime('%d/%m/%Y')}")
                    y -= 30

                    c.setFont("Helvetica-Bold", 11)
                    c.drawString(50, y, "S.No")
                    c.drawString(90, y, "Sub Code")
                    c.drawString(160, y, "Name")
                    c.drawString(300, y, "T/P")
                    c.drawString(340, y, "Credit")
                    c.drawString(400, y, "Grade")

                    c.setFont("Helvetica", 10)
                    for idx, s in enumerate(subjects, 1):
                        y -= 20
                        c.drawString(50, y, str(idx))
                        c.drawString(90, y, s[0])
                        c.drawString(160, y, s[1][:25])
                        c.drawString(300, y, s[2])
                        c.drawString(340, y, str(s[3]))
                        c.drawString(400, y, s[4])

                    y -= 40
                    c.setFont("Helvetica-Bold", 11)
                    c.drawString(50, y, f"Total Credits: {total_credits}")
                    c.drawString(250, y, f"SGPA: {sgpa:.2f}")
                    c.save()
                    return tmp.name

            pdf_path = generate_pdf()
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Marksheet",
                    data=f,
                    file_name="SGPA_Marksheet.pdf",
                    mime="application/pdf"
                )

# --------------------------
# CGPA Calculator Tab
# --------------------------
with tab2:
    st.header("📗 CGPA Calculator")
    num_sem = st.number_input("Enter number of semesters", min_value=1, max_value=12, step=1)

    total_cgpa_points = 0
    total_cgpa_credits = 0

    for i in range(1, num_sem + 1):
        sgpa = st.number_input(f"SGPA for Semester {i}", min_value=0.0, max_value=10.0, step=0.01, format="%.2f", key=f"sgpa_{i}")
        credit = st.number_input(f"Total Credits for Semester {i}", min_value=1, max_value=50, step=1, key=f"credit_{i}")
        total_cgpa_points += sgpa * credit
        total_cgpa_credits += credit

    if st.button("🎯 Calculate CGPA"):
        if total_cgpa_credits == 0:
            st.error("Total credits cannot be zero.")
        else:
            cgpa = total_cgpa_points / total_cgpa_credits
            st.success(f"✅ Your CGPA is: **{cgpa:.2f}**")
