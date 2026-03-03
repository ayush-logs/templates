```python
"""
Base Models Template
====================

This file contains production-ready base model abstractions
and conventions to be reused across projects.

Philosophy:
- Explicit > Implicit
- Extendable > Over-engineered
- Database integrity first
- Soft-deletes when business requires history
- Index intentionally
- Always design for future multi-user systems

You are encouraged to modify per project needs.
"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


# ==========================================================
# ABSTRACT BASE MODELS
# ==========================================================

class TimeStampedModel(models.Model):
    """
    Adds created_at and updated_at fields.

    Design Decision:
    - auto_now_add for immutable creation time
    - auto_now for automatic update tracking
    - Indexed because frequently filtered/sorted
    """

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDPrimaryKeyModel(models.Model):
    """
    UUID primary key base.

    Design Decision:
    - UUIDs are safer for public APIs.
    - Prevents predictable ID enumeration.
    - Good for distributed systems.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    """
    Custom QuerySet for soft delete support.
    """

    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    """
    Default manager excludes deleted records.
    """

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    """
    Soft delete base class.

    Design Decision:
    - Soft delete only when business requires recoverability.
    - Avoid if hard deletes are acceptable.
    """

    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # includes deleted

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])


# ==========================================================
# EXAMPLE DOMAIN MODEL (E-COM READY STRUCTURE)
# ==========================================================

class Category(UUIDPrimaryKeyModel, TimeStampedModel):
    """
    Product Category Model

    Design Decisions:
    - Slug must be unique for URL usage.
    - Self-referencing parent allows nested categories.
    - Indexed name for filtering/search.
    """

    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name


class Product(UUIDPrimaryKeyModel, TimeStampedModel, SoftDeleteModel):
    """
    Product Model

    Design Decisions:
    - Price uses Decimal (never Float).
    - Explicit stock field.
    - Index name for search.
    - on_delete=PROTECT prevents accidental category deletion.
    - Soft delete enabled for historical order consistency.
    """

    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    stock = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True, db_index=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["price"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.stock > 0 and self.is_active

```

# Production Principles & Rules

1. UUIDs instead of AutoField (prevents ID Enumeration attacks)
2. index fields moderately. 
3. use decimal for money, never floatfield
4. PROTECT instead of CASCADE. 
5. have explicit managers (allows querying deleted objects when needed)