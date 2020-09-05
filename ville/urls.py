from django.urls import path        
from django.conf.urls import url, include

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from ville import views
# from .views import valide_upload, delete_upload

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("selection", views.selection, name="selection" ),
    # path("selection/rues/", views.rues, name="rues" ),                # utile ???
    path("selection/<value>/", views.monument, name="monument" ),
    path("selection/<value>/<slug>/", views.detail, name="detail" ),


    # Upload
    path("upload/", views.UploadView.as_view(), name="upload"),
    path("import/", views.import_xls, name="import"),
    # path("valide_upload/", valide_upload, name="valide_upload"),
    path("delete_upload/", views.delete_upload, name="delete_upload"),

    # Login / Logout
    path('accounts/', include('django.contrib.auth.urls')),

    # Gestion
    path("fiche_import_d/", views.fiche_import, name="fiche_import"),
    path("fiche_import_n/", views.fiche_import2, name="fiche_import2"),
    path("del_fiche/<value>/<slug>/", views.del_fiche, name="del_fiche"),
    path("modif/", views.modif_fiche, name="modif_fiche"),
    path("del_verif/<value>/<slug>/", views.del_verif, name="del_verif"),

    # Path recherche
    path('fiche_import_d/s/', views.search, name='search'),
   
]