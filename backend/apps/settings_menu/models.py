from django.db import models


class MenuCategory(models.Model):
    name = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]


class MenuItem(models.Model):
    key = models.SlugField(max_length=80, unique=True)
    label = models.CharField(max_length=120)
    path = models.CharField(max_length=200)
    category = models.ForeignKey(MenuCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name="items")
    order = models.PositiveIntegerField(default=0)
    enabled = models.BooleanField(default=True)
    allowed_roles = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["order", "id"]


class CustomPage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(MenuCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name="custom_pages")
    content = models.TextField(blank=True)
    allowed_roles = models.JSONField(default=list, blank=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]
