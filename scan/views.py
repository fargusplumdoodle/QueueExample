from QueueExample.settings import q
from .Queue import Job
from .AbstractTool import DummyTool
from django.http import JsonResponse

"""
CSRF Exempt is a security concern.

It is necessary in development because the SST API will not be originally developed
with authentication. 
"""
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # MUST BE REMOVED WHEN AUTHENTICATION IS IMPLEMENTED!!!
def scan(request):
    """
        Procedure:
        1. validate input
            - User validation
            - alias validation
            - url validation
            - check if duplicate scan ( involves checking queue )
        2. add to queue
        3. return scan_id

    """
    # Ensuring we are using post
    if request.method != "POST": return JsonResponse({"error": "Method not allowed, use POST"}, status=404)

    # TODO: things with user input
    tool = DummyTool(run_command="sleep 5")
    alias = "dummy_tool"
    user = 'nobody'
    host = 'nobody'

    # creating a job and adding it to the queue
    scan_id = q.add(Job(tool, user, alias, host))

    return JsonResponse({"scan_id": scan_id}, status=200)
