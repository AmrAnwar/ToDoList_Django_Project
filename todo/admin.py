# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import (
    List,
    Task,
    Sublist,
    Profile,
    Project
)


class SublistInline(admin.TabularInline):
    model = Sublist
    extra = 1


class TaskListInline(admin.TabularInline):
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
    )
    model = Task
    extra = 1


class ListAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    inlines = [TaskListInline]


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']

    inlines = [SublistInline]

admin.site.register(List, ListAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Profile)
admin.site.register(Project)
