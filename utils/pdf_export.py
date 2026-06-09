from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(messages):

    file_path = "reports/chat_report.pdf"

    pdf = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "CyberShield AI Chat Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    for msg in messages:

        content.append(
            Paragraph(
                f"<b>{msg['role'].upper()}</b>: {msg['content']}",
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 8)
        )

    pdf.build(content)

    return file_path