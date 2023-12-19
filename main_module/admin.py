from django.contrib import admin
from main_module import models

# Register your models here.
admin.site.register(models.CodrepoData)
admin.site.register(models.RedditData)
admin.site.register(models.TwitterData)
admin.site.register(models.FacebookData)
admin.site.register(models.TechIndicators)


class CodrepoDataInline(admin.TabularInline):
    model = models.CodrepoData


class RedditDataInline(admin.TabularInline):
    model = models.RedditData


class TwitterDataInline(admin.TabularInline):
    model = models.TwitterData


class FacebookDataInline(admin.TabularInline):
    model = models.FacebookData


class TechIndicatorsInline(admin.TabularInline):
    model = models.TechIndicators


@admin.register(models.Token)
class TokenAdmin(admin.ModelAdmin):
    inlines = [
        CodrepoDataInline,
        RedditDataInline,
        TwitterDataInline,
        FacebookDataInline,
        TechIndicatorsInline,
    ]
