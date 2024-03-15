import requests
import tempfile

def download_pdf(url):
    response = requests.get(url)
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')     ## Create temporary pdf file
    temp_pdf.write(response.content)        ## Write content
    temp_pdf.close()
    return temp_pdf.name


