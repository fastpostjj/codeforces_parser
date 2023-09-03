from django.contrib import admin
from parsing.models import Problems, Tags, SendedProblems


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
        'solved_count'
    )

    list_display_links = (
        'id',
        'name',
        'contestId',
        'index',
        'points',
        'rating',
        'type_problem',
        'solved_count'
    )

    list_filter = (
        'name',
        'contestId',
        'index',
        'points',
        'rating',
        'type_problem',
        'solved_count'
    )

    search_fields = (
        'id',
        'name',
        'contestId',
        'index',
        'points',
        'rating',
        'type_problem',
        'solved_count'
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


@admin.register(SendedProblems)
class SendedProblemsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'problem',
        'datetimesend'
    )

    list_display_links = (
        'id',
        'user',
        'problem',
        'datetimesend'
    )

    list_filter = (
        'id',
        'user',
        'problem',
        'datetimesend'
    )

    search_fields = (
        'id',
        'user',
        'problem',
        'datetimesend'
    )
