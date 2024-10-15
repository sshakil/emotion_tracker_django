from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Entry

# DELETE /entries/<uuid> or /entries/<uuid>.json
@csrf_exempt
def entry_delete(request, uuid):
    # Find the entry by UUID
    # todo: convert to uuid field here, and to actual uuid type in db
    entry = get_object_or_404(Entry, uuid=uuid)

    if entry:
        entry.delete()
        # Respond with HTTP 204 No Content on success
        return HttpResponse(status=204)
    else:
        # If entry is not found, respond with HTTP 404
        return JsonResponse({'error': 'Entry not found'}, status=404)

# Helper function (equivalent to set_entry in Rails)
def set_entry(uuid):
    return get_object_or_404(Entry, uuid=uuid)