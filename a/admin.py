from django.contrib import admin
from django.apps import apps

app = apps.get_app_config('a')

for model_name, model in app.models.items():
    exclude = ['baseuser_groups', 'baseuser_user_permissions']
    if model_name not in exclude:
        admin.site.register(model)
