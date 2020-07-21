import django_filters
from ..models import CTO, Service
from django_filters import Filter, FilterSet
from django_filters.fields import Lookup
from django.db.models import Q


class NumberInFilter(django_filters.rest_framework.BaseInFilter, django_filters.rest_framework.NumberFilter):
    pass


class ListFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = 'in'
        values = value.split(',')
        return super(ListFilter, self).filter(qs, values)



class CtoFilter(django_filters.FilterSet):
    services_id = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='services__id',
        to_field_name='id',
        queryset=Service.objects.all(),
        conjoined=True
    )
    # services_in = NumberInFilter(field_name='services', lookup_expr='in')

    # services_id = ListFilter('services__id')
    class Meta:
        model = CTO
        fields = ('services_id',)
