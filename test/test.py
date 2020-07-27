import markdown
import os
from django.conf import settings
from xhtml2pdf import pisa

settings.configure(STATIC_URL = os.getcwd(), MEDIA_URL="")



with open('README.md', 'r', encoding='utf-8') as input_file:
        text = input_file.read()

html = markdown.markdown(text)

with open("output.html", 'w', encoding='utf-8', errors="xmlcharrefreplace") as output_file:
    output_file.write(html)

def link_callback(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically "" if not defined in settings.py
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(sUrl):
        # Replaces 'static/image.png' with 'c:\\my-project\\collected-static/image.png'
        path = os.path.join(sRoot, uri.replace(sUrl, ""))

        print(path)
    elif uri.startswith(mUrl):
        # MEDIA_URL default value is "" so everything matches this
        path = os.path.join(mRoot, uri.replace(mUrl, ""))

        print(path)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
    return path



def convert_html_to_pdf(source_html, output_filename):
    result_file = open(output_filename, "w+b")


    pisa_status = pisa.CreatePDF(
            source_html,
            dest=result_file,
            link_callback=link_callback)

    result_file.close()

    return pisa_status.err

pisa.showLogging()
convert_html_to_pdf(html, 'test.pdf')

print(str(settings.MEDIA_URL))

print(str(settings.STATIC_URL))