from rest_framework import mixins, viewsets

from account.serializers.user import UserSerializer
from account.models.user import CustomUser


class CustomUserViewSet(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
