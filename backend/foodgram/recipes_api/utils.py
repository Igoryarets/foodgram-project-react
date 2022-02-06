from io import StringIO
from wsgiref.util import FileWrapper

from django.db.models import Sum
from django.http import HttpResponse
from rest_framework.decorators import api_view

from .models import Ingredient


@api_view(['GET'])
def download_shopping_cart(request):
    user = request.user
    ingredients = Ingredient.objects.filter(
        recipe__shopping_cart__user=user
    ).values(
        'name', 'measurement_unit'
    ).annotate(amount=Sum('ingredient__amount'))

    ingredient_list = []

    for ingredient in ingredients:
        ingredient_list.append(
            f"{ingredient.get('name')} "
            f"({ingredient.get('measurement_unit')}) - "
            f"{ingredient.get('amount')}"
        )

    data = '\n'.join(ingredient_list)
    file_name = f'{user.username}_shopping_cart.txt'
    file = StringIO(data)
    response = HttpResponse(FileWrapper(file), content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    return response
