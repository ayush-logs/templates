Model 
--
```md
save()
delete()
clean()
__str__()
```

Serializer
--
```md
validate_<field>()
validate()
create()
update()
to_representation()
```
View
--
```md
get_queryset()
get_serializer_class()
perform_create()
perform_update()
perform_destroy()
get_permissions()
```

---

Model
--
```python
class Product(models.Model):
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)
```

```python
def delete(self, *args, **kwargs):
    print("Deleting product")
    super().delete(*args, **kwargs)
```

```python
def clean(self):
    if self.price < 0:
        raise ValidationError("Price cannot be negative")
```
