from django.contrib import admin
from parsing.models import Problems, Tags, Contest, Subscriptions


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'annotation'
        )

    list_display_links = (
        'id',
        'name',
        'annotation'
        )

    list_filter = (
        'name',
        'annotation'
        )

    search_fields = (
        'id',
        'name',
        'annotation'
        )


@admin.register(Problems)
class ProblemsAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'contestId',
        'index',
        'points',
        'rating',
        'type_problem',
        'solved_count',
        'contest'
    )

    list_display_links = (
        'id',
        'name',
        'contestId',
        'index',
        'points',
        'rating',
        'type_problem',
        'solved_count',
        'contest'
    )
    list_filter = (
        # 'name',
        'contestId',
        'index',
        'points',
        'rating',
        'type_problem',
        'solved_count',
        'contest'
    )

    search_fields = (
        'id',
        'name',
        'contestId',
        'index',
        'points',
        'rating',
        'type_problem',
        'solved_count',
        'contest'
    )


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        )

    list_display_links = (
        'id',
        'name',
        )

    list_filter = (
        'id',
        'name',
        )

    search_fields = (
        'id',
        'name',
        )


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'contest',
        'tag',
        'rating',
        'is_active'
    )

    list_display_links = (
        'user',
        'contest',
        'tag',
        'rating'
    )

    list_filter = (
        'user',
        'contest',
        'tag',
        'rating',
        'is_active'
    )

    search_fields = (
        'user',
        'contest',
        'tag',
        'rating',
        'is_active'
    )
