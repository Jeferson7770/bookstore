import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from product.factories import CategoryFactory
from product.models import Category


class CategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="books", slug="books")

    def test_get_all_category(self):
        response = self.client.get(reverse("category-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category_data = json.loads(response.content)

        self.assertEqual(category_data["results"][0]["title"], self.category.title)

    def test_create_category(self):
        data = {"title": "technology", "slug": "technology"}

        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}),
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_category = Category.objects.get(title="technology")
        self.assertEqual(created_category.title, "technology")

    # --- TESTES DO CRUD ---

    def test_get_single_category(self):
        """Testa buscar uma categoria específica (Retrieve / GET by ID)"""
        response = self.client.get(
            reverse("category-detail", kwargs={"version": "v1", "pk": self.category.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category_data = json.loads(response.content)
        self.assertEqual(category_data["title"], self.category.title)

    def test_update_category(self):
        """Testa atualizar uma categoria (Update / PUT)"""
        data = {"title": "books updated", "slug": "books-updated"}
        response = self.client.put(
            reverse(
                "category-detail", kwargs={"version": "v1", "pk": self.category.id}
            ),
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.title, "books updated")

    def test_delete_category(self):
        """Testa remover uma categoria (Delete / DESTROY)"""
        response = self.client.delete(
            reverse("category-detail", kwargs={"version": "v1", "pk": self.category.id})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

        # import pdb; pdb.set_trace() Serve para encontrar erros
