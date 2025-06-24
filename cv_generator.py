import streamlit as st
from fpdf import FPDF

# PDF-klasse voor het CV
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "CV / Resume", border=0, ln=1, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, ln=1)
        self.set_text_color(0, 0, 0)

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_pdf(data):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, data["name"], ln=1)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, data["email"], ln=1)
    pdf.cell(0, 10, data["phone"], ln=1)
    pdf.ln(10)

    if data["summary"]:
        pdf.chapter_title("Profiel")
        pdf.chapter_body(data["summary"])

    if data["experience"]:
        pdf.chapter_title("Werkervaring")
        pdf.chapter_body(data["experience"])

    if data["education"]:
        pdf.chapter_title("Opleiding")
        pdf.chapter_body(data["education"])

    if data["skills"]:
        pdf.chapter_title("Vaardigheden")
        pdf.chapter_body(data["skills"])

    return pdf.output(dest="S").encode("latin-1")

# Streamlit app
st.title("📄 CV / Resume PDF Generator")

name = st.text_input("Naam", "Jan Jansen")
email = st.text_input("E-mail", "jan@example.com")
phone = st.text_input("Telefoonnummer", "+31 6 12345678")
summary = st.text_area("Profiel (kort over jezelf)")
experience = st.text_area("Werkervaring")
education = st.text_area("Opleiding")
skills = st.text_area("Vaardigheden (bijv. Python, Photoshop)")

if st.button("Genereer PDF"):
    if not name or not email:
        st.warning("Vul minimaal naam en e-mail in.")
    else:
        pdf_bytes = generate_pdf({
            "name": name,
            "email": email,
            "phone": phone,
            "summary": summary,
            "experience": experience,
            "education": education,
            "skills": skills
        })
        st.download_button(
            label="Download je CV als PDF",
            data=pdf_bytes,
            file_name=f"{name.replace(' ', '_')}_CV.pdf",
            mime="application/pdf"
        )
