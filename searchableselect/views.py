try:
    # Django <=1.9
    from django.db.models.loading import get_model
except ImportError:
    # Django 1.10+
    from django.apps import apps
    get_model = apps.get_model

from django.utils.encoding import smart_str
from django.http import JsonResponse


def filter_models(request):
    model_name = request.GET.get('model')
    search_field = request.GET.get('search_field')
    value = request.GET.get('q').strip()

    model = get_model(model_name)

    values = model.objects.filter(**{'{}__icontains'.format(search_field): value})[:10]
    values = [
        dict(pk=v.pk, name=smart_str(v))
        for v
        in values
    ]

    return JsonResponse(dict(result=values))
