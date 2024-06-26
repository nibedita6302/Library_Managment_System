import os
from datetime import datetime, date
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from .analytics import *
from .generateGraphs import create_bar_graph, create_pie_chart

def create_pdf(user_id):
    month = datetime.now().strftime('%B')
    year = datetime.now().strftime('%Y')
    file_path = f"./static/pdfs/{month}_{year}.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)     ## Create a PDF document

    ## Create a list to hold the content of the PDF
    elements = []

    ## Add header
    header_style = getSampleStyleSheet()["Heading1"]
    header_text = Paragraph(f"<b>MONTHLY ACTIVITY REPORT - {month}</b>", header_style)
    elements.append(header_text)

    ## ----------Add Section Distribution Pie Chart------------
    text = "Genre Distribution Chart\n\n"
    text_paragraph = Paragraph(text, getSampleStyleSheet()["Heading2"])
    elements.append(text_paragraph)
    objects1 = section_distribution_user(user_id)
    data1 = {}
    for obj in objects1:                         ## Convert to dictionary
        data1[obj.section_name] = obj.count
    image_path = create_pie_chart(data=data1, title='Reader Preference Pie',    ## Add the pie chart
                                  filename=f'pie_{month}_{year}')    
    img = Image(image_path, width=3*inch, height=3*inch)   
    elements.append(img)

    ## ----------------Favourite Author Graph-------------------
    text = "My Favourite Authors\n\n"
    text_paragraph = Paragraph(text, getSampleStyleSheet()["Heading2"])
    elements.append(text_paragraph)
    objects3 = fav_author(user_id)
    ## Make bar graph
    data1 = {}
    for obj in objects3:                         ## Convert to dictionary
        data1[obj.author_name] = obj.count
    image_path = create_bar_graph(data=data1, title='Author Read-o-Meter',    ## Add the pie chart
                                  filename=f'bar_{month}_{year}')   
    img = Image(image_path, width=6*inch, height=4*inch)   
    elements.append(img)

    ## ----------------Library Rankers Table--------------------
    text = "Top 5 Library Rankers, Are you one of them?\n\n"
    text_paragraph = Paragraph(text, getSampleStyleSheet()["Heading2"])
    elements.append(text_paragraph)
    data2 = [
        ['Rank', 'Username', 'Book Issues']         ## Add a table
    ]
    objects2 = user_ranking()
    for i in range(min(len(objects2),5)):   ## Display atmost top 5 Rankings
        data2.append([i+1, objects2[i].name, objects2[i].issue_count])

    table = Table(data2, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0, colors.black)
    ])
    elements.append(table)

    ## Build the PDF document - Saves the PDF in path
    doc.build(elements)
    print(f"PDF created successfully: {file_path}")
    return file_path