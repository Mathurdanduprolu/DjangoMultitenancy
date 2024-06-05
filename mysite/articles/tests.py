from django.test import TestCase, Client
from django.urls import reverse
from tenants.models import Tenant
from .models import Article

class MultiTenancyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.tenant1 = Tenant.objects.create(name='Tenant 1', domain='tenant1.localhost')
        self.tenant2 = Tenant.objects.create(name='Tenant 2', domain='tenant2.localhost')
        self.article1 = Article.objects.create(tenant=self.tenant1, title='Article 1', content='Content for article 1')
        self.article2 = Article.objects.create(tenant=self.tenant2, title='Article 2', content='Content for article 2')
        print(self.tenant1)
        print(self.tenant2)

    def test_tenant1_articles(self):
        response = self.client.get(reverse('article_list'), HTTP_HOST='tenant1.localhost')
        print(f"Debug: response.status_code={response.status_code}")
        print(f"Debug: response.content={response.content}")
        self.assertContains(response, self.article1.title)
        self.assertNotContains(response, self.article2.title)

    def test_tenant2_articles(self):
        response = self.client.get(reverse('article_list'), HTTP_HOST='tenant2.localhost')
        print(f"Debug: response.status_code={response.status_code}")
        print(f"Debug: response.content={response.content}")
        self.assertContains(response, self.article2.title)
        self.assertNotContains(response, self.article1.title)
