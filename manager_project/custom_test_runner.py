# from django.test.runner import DiscoverRunner
#
# class CustomTestRunner(DiscoverRunner):
#
#     def run_tests(self, test_labels, extra_tests=None, **kwargs):
#         # First, run test cases in some specific order
#         test_cases = [
#             'apps.users.tests.test_views.UserViewTestCases',
#             'apps.projects.test.test_project.ProjectTestCases',
#         ]
#         suite = self.build_suite(test_cases)
#         result = self.run_suite(suite)
#
#         # Then, run all remaining test cases
#         remaining_test_cases = set(test_labels) - set(test_cases)
#         remaining_suite = self.build_suite(remaining_test_cases)
#         remaining_suite.run(result)
#         return self.suite_result(remaining_suite, result)