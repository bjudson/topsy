from django.http import JsonResponse

def json_success(response, status=200):
    return JsonResponse({'success': True, 'response': response}, status=status)

def json_error(message, status=400):
    return JsonResponse({'success': False, 'message': message}, status=status)
