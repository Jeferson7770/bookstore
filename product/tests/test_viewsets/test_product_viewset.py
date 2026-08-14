import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory
from product.models import Product


class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        token.save()
        self.category = CategoryFactory()
        self.product = ProductFactory(
            title="pro controller",
            price=200.00,
            category=[self.category],
        )

    def test_get_all_product(self):
        """Testa listar produtos publicamente (sem token)"""
        response = self.client.get(reverse("product-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_data = json.loads(response.content)

        self.assertEqual(product_data["results"][0]["title"], self.product.title)
        self.assertEqual(float(product_data["results"][0]["price"]), float(self.product.price))
        self.assertEqual(product_data["results"][0]["active"], self.product.active)

    def test_create_product(self):
        """Testa criar produto"""
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = json.dumps({"title": "notebook", "price": 800.00, "categories_id": [self.category.id]})

        response = self.client.post(
            reverse("product-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_product = Product.objects.get(title="notebook")

        self.assertEqual(created_product.title, "notebook")
        self.assertEqual(float(created_product.price), 800.00)

    # --- TESTES DO CRUD ---

    def test_get_single_product(self):
        """Testa buscar um único produto publicamente (sem token)"""
        response = self.client.get(reverse("product-detail", kwargs={"version": "v1", "pk": self.product.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_data = json.loads(response.content)
        self.assertEqual(product_data["title"], self.product.title)

    def test_update_product(self):
        """Testa atualizar um produto (PUT)"""
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {
            "title": "pro controller updated",
            "price": 250.00,
            "categories_id": [self.category.id],
        }
        response = self.client.put(
            reverse("product-detail", kwargs={"version": "v1", "pk": self.product.id}),
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.title, "pro controller updated")
        self.assertEqual(float(self.product.price), 250.00)

    def test_delete_product(self):
        """Testa deletar um produto (Destroy)"""
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.delete(reverse("product-detail", kwargs={"version": "v1", "pk": self.product.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
