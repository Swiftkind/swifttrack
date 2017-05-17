import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

class CreatePdf():
    '''
    Create PDF files
    Parameters:
    1. data: dictionary - dictionary to be passed to the template
    2. template: string - the html file to be converted to PDF
    3. file_path:string - the folder and the desired file name when saving the file; Files are saved in media folder
        (be sure to have MEDIA_URL and MEDIA ROOT in your settings)
    '''
    def generate_pdf(self, data, template, file_path, style):
        template = get_template(template)
        html = template.render(Context(data))
        file = open(os.path.join(settings.MEDIA_ROOT, file_path), "w+b")
        pisaStatus = pisa.CreatePDF(html, dest=file, default_css=style)
        file.seek(0)
        pdf = file.read()
        file.close()
        return HttpResponse(pdf, content_type='application/pdf')