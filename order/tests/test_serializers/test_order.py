import pytest
from order.factories import OrderFactory, UserFactory
from product.factories import ProductFactory
from order.serializers.order_serializer import OrderSerializer
from order.models import Order


@pytest.mark.django_db
def test_order_serializer_calculation():
    # Os dois produtos estão usando a ProductFactory com preços definidos
    product_1 = ProductFactory(price=50.00)
    product_2 = ProductFactory(price=75.50)

    order = OrderFactory(product=(product_1, product_2))

    # Passamos o pedido para o Serializer
    serializer = OrderSerializer(order)
    data = serializer.data

    assert set(data.keys()) == {"product", "total"}
    assert len(data["product"]) == 2
    assert data["total"] == 125.50


def test_order_factory_build_without_save():
    order = OrderFactory.build()
    assert order.id is None


@pytest.mark.django_db
def test_order_serializer_creation():
    user = UserFactory()
    product_1 = ProductFactory(price=30.00)
    product_2 = ProductFactory(price=40.00)

    data = {"user": user.id, "products_id": [product_1.id, product_2.id]}

    serializer = OrderSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    order = serializer.save(user=user)

    assert order.id is not None
    assert order.product.count() == 2
    assert order.user == user
