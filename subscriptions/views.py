from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Account, Author, Book
from .serializers import AccountSerializer, AuthorSerializer, BookSerializer


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    permission_classes = [AllowAny]

    @action(detail=True, methods=['patch'], name='Update Subscription')
    def update_subscription(self, request, pk):
        account = Account.objects.get(pk=pk)

        days = request.data.get('days')
        if not days:
            return Response({
                'account_id': account.id,
                'status': 'error',
                'msg': 'days not found'
            })

        account.update_subscription(days)
        return Response({
            'account_id': account.id,
            'status': 'ok',
            'period': account.subscription
        })


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def list(self, request, *args, **kwargs):
        account = Account.objects.filter(user=request.user.id).first()
        serializer_class = self.get_serializer_class()
        if account and account.is_active():
            serializer_class.Meta.fields = '__all__'
        else:
            serializer_class.Meta.fields = ['id', 'title']
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        account = Account.objects.filter(user=request.user.id).first()
        serializer_class = self.get_serializer_class()
        if account and account.is_active():
            serializer_class.Meta.fields = '__all__'
        else:
            serializer_class.Meta.fields = ['id', 'title']
        return super().retrieve(request, *args, **kwargs)
