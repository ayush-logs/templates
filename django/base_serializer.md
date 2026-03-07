```python 
"""
Base Serializers Template
=========================

Philosophy:
- Explicit is better than magical.
- Separate read and write concerns.
- Validate business logic at serializer layer.
- Keep serializers thin — complex logic belongs in services.
- Always assume public API exposure.

You are encouraged to adapt per project.
"""

from rest_framework import serializers
from django.db import transaction


# ==========================================================
# BASE MODEL SERIALIZER
# ==========================================================

class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer for all model serializers.

    Design Decisions:
    - Read-only id, created_at, updated_at by default.
    - Assumes UUID primary keys.
    - Safe defaults for production APIs.
    """

    id = serializers.UUIDField(read_only=True)

    class Meta:
        abstract = True
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        """
        Global object-level validation hook.

        Override in child serializers when needed.

        Keep business-heavy logic out of here.
        """
        return super().validate(attrs)


# ==========================================================
# WRITE SERIALIZER BASE
# ==========================================================

class BaseWriteSerializer(BaseModelSerializer):
    """
    Base class for create/update serializers.

    Design Decisions:
    - Wrapped in atomic transaction.
    - Explicit create/update methods.
    - Designed for future service layer injection.
    """

    @transaction.atomic
    def create(self, validated_data):
        """
        Override in child if custom creation logic is needed.
        """
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Override in child if custom update logic is needed.
        """
        return super().update(instance, validated_data)


# ==========================================================
# READ SERIALIZER BASE
# ==========================================================

class BaseReadSerializer(BaseModelSerializer):
    """
    Used for GET endpoints.

    Design Decisions:
    - Keeps representation logic clean.
    - Allows computed fields via SerializerMethodField.
    - No write-only fields.
    """

    class Meta(BaseModelSerializer.Meta):
        abstract = True


# ==========================================================
# SOFT DELETE SUPPORT SERIALIZER MIXIN
# ==========================================================

class SoftDeleteSerializerMixin:
    """
    Adds soft delete handling support.

    Assumes model has:
    - is_deleted
    - soft_delete() method

    Use when needed.
    """

    def delete(self, instance):
        if hasattr(instance, "soft_delete"):
            instance.soft_delete()
        else:
            instance.delete()


# ==========================================================
# EXAMPLE USAGE (E-COM READY)
# ==========================================================

"""
Below is an example implementation for Product.
This is here as a reference pattern.
"""

from apps.products.models import Product  # adjust per project


class ProductReadSerializer(BaseReadSerializer):
    """
    Product Read Serializer

    Design Decisions:
    - Exposes computed property is_in_stock.
    - Category returned as nested minimal representation.
    """

    is_in_stock = serializers.BooleanField(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta(BaseReadSerializer.Meta):
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "is_active",
            "is_in_stock",
            "category_name",
            "created_at",
        )


class ProductWriteSerializer(BaseWriteSerializer):
    """
    Product Write Serializer

    Design Decisions:
    - Accept category as primary key.
    - Slug uniqueness validated by model.
    - Keep business rules minimal here.
    """

    class Meta(BaseWriteSerializer.Meta):
        model = Product
        fields = (
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "is_active",
            "category",
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
```