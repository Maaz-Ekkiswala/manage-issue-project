
import os
from django.core.files.uploadedfile import SimpleUploadedFile

from manager_project.manager_test_client import ManagerTestClient


class UserViewTestCases(ManagerTestClient):

    def test_get_user_by_id(self):
        response = self.authorized_client.get(f"/api/v1/users/{self.user.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("username"), "jack@nomail.com")
        self.assertEqual(response.data.get("first_name"), "jack")
        self.assertEqual(response.data.get("last_name"), "george")

    def test_get_user_with_unauthorized_client(self):
        response = self.unauthorized_client.get(f"/api/v1/users/{self.user.id}/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data,
            {"detail": "Authentication credentials were not provided."}
        )

    def test_get_user_with_incorrect_url(self):
        response = self.authorized_client.get(f"/api/v1//users/{self.user.id}")
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        image_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                '/home/elixirtechne/PycharmProject/manager_project/media/avatars/Snake_River_5mb.jpg'
        ))
        with open(image_path, 'rb') as f:
            image_content = f.read()

        image = SimpleUploadedFile('Snake_River_5mb.jpg', image_content, content_type='image/jpeg')
        data = {
            "first_name": "Jhones",
            "last_name": "George",
            "avatar": image
        }
        response = self.authorized_client.put(
            f"/api/v1/users/{self.user.id}/",
            data=data,
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("first_name"), "Jhones")
        self.assertEqual(response.data.get("last_name"), "George")

    def test_update_user_with_unauthorized_client(self):
        data = {
            "first_name": "Jhones",
            "last_name": "George",
        }
        response = self.unauthorized_client.put(
            f"/api/v1/users/{self.user.id}/", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 401)
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
            f"/api/v1/users/{7}/",
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Not found."})

    def test_get_list_user_without_admin_user(self):
        response = self.authorized_client.get("/api/v1/users/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."}
        )

    def test_get_list_user(self):
        response = self.admin_client.get("/api/v1/users/")
        response_data = response.json()
        response_count = len(response_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_count, 2)
