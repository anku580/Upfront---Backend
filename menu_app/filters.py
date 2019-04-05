import django_filters
from menu_app.models import Category,Menu



class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = '__all__'


class MenuFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains')
    class Meta:
        model = Menu
        exclude = ['photo']



