from django.conf import settings
from django.test import TestCase

from aws_config import AWSHandler


class AWSHandlerTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # Mock settings attributes
        settings.UMAMI_PAGE_URL = "https://example.com"
        settings.UMAMI_WEBSITE_ID = "123456"
        settings.UMAMI_ENABLED = True

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
      ...

    def test_to_be_added(self):
        self.assertEqual(1, 1)