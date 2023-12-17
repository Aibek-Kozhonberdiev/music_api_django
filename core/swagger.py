from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Documentation for the music API",
      terms_of_service=settings.DOCS_TERMS_OF_SERVISE,
      contact=openapi.Contact(email=settings.DOCS_EMAIL),
      license=openapi.License(name=settings.DOCS_LICENSE),
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticated, )
)
