from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import read_data
import tenseal as ts
import base64


@csrf_exempt
def set_public_key(request):
    if request.method == 'POST' and request.FILES.get('file', None):
        uploaded_file = request.FILES['file']
        with open('public_key.txt', 'wb') as f:
            f.write(uploaded_file.read())
        return JsonResponse({'message': 'Public Key Set successfully'})
    else:
        return JsonResponse({'error': 'Public Key failed to set'}, status=400)


@csrf_exempt
def input_controller(request):
    if request.method == 'POST' and request.FILES.get('states', None):
        context = ts.context_from(read_data('public_key.txt'))
        states_proto = base64.b64decode(request.FILES['states'].read())
        error_proto = base64.b64decode(request.FILES['error'].read())
        encrypted_states = ts.lazy_ckks_vector_from(states_proto)
        encrypted_states.link_context(context)
        encrypted_error = ts.lazy_ckks_vector_from(error_proto)
        encrypted_error.link_context(context)

        ACT = [[1, 0], [0.0063, 0.3678]]
        BCT = [[0, 0.0063]]
        CCT = [[10], [-99.90]]
        DCT = [[3]]

        encrypted_states_next = encrypted_states.matmul(ACT) + encrypted_error.matmul(BCT)
        encrypted_control_signal = encrypted_states.matmul(CCT) + encrypted_error.matmul(DCT)

        return JsonResponse({
            'states': base64.b64encode(encrypted_states_next.serialize()).decode('ascii'),
            'control_signal': base64.b64encode(encrypted_control_signal.serialize()).decode('ascii'),
        })
    else:
        return JsonResponse({'error': 'The method does not exist'}, status=400)
