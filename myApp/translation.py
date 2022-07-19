from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Problems)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)