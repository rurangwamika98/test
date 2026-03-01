from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def broadcast(request):
    message = request.data.get("message", "")
    return Response({"status": "queued", "audience": "drivers", "message": message})
