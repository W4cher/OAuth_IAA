from django.apps import AppConfig



class AuthenticationApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_api'

    def ready(self):
            from actstream import registry
            registry.register(self.get_model('CustomUser'))
            import auth_api.signals
            