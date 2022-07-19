from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


@admin.register(Problems)
class ProblemAdmin(TranslationAdmin):
    prepopulated_fields = {'slug':('title', )}


admin.site.register(Feedback)


