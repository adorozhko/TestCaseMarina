from rest_framework.routers import DefaultRouter

from .views import AccountViewSet, AuthorViewSet, BookViewSet

router = DefaultRouter()
router.register('accounts', AccountViewSet)
router.register('authors', AuthorViewSet)
router.register('books', BookViewSet)
