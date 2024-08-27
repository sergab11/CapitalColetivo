from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('campanhas/', include('campanhas.urls')),
    path('contribuicoes/', include('contribuicoes.urls')),
    path('navegacao/', include('navegacao.urls')),
    path('organizacoes/', include('organizacoes.urls')),
    path('projetos/', include('projetos.urls')),
    path('', include('usuarios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)