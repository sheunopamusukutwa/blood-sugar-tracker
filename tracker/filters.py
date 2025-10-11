# readings/filters.py
import django_filters as df
from .models import Reading

class ReadingFilter(df.FilterSet):
    # Accept YYYY-MM-DD and compare to timestamp's date part
    date_from = df.DateFilter(field_name="timestamp", lookup_expr="date__gte")
    date_to   = df.DateFilter(field_name="timestamp", lookup_expr="date__lte")

def _split_csv(value): return [v.strip() for v in value.split(",") if v.strip()]
statuses = df.CharFilter(method="filter_statuses")
def filter_statuses(self, qs, name, value):
    return qs.filter(status__in=_split_csv(value))

    class Meta:
        model = Reading
        fields = ["date_from", "date_to", "status"]
