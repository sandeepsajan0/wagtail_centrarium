from django.shortcuts import render

# Create your views here.
from wagtail.documents.views import serve


def view_document(request, document_id, document_filename):
    """
    Calls the normal document `serve` view, except makes it not an attachment.
    """
    # Get response from `serve` first
    response = serve.serve(request, document_id, document_filename)

    # Remove "attachment" from response's Content-Disposition
    contdisp = response['Content-Disposition']
    response['Content-Disposition'] = "; ".join(
        [x for x in contdisp.split("; ") if x != "attachment"]
    )

    # Return the response
    return response