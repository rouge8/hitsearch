from search.models import Page, Link, Tag
from django.contrib import admin

class PageAdmin(admin.ModelAdmin):
    list_display = ("title" , "url", "discovery_time")
    list_filter = ["discovery_time"]
    search_fields = ["title"]

admin.site.register(Page,PageAdmin)

class LinkAdmin(admin.ModelAdmin):
    list_display = ( "source", "target")
    list_filter = ["source"]
    #search_fields = ["source", "target"]  # Cant get this to work

admin.site.register(Link,LinkAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ( "tag", "page", "word_count", "term_frequency")
    list_filter = ["tag","page"]
    #search_fields = ["tag", "page"]  # Cant get this to work

admin.site.register(Tag,TagAdmin)
