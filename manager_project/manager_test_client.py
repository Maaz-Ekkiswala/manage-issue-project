from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import UserProfile

Test_username = 'jack@nomail.com'
Test_password = 'password'
Test_first_name = 'jack'
Test_last_name = 'george'
Test_mobile = '9898989898'

ADMIN_USERNAME = "admin@xxx.com"
ADMIN_PASSWORD = "admin@123"
ADMIN_FIRST_NAME = "Admin"
ADMIN_LAST_NAME = "User"
ADMIN_MOBILE = "9090909090"


class ManagerTestClient(APITestCase):
    fixtures = ["apps/masters/fixtures/category.json"]

    @classmethod
    def setUpTestData(cls):
        super(ManagerTestClient, cls).setUpTestData()
        UserProfile.objects.create(
            username=Test_username,
            password=Test_password,
            first_name=Test_first_name,
            last_name=Test_last_name,
            mobile=Test_mobile,
            is_active=True,
        )

        UserProfile.objects.create(
            username=ADMIN_USERNAME,
            password=ADMIN_PASSWORD,
            first_name=ADMIN_FIRST_NAME,
            last_name=ADMIN_LAST_NAME,
            mobile=ADMIN_MOBILE,
            is_active=True,
            is_superuser=True,
            is_staff=True,
        )

    def setUp(self) -> None:
        super(ManagerTestClient, self).setUp()
        self.user = UserProfile.objects.filter(username=Test_username).first()
        self.admin_user = UserProfile.objects.get(username=ADMIN_USERNAME)
        admin_user_token = RefreshToken.for_user(self.admin_user)
        admin_user_access_token = str(admin_user_token.access_token)
        user_token = RefreshToken.for_user(self.user)
        user_access_key = str(user_token.access_token)
        self.authorized_client = APIClient(
            self.user, HTTP_AUTHORIZATION="Bearer " + user_access_key
        )
        self.unauthorized_client = APIClient(
            self.user
        )
        self.admin_client = APIClient(
            self.admin_user, HTTP_AUTHORIZATION="Bearer " + admin_user_access_token
        )