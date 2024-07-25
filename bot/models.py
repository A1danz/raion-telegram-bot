from django.db import models
from django.db.models import Q, Case, When, Value, IntegerField
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")

    def __str__(self):
        return self.name


class VisibilityType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Visibility Type")
        verbose_name_plural = _("Visibility Types")

    def __str__(self):
        return self.name


class ThingManager(models.Manager):
    def search(self, query, visibility_type, offset=0, limit=10):
        return self.annotate(
            priority=Case(
                When(name__icontains=query, then=Value(1)),
                When(category__name__icontains=query, then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        ).filter(
            visibility_type=visibility_type
        ).order_by('priority', 'name')[offset:offset + limit]


class Thing(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"))
    colors = models.ManyToManyField(Color, verbose_name=_("Colors"))
    cost = models.PositiveIntegerField(verbose_name=_("Cost"), null=True)
    description = models.TextField(verbose_name=_("Description"), null=True)
    visibility_type = models.ForeignKey(VisibilityType, on_delete=models.CASCADE, verbose_name=_("Visibility Type"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    objects = ThingManager()

    class Meta:
        verbose_name = _("Thing")
        verbose_name_plural = _("Things")
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Photo(models.Model):
    thing = models.ForeignKey(Thing, related_name='photos', on_delete=models.CASCADE, verbose_name=_("Thing"))
    file_id = models.CharField(verbose_name=_("Tg file_id"))
    file_path = models.CharField(verbose_name=_("Tg file_path"))
    url = models.CharField(verbose_name=_("Url to photo"), null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))

    def __str__(self):
        return f"Photo for {self.thing.name} - {self.file_id}"
