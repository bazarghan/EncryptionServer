from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View


class Controller1(View):
    def get(self, request):
        data = request.GET.dict()
        if 'inputs' in data:
            inputs = data['inputs'].split(',')
            print(inputs)
            return JsonResponse(data)
        else:
            return HttpResponseBadRequest('Missing Input in the Request')


