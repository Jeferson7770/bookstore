from rest_framework import serializers

from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True)
    products_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        many=True,
        source="product",  
    )
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total

    class Meta:
        model = Order
        fields = ["product", "products_id", "total"]

    def create(self, validated_data):
        products_data = validated_data.pop("product")

        order = Order.objects.create(**validated_data)

        order.product.set(products_data)

        return order
