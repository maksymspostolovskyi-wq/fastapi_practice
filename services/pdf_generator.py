from fpdf import FPDF


def generate_posts_report(filename: str, report_title: str, posts_data: list) -> str:
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, report_title, ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for post in posts_data:
        line = f"ID: {post.id} | Title: {post.title} | Published: {post.published}"
        pdf.cell(0, 10, line, ln=True)
        pdf.ln(2)

    filepath = f"./{filename}"
    pdf.output(filepath)

    return filepath
