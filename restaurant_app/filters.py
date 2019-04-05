import django_filters
from restaurant_app.models import Restaurant
from menu_app.models import Category,Menu


class RestaurantFilter(django_filters.FilterSet):



    #additional filtering fields
    res_user = django_filters.NumberFilter(field_name='res_user')
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains')
    approved_admin_id = django_filters.NumberFilter(field_name='approved_admin_id')
    category = django_filters.CharFilter(field_name='category__name',lookup_expr='icontains')
    dish = django_filters.CharFilter(field_name='menu__name',lookup_expr='icontains',distinct=True)
    latitude = django_filters.NumberFilter(field_name='latitude',method='filterByLatitude')
    longitude = django_filters.NumberFilter(field_name='longitude', method='filterByLongitude')

    class Meta:
        model = Restaurant
        exclude = 'photo'

    def filterByLatitude(self, queryset, name, *value):
        latitude = float(value[0])
        latitude_east = latitude - 0.4
        latitude_west = latitude + 0.4
        return queryset.filter(latitude__gte=latitude_east, latitude__lte=latitude_west)

    def filterByLongitude(self, queryset, name, *value):
        longitude = float(value[0])
        longitude_north = longitude - 0.4
        longitude_south = longitude + 0.4
        return queryset.filter(longitude__gte=longitude_north, longitude__lte=longitude_south)

