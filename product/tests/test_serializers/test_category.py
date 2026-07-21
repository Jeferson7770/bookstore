import pytest
from product.factories import CategoryFactory
from product.serializers.product_serializer import CategorySerializer


@pytest.mark.django_db
def test_category_serializer():
    # Cria a categoria via factory com dados completos
    category = CategoryFactory(
        title="Livros", slug="livros", description="Categoria de livros", active=True
    )

    # Serializa a categoria
    serializer = CategorySerializer(category)
    data = serializer.data

    # Valida se todos os campos definidos no serializer estão presentes e corretos
    assert data["title"] == "Livros"
    assert data["slug"] == "livros"
    assert data["description"] == "Categoria de livros"
    assert data["active"] is True
