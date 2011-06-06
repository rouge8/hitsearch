from search.models import Page, Link, Tag
from django.contrib import admin

class PageAdmin(admin.ModelAdmin):
    list_display = ("title" , "url", "discovery_time")

admin.site.register(Page,PageAdmin)

class LinkAdmin(admin.ModelAdmin):
    list_display = ( "source", "target")

admin.site.register(Link,LinkAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ( "tag", "page", "word_count", "term_frequency")

admin.site.register(Tag,TagAdmin)
