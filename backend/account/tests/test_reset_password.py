from unittest import TestCase, mock

from account.views.password_reset import PasswordResetViewSet
from account.serializers.reset_password import (
    ResetPasswordSerializer, ValidateResetRequest)


class TestAdminCustomerViewSet(TestCase):

    def setUp(self):
        self.validate_ser = ValidateResetRequest()
        self.request = mock.Mock()

    @mock.patch('account.serializers.reset_password.ValidateResetRequest')
    def test_validate_reset_verify(self, mock_get_object):
        pass
