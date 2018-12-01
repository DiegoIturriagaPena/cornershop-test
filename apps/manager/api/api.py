from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from apps.employees import models as employee_models
from rest_framework.views import Response


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def change_order_state(request):
    """Change the status of the order."""
    data = request.POST
    if not 'pk' in data.keys():
        return Response('Bad Request', status=HTTP_400_BAD_REQUEST)
    order = get_object_or_404(employee_models.Order, pk=data.get('pk'))
    try:
        order.state = 'Ready'
        order.save()
    except Exception as exc:
        error = 'Error: %s' % exc
        return Response(error, status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response("OK", status=HTTP_200_OK)
