import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from product.models import Product
from order.models import Order


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        # usuário e o token para autenticação
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        token.save()

        # credenciais do cliente para enviar o token
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100, category=[self.category]
        )
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        self.assertEqual(
            order_data["results"][0]["product"][0]["title"], self.product.title
        )
        self.assertEqual(
            float(order_data["results"][0]["product"][0]["price"]),
            float(self.product.price),
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["category"][0]["title"],
            self.category.title,
        )

    def test_create_order(self):
        product = ProductFactory()
        data = json.dumps({"products_id": [product.id], "user": self.user.id})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_order = Order.objects.get(user=self.user)
        self.assertIsNotNone(created_order)

    def test_get_single_order(self):
        """Testa buscar um único pedido (Retrieve)"""
        response = self.client.get(
            reverse("order-detail", kwargs={"version": "v1", "pk": self.order.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_data = json.loads(response.content)

        self.assertEqual(order_data["product"][0]["title"], self.product.title)

    def test_delete_order(self):
        """Testa deletar um pedido (Destroy)"""
        response = self.client.delete(
            reverse("order-detail", kwargs={"version": "v1", "pk": self.order.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())
