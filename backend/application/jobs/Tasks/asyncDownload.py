import requests
import tempfile
from flask import jsonify, request, send_file
from celery import Celery
import secrets

def download_pdf(url, filename):
    response = requests.get(url)
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')     ## Create temporary pdf file
    temp_pdf.write(response.content)        ## Write content
    temp_pdf.close()
    ## Send file as attachement to be downloaded
    return send_file(temp_pdf, as_attachment=True, attachement_filename=filename)


