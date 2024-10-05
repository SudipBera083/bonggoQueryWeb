from django.contrib import admin
from .models import Project, Collaboration, CodeSnippet
admin.site.register(Project)
admin.site.register(Collaboration)
admin.site.register(CodeSnippet)
# Register your models here.
