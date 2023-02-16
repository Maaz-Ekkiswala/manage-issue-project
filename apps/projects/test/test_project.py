import json

from rest_framework import status

from manager_project.manager_test_client import ManagerTestClient


# Create your tests here.
class ProjectTestCases(ManagerTestClient):

    def create_project(self):
        data = {
            "name": "Software_Project",
            "url": "/test/url/software_project",
            "description": "This is test software project",
            "category": 1
        }
        response = self.admin_client.post(
            path="/api/v1/projects/",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.json()

    def test_create_project(self):
        data = {
            "name": "test_project",
            "url": "/test/url/project",
            "description": "This is test project",
            "category": 2
        }
        response = self.admin_client.post(
            path="/api/v1/projects/",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), "test_project")
        self.assertEqual(response.data.get("url"), "/test/url/project")
        self.assertEqual(response.data.get("description"), "This is test project")

    def test_create_project_with_authenticated_client(self):
        data = {
            "name": "test_project",
            "url": "/test/url/project",
            "description": "This is test project",
            "category": 2
        }
        response = self.authorized_client.post(
            path="/api/v1/projects/",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."}
        )

    def test_create_project_without_required_fields(self):
        data = {
            "url": "/test/url/project",
            "description": "This is test project",
            "category": 2
        }
        response = self.admin_client.post(
            path="/api/v1/projects/",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_project_with_unauthorized_client(self):
        data = {
            "url": "/test/url/project",
            "description": "This is test project",
            "category": 2
        }
        response = self.unauthorized_client.post(
            path="/api/v1/projects/",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {"detail": "Authentication credentials were not provided."}
        )

    def test_update_project(self):
        project_id = self.create_project().get("id")
        data = {
            "name": "Business_Project",
            "url": "/test/url/business_project",
            "description": "This is test business project",
            "category": 3
        }
        response = self.admin_client.put(
            path=f"/api/v1/projects/{project_id}/",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "Business_Project")
        self.assertEqual(response.data.get("url"), "/test/url/business_project")
        self.assertEqual(response.data.get("description"), "This is test business project")

    def test_update_project_with_authorized_client(self):
        project_id = self.create_project().get("id")
        data = {
            "name": "Business_Project",
            "url": "/test/url/business_project",
            "description": "This is test business project",
            "category": 3
        }
        response = self.authorized_client.put(
            path=f"/api/v1/projects/{project_id}/",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."}
        )

    def test_update_project_with_different_id(self):
        data = {
            "name": "Business_Project",
            "url": "/test/url/business_project",
            "description": "This is test business project",
            "category": 3
        }
        response = self.admin_client.put(
            path=f"/api/v1/projects/8/",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Not found."})

    def test_get_project_by_id(self):
        project_id = self.create_project().get("id")
        response = self.admin_client.get(
            path=f"/api/v1/projects/{project_id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_project_with_different_id(self):
        response = self.admin_client.get(
            path=f"/api/v1/projects/9/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(), {
            "message": "Project not found"
        })

    def test_get_project_by_id_with_authorize_client(self):
        project_id = self.create_project().get("id")
        response = self.authorized_client.get(
            path=f"/api/v1/projects/{project_id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_project_users(self):
        project_id = self.create_project().get("id")
        data = [
            {
                "assign_to": self.user.id
            },
            {
                "assign_to": self.admin_user.id
            }
        ]
        response = self.admin_client.post(
            path=f"/api/v1/projects/{project_id}/project-users/",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_project_users_with_authorized_client(self):
        project_id = self.create_project().get("id")
        data = [
            {
                "assign_to": self.user.id
            },
            {
                "assign_to": self.admin_user.id
            }
        ]
        response = self.authorized_client.post(
            path=f"/api/v1/projects/{project_id}/project-users/",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."}
        )

    def test_get_list_of_projects(self):
        response = self.authorized_client.get(path='/api/v1/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_of_project_with_different_url(self):
        response = self.authorized_client.get(path="/api/v1//projects/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND  )
