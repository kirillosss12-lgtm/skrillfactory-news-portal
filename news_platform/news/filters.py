from django_filters import FilterSet, CharFilter, DateFilter
from django.forms import DateInput
from .models import Tovar

class ProductFilter(FilterSet):



    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название'
    )


    added_after = DateFilter(

        field_name='data',
        lookup_expr = 'date__gt',
        label='Позже даты',
        widget = DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model=Tovar
        fields=[]