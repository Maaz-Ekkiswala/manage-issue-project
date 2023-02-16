import json

from rest_framework import status

from apps.issues.constants import Type, Status, Priority
from apps.projects.test.test_project import ProjectTestCases
from manager_project.manager_test_client import ManagerTestClient


# Create your tests here.

class IssuesTestCases(ManagerTestClient):
    fixtures = ["apps/projects/fixtures/projects.json"]
    def test_create_issue(self):
        data = {
            "title": "This is test_issue",
            "type": Type.TASK,
            "status": Status.PENDING,
            "priority": Priority.LOW,
            "description": "This issue is created for test and testing",
            "reported_id": self.user.id
        }
        response = self.authorized_client.post(
            path=f"/api/v1/issues/?1",
            data=json.dumps(data),
            content_type='application.json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)