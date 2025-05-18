from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf_report(data: dict, filename: str = "resume_report.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Smart Resume Analysis Report")
    y -= 30

    c.setFont("Helvetica", 12)

    for key, value in data.items():
        if isinstance(value, list):
            c.drawString(50, y, f"{key.capitalize()}:")
            y -= 20
            for item in value:
                c.drawString(70, y, f"- {item}")
                y -= 15
        else:
            c.drawString(50, y, f"{key.capitalize()}: {value}")
            y -= 25

        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
    return filename
