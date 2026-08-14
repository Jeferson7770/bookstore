import pytest

from product.factories import ProductFactory, CategoryFactory
from product.serializers.product_serializer import ProductSerializer


@pytest.mark.django_db
def test_product_serializer_fields():
    # Categoria usando a factory
    category = CategoryFactory(title="Livros")

    # Produto associado a categoria criada
    product = ProductFactory(title="O Senhor dos Anéis", price=79.90, active=True, category=(category,))

    serializer = ProductSerializer(product)
    data = serializer.data

    assert set(data.keys()) == {
        "id",
        "title",
        "description",
        "price",
        "active",
        "category",
    }

    assert data["title"] == "O Senhor dos Anéis"
    assert float(data["price"]) == 79.90
    assert data["active"] is True

    assert len(data["category"]) == 1
    assert data["category"][0]["title"] == "Livros"
