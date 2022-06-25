from unittest import TestCase, mock
from account.views.profile import AdminCustomerViewSet

from account.models.user import CustomUser


class TestAdminCustomerViewSet(TestCase):

    def setUp(self):
        self.profile_view = AdminCustomerViewSet()
        self.request = mock.Mock()

    @mock.patch('account.views.profile.AdminCustomerViewSet.get_object')
    def test_profile_activate(self, mock_get_object):
        """
        Test that ban and actiavte works
        """
        mock_get_object.owner = mock.Mock(spec=CustomUser)
        response = self.profile_view.activate(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(mock_get_object.owner.is_active)
        self.assertIsNotNone(mock_get_object.activated)

    @mock.patch('account.views.profile.AdminCustomerViewSet.get_object')
    def test_profile_ban(self, mock_get_object):
        """
        Test that ban and actiavte works
        """
        mock_get_object.owner = mock.Mock(spec=CustomUser)
        response = self.profile_view.ban(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(False, mock_get_object.owner.is_active)
        self.assertEqual(False, mock_get_object.activated)
        self.assertEqual(False, mock_get_object.banned)
