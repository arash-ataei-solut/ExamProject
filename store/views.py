from collections import OrderedDict
from django.db.models import Avg, F
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from user.views import get_user_by_token
from .models import Store
from .serializers import StoreSerializer, StoreDetailSerializer
from .tasks import buy
from product.models import Product
from product.views import ProductView
from product.serializers import ProductSerializer
from product.renderers import MyRenderer


class StoreView(GenericViewSet, ListModelMixin):
    renderer_classes = [MyRenderer, JSONRenderer]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    queryset = Store.objects.all()

    serializers = {
        'list': StoreSerializer,
        'retrieve': ProductSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def retrieve(self, request, **kwargs):
        store = Store.objects.get(pk=kwargs['pk'])
        store_info = StoreDetailSerializer(store, context={'request': request})

        qs = Product.objects.filter(
            store=store
        ).annotate(
            average_rate=Avg('rates__rate')
        ).order_by(
            F('average_rate').desc(nulls_first=True), '-create_date'
        )

        queryset = SearchFilter().filter_queryset(
            request,
            qs,
            ProductView()
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(OrderedDict([
                ('count', self.paginator.page.paginator.count),
                ('next', self.paginator.get_next_link()),
                ('previous', self.paginator.get_previous_link()),
                ('category_info', store_info.data),
                ('results', serializer.data),
            ]))

        serializer = self.get_serializer(queryset, many=True)
        return Response(OrderedDict([
            ('category_info', store_info.data),
            ('posts', serializer.data),
        ]))

    @action(methods=['get'], detail=True)
    def buy(self, request, **kwargs):
        if 'Authorization' in request.COOKIES:
            buy.delay(get_user_by_token(request), kwargs['pk'])
            return HttpResponseRedirect(reverse('store-detail', kwargs={'pk': kwargs['pk']}))
        else:
            return HttpResponseRedirect(reverse('login'))
