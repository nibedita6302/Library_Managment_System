import os
from datetime import datetime, date
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from utils.analytics import *
from .generateGraphs import pieChart

def create_pdf(user_id):
    month = datetime.now().strftime('%B')
    year = datetime.now().strftime('%Y')
    file_path = f"./static/pdfs/{month}_{year}.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)     # Create a PDF document

    # Create a list to hold the content of the PDF
    elements = []

    # Add a header
    header_style = getSampleStyleSheet()["Heading1"]
    header_text = Paragraph(f"<b>MONTHLY ACTIVITY REPORT - {month}</b>", header_style)
    elements.append(header_text)

    # Add some text
    text = "Section Wise - Book Read Distribution\n\n"
    text_paragraph = Paragraph(text, getSampleStyleSheet()["Heading2"])
    elements.append(text_paragraph)
    objects1 = section_distribution_user(user_id)
    data1 = {}
    for obj in objects1:                         ## Convert to dictionary
        data1[obj.section_name] = obj.count

    image_path = pieChart(data1)
    img = Image(image_path, width=300, height=300)   # Add an image
    elements.append(img)

    text = "Store Manager and Admin Logs Table\n\n"
    text_paragraph = Paragraph(text, getSampleStyleSheet()["Heading2"])
    elements.append(text_paragraph)

    # Add a table
    data2 = [
        ['Username', 'Rank']
    ]
    objects2 = user_ranking()
    for i in range(len(objects2)):
        data2.append([objects2.name, i])

    table = Table(data2, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    elements.append(table)

    text = "My Favourite Authors\n\n"
    text_paragraph = Paragraph(text, getSampleStyleSheet()["Heading2"])
    elements.append(text_paragraph)
    objects3 = fav_author(user_id)
    for obj in objects3:
        text = f"Author - {obj.author_name}\t\tReads:{obj.count}\n\n"
        text_paragraph = Paragraph(text, getSampleStyleSheet()["BodyText"])
        elements.append(text_paragraph)

    # Build the PDF document - Saves the PDF in path
    doc.build(elements)
    print(f"PDF created successfully: {file_path}")
    return file_path