import json
from rest_framework import status

from apps.users.models import UserProfile
from manager_project.manager_test_client import ManagerTestClient


class UserViewTestCases(ManagerTestClient):

    def test_get_user_by_id(self):
        response = self.authorized_client.get(f"/api/v1/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("username"), "jack@nomail.com")
        self.assertEqual(response.data.get("first_name"), "jack")
        self.assertEqual(response.data.get("last_name"), "george")

    def test_get_user_with_unauthorized_client(self):
        response = self.unauthorized_client.get(f"/api/v1/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {"detail": "Authentication credentials were not provided."}
        )

    def test_get_user_with_incorrect_url(self):
        response = self.authorized_client.get(f"/api/v1//users/{self.user.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user(self):
        data = {
            "first_name": "Jhones",
            "last_name": "George",
        }
        response = self.authorized_client.put(
            path=f"/api/v1/users/{self.user.id}/",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("first_name"), "Jhones")
        self.assertEqual(response.data.get("last_name"), "George")

    def test_update_user_with_unauthorized_client(self):
        data = {
            "first_name": "Jhones",
            "last_name": "George",
        }
        response = self.unauthorized_client.put(
            f"/api/v1/users/{self.user.id}/", data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {"detail": "Authentication credentials were not provided."}
        )

    def test_update_user_with_different_id(self):
        data = {
            "first_name": "Jhones",
            "last_name": "George",
        }
        response = self.authorized_client.put(
            f"/api/v1/users/50/",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Not found."})

    def test_get_list_user_without_admin_user(self):
        response = self.authorized_client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."}
        )

    def test_get_list_user(self):
        response = self.admin_client.get("/api/v1/users/")
        response_data = response.json()
        response_count = len(response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.count(), response_count)
