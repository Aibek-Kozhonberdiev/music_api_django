from django.http import JsonResponse


def custom_404(request, exception):
    response_data = {'error': 'Not Found'}
    return JsonResponse(response_data, status=404)

def custom_500(request):
    response_data = {'error': "Server Error (500)"}
    return JsonResponse(response_data, status=500)
