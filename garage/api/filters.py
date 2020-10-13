import django_filters
from ..models import Event, CalendarEvent


class EventFilter(django_filters.FilterSet):
    from_date = django_filters.rest_framework.DateTimeFilter(field_name="date", lookup_expr='gte')
    to_date = django_filters.rest_framework.DateTimeFilter(field_name="date", lookup_expr='lte')
    class Meta:
        model = Event
        fields = ['type', 'from_date', 'to_date']


class CalendarEventFilter(django_filters.FilterSet):

    class Meta:
        model = CalendarEvent
        fields = ['date']
