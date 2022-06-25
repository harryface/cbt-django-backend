import unittest
from unittest.mock import patch, Mock

from core.models.answer import Answer
from core.models.question import Question
from core.permissions import ExamPermission, AnswerPermission
from core.views.answer import AnswerCreateView
from core.views.exam import ExamViewSet


class TestExamPermission(unittest.TestCase):
    """
    Unit test suite for Exam Permission class
    """

    def setUp(self):
        self.request = Mock()
        self.view = Mock(spec=ExamViewSet)
        return super().setUp()

    def test_fail_if_not_authenticated(self):
        """
        Check that it fails if not authenticated
        """

        permissions = ExamPermission()
        self.request.user.is_authenticated = True
        has_access = permissions.has_permission(self.request, self.view)

        self.assertFalse(has_access)

    def test_allows_list_for_students(self):
        """
        Check that it allows student for listing exams
        """

        permissions = ExamPermission()
        self.request.user.role == "student"
        self.view.action = "list"
        has_access = permissions.has_permission(self.request, self.view)

        self.view.queryset.filter.assert_called()
        self.assertTrue(has_access)
    
    def test_allows_retrieve_for_students(self):
        """
        Check that it allows student for listing exams
        """

        permissions = ExamPermission()
        self.request.user.role == "student"
        self.view.action = "retrieve"
        has_access = permissions.has_permission(self.request, self.view)

        self.view.queryset.filter.assert_called()
        self.assertTrue(has_access)

    def test_allows_result_for_students(self):
        """
        Check that it allows student for listing exams
        """

        permissions = ExamPermission()
        self.request.user.role == "student"
        self.view.action = "result"
        has_access = permissions.has_permission(self.request, self.view)

        self.assertTrue(has_access)

    def test_blocks_other_actions_for_students(self):
        """
        Check that it blocks student for other actions
        """

        permissions = ExamPermission()
        self.request.user.role == "student"
        self.view.action = "create"
        has_access = permissions.has_permission(self.request, self.view)

        self.assertFalse(has_access)

    def test_allows_for_examiner(self):
        """
        Check that if examiner, pass
        """

        permissions = ExamPermission()
        self.request.user.role == "examiner"
        has_access = permissions.has_permission(self.request, self.view)

        self.assertTrue(has_access)


class TestAnswerPermission(unittest.TestCase):
    """
    Unit test suite for Answer Permission class
    """

    def setUp(self):
        self.request = Mock()
        self.view = Mock(spec=AnswerCreateView)
        self.obj = Mock(spec=Answer)
        return super().setUp()

    def test_fail_if_not_authenticated(self):
        """
        Check that it fails if not authenticated
        """

        permissions = ExamPermission()
        self.request.user.is_authenticated = True
        has_access = permissions.has_permission(self.request, self.view)

        self.assertFalse(has_access)
        
    def test_allows_list_for_students(self):
        """
        Check that it allows student for listing exams
        """

        permissions = ExamPermission()
        self.request.data = [{"question": 1, "answer": "20" }, {"question": 2, "answer": "test" }]
        self.request.user.is_authenticated = True
        self.request.user.role == "student"
        self.view.action = "list"
        has_access = permissions.has_permission(self.request, self.view)

        self.view.queryset.filter.assert_called()
        self.assertTrue(has_access)