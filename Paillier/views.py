import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from base64 import b64encode
from .encryption_state_space import EncryptedStateSpace as ess

controller_enc = []


def reset_controller(request):
    if request.method == 'GET':
        for controller in controller_enc:
            controller.reset()
        return JsonResponse({'success': True}, status=200)
    else:
        return JsonResponse({'success': False, 'message': 'Method Not Allowed'}, status=405)


def input_controller(request):
    if request.method == 'GET':
        data = request.GET.dict()
        if 'inputs' in data:
            inputs = [int(inp) for inp in data['inputs'].split(',')]
            outputs = []
            for inp, controller in zip(inputs, controller_enc):
                outputs.append(controller.out(inp))

            return JsonResponse({'success': True, 'outputs': outputs}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Missing Required Parameters'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Method Not Allowed'}, status=405)


@csrf_exempt
def create_controller(request, *args, **kwargs):
    global controller_enc
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            A = data['A']
            B = data['B']
            C = data['C']
            D = data['D']
            init = data['init']
            n = data['n']

            if None in [A, B, C, D, init, n]:
                res = {
                    'success': False,
                    'message': 'Missing Required Parameters',
                }
                return JsonResponse(res, status=400)

            controller_enc = []
            for i in range(0, n):
                controller_enc.append(ess(A, B, C, D, init))

            return JsonResponse({'success': True, 'message': 'Controller Created'}, status=200)

        except ValueError:
            res = {
                'success': False,
                'message': 'Somthing Went Wrong',
            }
            return JsonResponse(res, status=400)

    else:
        return JsonResponse({'success': False, 'message': 'Method Not Allowed'}, status=405)


def set_public_key(request):
    if not request.method == 'GET':
        return JsonResponse({'success': False, 'message': 'Method Not Allowed'}, status=405)

    data = request.GET.dict()
    if 'public_key' in data:
        public_key = data['public_key'].split(',')
        pem_public_key = public_key_to_pem(public_key)
        with open('pub.crt', 'w') as f:
            f.write(pem_public_key)
        res = {
            'success': True,
            'public-key': pem_public_key
        }
        return JsonResponse(res)
    else:
        res = {
            'success': False,
            'message': 'Missing Required Parameters',
        }
        return JsonResponse(res, status=400)


def public_key_to_pem(public_key):
    public_key_data = f"{public_key[0]},{public_key[1]}".encode('utf-8')
    b64_encoded_key = b64encode(public_key_data).decode('utf-8')
    line_length = 64
    b64_encoded_key_lines = [b64_encoded_key[i:i + line_length] for i in range(0, len(b64_encoded_key), line_length)]
    formatted_key = '\n'.join(b64_encoded_key_lines)
    pem_key = f"-----BEGIN PAILLIER PUBLIC KEY-----\n{formatted_key}\n-----END PAILLIER PUBLIC KEY-----"

    return pem_key
