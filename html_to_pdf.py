# Django-rest-framework-html-to-pdf

from rest_framework.views import APIView
from weasyprint import HTML
from django.http import HttpResponse
from datetime import datetime
from rest_framework.parsers import BaseParser
import os


class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()


class PDF(APIView):
    parser_classes = [PlainTextParser]

    def post(self, request, *args, **kwargs):
        try:
            temp_file_name = 'job'+str(datetime.now)+'.html'
            f = open(temp_file_name, "w+")
            f.write(str(request.data.decode("utf-8") ))
            f.close()
            pdf_file = HTML(temp_file_name).write_pdf()
            os.remove(temp_file_name)
            response = HttpResponse(pdf_file, content_type='application / pdf') 
            # filename = "JobCard_%s.pdf" % str(datetime.now())
            # content = "attachment; filename='%s'" % (filename)
            # response['Content-Disposition'] = content
            # if request.data["Print"] is True:
            #     filename = "JobCard_%s.pdf" % str(datetime.now())
            #     content = "attachment; filename='%s'" % (filename)
            #     response['Content-Disposition'] = content

            return response
        except Exception as e:
            return HttpResponse("Error Occurred"+e)
