from rest_framework.routers import DefaultRouter

from account.views.password_reset import PasswordResetViewSet
from account.views.user import CustomUserViewSet

app_name = 'account'

router = DefaultRouter()
router.register(r'register', CustomUserViewSet, basename='register')
router.register(r'reset', PasswordResetViewSet, basename='reset')

urlpatterns = router.urls
