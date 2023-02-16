import json

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from apps.issues.constants import Type, Status, Priority
from apps.issues.models import Issues
from apps.projects.models import ProjectUser

from apps.users.models import UserProfile
from manager_project.manager_test_client import ManagerTestClient


Test_username = 'jhones@nomail.com'
Test_password = 'password'
Test_first_name = 'charlie'
Test_last_name = 'george'
Test_mobile = '6363636363'

Test2_username = 'charlie@nomail.com'
Test2_password = 'password'
Test2_first_name = 'charlie'
Test2_last_name = 'george'
Test2_mobile = '7070707070'
# Create your tests here.


class IssuesTestCases(ManagerTestClient):

    @classmethod
    def setUpTestData(cls):
        super(IssuesTestCases, cls).setUpTestData()
        UserProfile.objects.create(
            username=Test_username,
            password=Test_password,
            first_name=Test_first_name,
            last_name=Test_last_name,
            mobile=Test_mobile,
            is_active=True,
        )

        UserProfile.objects.create(
            username=Test2_username,
            password=Test2_password,
            first_name=Test2_first_name,
            last_name=Test2_last_name,
            mobile=Test2_mobile,
            is_active=True,
        )

    def setUp(self) -> None:
        super(IssuesTestCases, self).setUp()
        self.user_for_issue = UserProfile.objects.filter(username=Test_username).first()
        self.user_for_issue_second = UserProfile.objects.filter(username=Test2_username).first()
        ProjectUser.objects.create(project_id=1, assign_to=self.user_for_issue)
        ProjectUser.objects.create(project_id=1, assign_to=self.user_for_issue_second)
        ProjectUser.objects.create(project_id=1, assign_to=self.admin_user)
        self.issue = Issues.objects.create(
            project_id=1,
            title="This is test_issue",
            type=Type.BUG,
            status=Status.IN_PROGRESS,
            priority=Priority.HIGH,
            description="This issue is created for test and testing",
            reported_id=self.user,
            created_by_id=self.user_for_issue.id
        )
        user_token = RefreshToken.for_user(self.user_for_issue)
        user_token_second = RefreshToken.for_user(self.user_for_issue_second)
        user_access_key = str(user_token.access_token)
        user_access_key_second = str(user_token_second.access_token)
        self.authorized_client_for_issue = APIClient(
            self.user_for_issue, HTTP_AUTHORIZATION="Bearer " + user_access_key
        )
        self.authorized_client_for_issue_second = APIClient(
            self.user_for_issue_second, HTTP_AUTHORIZATION="Bearer " + user_access_key_second
        )

    def test_create_issue(self):
        data = {
            "title": "This is test_issue",
            "type": Type.TASK,
            "status": Status.PENDING,
            "priority": Priority.LOW,
            "description": "This issue is created for test and testing",
            "reported_id": self.user.id
        }
        response = self.authorized_client_for_issue.post(
            path=f"/api/v1/issues/?project_id=1",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_issue_with_client_not_in_project_user(self):
        data = {
            "title": "This is test_issue",
            "type": "task",
            "status": "pending",
            "priority": "low",
            "description": "This issue is created for test and testing",
            "reported_id": self.user.id
        }
        response = self.authorized_client.post(
            path=f"/api/v1/issues/?project_id=1",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."}
        )

    def test_create_issue_with_incorrect_data(self):
        data = {
            "type": Type.TASK,
            "status": Status.PENDING,
            "priority": Priority.LOW,
            "description": "This issue is created for test and testing",
            "reported_id": self.user.id
        }
        response = self.authorized_client_for_issue.post(
            path=f"/api/v1/issues/?project_id=1",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_issue_with_assign_users(self):
        data = {
            "title": "This is test_issue",
            "type": Type.TASK,
            "status": Status.PENDING,
            "priority": Priority.LOW,
            "description": "This issue is created for test and testing",
            "reported_id": self.user.id,
            "issue_users": [self.admin_user.id, self.user_for_issue.id]
        }
        response = self.authorized_client_for_issue.post(
            path=f"/api/v1/issues/?project_id=1",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_issue_with_assign_incorrect_users(self):
        data = {
            "title": "This is test_issue",
            "type": Type.TASK,
            "status": Status.PENDING,
            "priority": Priority.LOW,
            "description": "This issue is created for test and testing",
            "reported_id": self.user.id,
            "issue_users": [8, self.user_for_issue.id]
        }
        response = self.authorized_client_for_issue.post(
            path=f"/api/v1/issues/?project_id=1",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."}
        )

    def test_update_issue(self):
        data = {
            "title": "This is test_issue",
            "type": Type.TASK,
            "status": Status.PENDING,
            "priority": Priority.LOW,
            "description": "This issue is created for test and testing",
            "reported_id": self.user.id,
        }
        response = self.authorized_client_for_issue.put(
            path=f"/api/v1/issues/{self.issue.id}/?project_id=1",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_issue_with_unauthorized_client(self):
        data = {
            "title": "This is test_issue",
            "type": Type.TASK,
            "status": Status.PENDING,
            "priority": Priority.LOW,
            "description": "This issue is created for test and testing",
            "reported_id": self.user.id,
        }
        response = self.unauthorized_client.put(
            path=f"/api/v1/issues/{self.issue.id}/?project_id=1",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {"detail": "Authentication credentials were not provided."}
        )

    def test_get_issue_by_id(self):
        response = self.authorized_client_for_issue.get(
            path=f"/api/v1/issues/{self.issue.id}/?project_id=1",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), "This is test_issue")
        self.assertEqual(response.data.get("type"), "bug")
        self.assertEqual(response.data.get("priority"), "high")

    def test_get_issue_by_id_with_another_client(self):
        response = self.authorized_client.get(
            path=f"/api/v1/issues/{self.issue.id}/?project_id=1",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."}
        )

    def test_add_issue_users(self):
        data = {"issue_users": [self.user_for_issue.id]}
        response = self.authorized_client_for_issue.post(
            path=f"/api/v1/issues/{self.issue.id}/issue-users/?project_id=1",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_issue_users_with_invalid_users(self):
        data = {"issue_users": [self.user_for_issue.id, self.user.id]}
        response = self.authorized_client_for_issue.post(
            path=f"/api/v1/issues/{self.issue.id}/issue-users/?project_id=1",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."}
        )

    def test_delete_issue_with_other_user(self):
        response = self.authorized_client_for_issue_second.delete(
            path=f"/api/v1/issues/{self.issue.id}/?project_id=1",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {"message": "You cannot delete other's issue"})

    def test_delete_issue(self):
        response = self.authorized_client_for_issue.delete(
            path=f"/api/v1/issues/{self.issue.id}/?project_id=1",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Issue deleted successfully"})