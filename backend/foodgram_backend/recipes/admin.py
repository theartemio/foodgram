from django.contrib import admin
from django.db.models import Count

from .models import Ingredient, Recipe, RecipeIngredient, ShortenedLinks, Tag


class SearchAdminMixin:
    """Миксин для поиска по названию."""

    search_fields = ("name",)


class IngredientInline(admin.StackedInline):
    """Инлайн для отображения связанных с рецептом ингредиентов."""

    model = RecipeIngredient
    extra = 0

@admin.register(Tag) 
class TagAdmin(SearchAdminMixin, admin.ModelAdmin):
    list_display = ("name", "slug")
    list_editable = ("slug",)
    list_display_links = ("name",)

@admin.register(Ingredient)
class IngredientAdmin(SearchAdminMixin, admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_editable = ("measurement_unit",)
    list_display_links = ("name",)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "name",
        "image",
        "text",
        "cooking_time",
        "total_faves",
    )
    search_fields = (
        "name",
        "author",
    )
    list_filter = ("tags",)
    list_display_links = ("name",)
    filter_horizontal = ("ingredients",)
    inlines = (IngredientInline,)
    readonly_fields = ("total_faves",)

    def total_faves(self, obj):
        return obj.faves_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            faves_count=Count("userlists_favorites_list")
        )
        return queryset

admin.site.register(ShortenedLinks)
