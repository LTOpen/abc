from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subcategories",
    )

    def __str__(self):
        return self.name


# Create your models here.
class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    from_account = models.ForeignKey(
        "accounts.Account", on_delete=models.CASCADE, related_name="from_account"
    )
    to_account = models.ForeignKey(
        "accounts.Account", on_delete=models.CASCADE, related_name="to_account"
    )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    categories = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="categories",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.amount} from {self.from_account} to {self.to_account}"
