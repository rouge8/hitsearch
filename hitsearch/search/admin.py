from search.models import Page, Link, Tag
from django.contrib import admin

class PageAdmin(admin.ModelAdmin):
    list_display = ("title" , "url", "discovery_time")
    list_filter = ["discovery_time"]
    search_fields = ["title"]

admin.site.register(Page,PageAdmin)

class LinkAdmin(admin.ModelAdmin):
    list_display = ( "source", "target")
    search_fields = ["source__url", "target__url"]  # Cant get this to work

admin.site.register(Link,LinkAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ( "tag", "page", "word_count")
    search_fields = ["tag", "page__url"]  # Cant get this to work

admin.site.register(Tag,TagAdmin)
