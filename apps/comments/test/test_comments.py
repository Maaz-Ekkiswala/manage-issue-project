import json

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.comments.models import Comments
from apps.issues.constants import Type, Status, Priority
from rest_framework.test import APIClient
from apps.issues.models import Issues, IssueUser
from apps.users.models import UserProfile
from manager_project.manager_test_client import ManagerTestClient

Test_username = 'james@nomail.com'
Test_password = 'password'
Test_first_name = 'charlie'
Test_last_name = 'george'
Test_mobile = '6363636363'


class CommentsTestCases(ManagerTestClient):

    @classmethod
    def setUpTestData(cls):
        super(CommentsTestCases, cls).setUpTestData()
        UserProfile.objects.create(
            username=Test_username,
            password=Test_password,
            first_name=Test_first_name,
            last_name=Test_last_name,
            mobile=Test_mobile,
            is_active=True,
        )

    def setUp(self) -> None:
        super(CommentsTestCases, self).setUp()
        self.user_for_comment = UserProfile.objects.filter(username=Test_username).first()
        self.issue = Issues.objects.create(
            project_id=1,
            title="This is test_issue",
            type=Type.BUG,
            status=Status.IN_PROGRESS,
            priority=Priority.HIGH,
            description="This issue is created for test and testing",
            reported_id=self.user,
            created_by_id=self.user.id
        )
        IssueUser.objects.create(issue=self.issue, assign_to_id=self.user_for_comment.id)
        IssueUser.objects.create(issue=self.issue, assign_to_id=self.user.id)
        self.comment = Comments.objects.create(
            issue=self.issue,
            commented_by_id=self.user_for_comment.id,
            description="this is the testing comment"
        )
        user_token_for_comment = RefreshToken.for_user(self.user_for_comment)
        user_access_token_for_comment = str(user_token_for_comment.access_token)
        self.authorized_client_for_comment = APIClient(
            self.user_for_comment, HTTP_AUTHORIZATION="Bearer " + user_access_token_for_comment
        )

    def test_create_comment(self):
        data = {"description": "This is the first comment"}
        response = self.authorized_client_for_comment.post(
            path=f"/api/v1/comments/?issue_id={str(self.issue.id)}",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("description"), "This is the first comment")

    def test_create_comment_with_invalid_url(self):
        data = {"description": "This is the first comment"}
        response = self.authorized_client_for_comment.post(
            path=f"api/v1/comments/?issue_id={str(self.issue.id)}",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment_with_unauthorized_user(self):
        data = {"description": "This is the first comment"}
        response = self.unauthorized_client.post(
            path=f"/api/v1/comments/?issue_id={str(self.issue.id)}",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {"detail": "Authentication credentials were not provided."}
        )

    def test_create_comment_with_invalid_issue_id(self):
        data = {"description": "This is the first comment"}
        response = self.authorized_client_for_comment.post(
            path=f"/api/v1/comments/?issue_id={10}",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"message": "Issue not found"}
        )

    def test_update_comment(self):
        data = {"description": "This is the updated comment"}

        response = self.authorized_client_for_comment.put(
            path=f"/api/v1/comments/{str(self.comment.id)}/?issue_id={str(self.issue.id)}",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("description"), "This is the updated comment")

    def test_update_comment_with_another_client(self):
        data = {"description": "This is the updated comment"}

        response = self.authorized_client.put(
            path=f"/api/v1/comments/{str(self.comment.id)}/?issue_id={str(self.issue.id)}",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {"message": "You cannot update other's comment"})

    def test_delete_comment_with_another_client(self):
        response = self.authorized_client.delete(
            path=f"/api/v1/comments/{str(self.comment.id)}/?issue_id={str(self.issue.id)}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {"message": "You cannot delete other's comment"})

    def test_delete_comment(self):
        response = self.authorized_client_for_comment.delete(
            path=f"/api/v1/comments/{str(self.comment.id)}/?issue_id={str(self.issue.id)}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Comment deleted successfully"})

    def test_delete_comment_with_unauthorized_client(self):
        response = self.unauthorized_client.delete(
            path=f"/api/v1/comments/{str(self.comment.id)}/?issue_id={str(self.issue.id)}",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {"detail": "Authentication credentials were not provided."}
        )

    def test_get_list_of_comments(self):
        response = self.authorized_client_for_comment.get(
            path=f"/api/v1/comments/?issue_id={str(self.issue.id)}"
        )
        response_data = response.json()
        response_count = len(response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comments.objects.count(), response_count)

    def test_get_list_of_comments_with_unauthorized_client(self):
        response = self.unauthorized_client.get(
            path=f"/api/v1/comments/?issue_id={str(self.issue.id)}"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {"detail": "Authentication credentials were not provided."}
        )
