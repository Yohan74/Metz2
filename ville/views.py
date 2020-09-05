from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages

#Upload
from django.views.generic import View, TemplateView  # + Login / Logout
from django.core.files.storage import FileSystemStorage
import os

#Login / Logout
from django.contrib.auth import authenticate, login, logout
from django.conf import settings


from .models import SELECTION, Noms, Dates
from .forms import Upload_Form
from ville import import_test

# Create your views here.

def accueil (request) :
    return render (request,'ville/accueil.html')


def selection (request) :

    context = {
        "selection" : SELECTION
    }

    return render (request,'ville/selection.html', context)


# def rues (request) :
#     context = {}

#     return render (request,'ville/rues.html', context)


def monument (request,value) :
    for a, b in SELECTION :
        if b == value :
            value = a 

    monuments = Noms.objects.filter(selection=value)

    context = {
        "value" : value,
        "monuments" : monuments,
    }

    return render (request,'ville/monument.html', context)


def detail (request, value, slug) : 

    detail_nom = Noms.objects.get(slug=slug,selection=value)
    nom = detail_nom.nom

    context = {
        'nom' : nom,
        'detail_nom' : detail_nom,
    }

    return render (request,'ville/detail.html', context)


def fiche_import (request) :
    fiche_imports = Noms.objects.all().order_by("slug")

    context = {
        "selections" : SELECTION,
        "trie" : "1",
        "fiche_imports" : fiche_imports ,
    }

    return render (request,'ville/fiche_import.html', context)


def fiche_import2 (request) :
    fiche_imports = Noms.objects.all().order_by("creation")

    context = {
        "selections" : SELECTION,
        "trie" : "2",
        "fiche_imports" : fiche_imports ,
    }

    return render (request,'ville/fiche_import.html', context)


def search (request):
    try:
        q = request.GET.get('q')
        r = request.GET.get('r')
    except:
        q = None

    if q :
        fiche_imports = Noms.objects.filter(nom__icontains=q).order_by("slug")

    elif r :
        fiche_imports = Noms.objects.filter(selection__icontains=r).order_by("slug")
    else:
        return redirect ("fiche_import")

    context = {
        "selections" : SELECTION,
        'r': r,
        'q' : q ,
        "fiche_imports" : fiche_imports,
        }
    return render (request,'ville/fiche_import.html', context)


def del_fiche (request, value, slug) :
    fiche = Noms.objects.get(selection=value, slug=slug)
    fiche.delete()
    messages.warning(request, "La fiche a bien été supprimé")

    return redirect("fiche_import")


def import_xls (request):
    num_monument, name_monument, rem_monument, list_monument, files = import_test.import_ext_xls()
    slug = name_monument.lower().replace(" ","_")

    if request.method == 'POST':

        form = Upload_Form(request.POST or None)

        if form.is_valid():
            selection = form.cleaned_data['selection']
            verification = form.cleaned_data['verification']
            test_nom_selection = Noms.objects.filter(nom=name_monument, selection=selection)
            test_nom = Noms.objects.filter(nom=name_monument)

            if not test_nom_selection :

                if test_nom :
                    messages.warning(
                        request, "Importation effectuée mais fiche déjà présente sous un autre style de monument.")

                add_monument = Noms(
                        nom=name_monument,
                        selection = selection,
                        verification = verification,
                        slug = slug,
                        )

                add_monument.save()                        # A REMETTRE

                for date, historique, remarque in list_monument :
                    
                    add_date = Dates(
                        nom = Noms.objects.get(nom=name_monument, selection=selection),       ## LA JE NE SAISI PAS TROP pourquoi je dois prendre un object.get
                        date = date,
                        historique = historique,
                        remarque = remarque,
                    )

                    add_date.save()                       # A REMETTRE

                messages.info(
                    request, "Importation réussie")

            elif test_nom_selection :

                messages.warning(
                    request, "Importation non effectuée car fiche déjà présente.")

            delete_upload(request)
            # for f in files :                  # Ne pas OUBLIER DE REMETTRE AINSI QUE Ligne 124
            #     if f.endswith(".xls") or f.endswith(".xlsx")  : 
            #         os.remove(f)
            # form = Upload_Form()
            return redirect("upload")

        else :
            print("Form IMPORT_xls non valide")

    else :
        form = Upload_Form()

    context = {
        "num_monument": num_monument,
        "name_monument":name_monument,
        "rem_monument":rem_monument,
        "list_monument" : list_monument,
        "form" : form,
    }

    return render (request,'ville/import.html', context)

class UploadView(View):

    def post(self, *args, **kwargs):

            if self.request.method == "POST" :
                uploaded_file = self.request.FILES['document']  # document viens du name dans input de upload.html
                name_data = uploaded_file.name

                ## name_data contient le nom du fichier => doit finir par xls

                fs = FileSystemStorage()
                fs.save(uploaded_file.name, uploaded_file)   # A REMETTRE AINSI QUE LE DELETE dans Valide_upload

                try :
                    num_monument, name_monument, rem_monument, list_monument, files = import_test.import_ext_xls()
                except :
                    delete_upload(self.request)
                    messages.warning(
                        self.request, "La présentation de la fiche n'est pas conforme.")
                    return redirect("upload")


                context = {
                    "num_monument": num_monument,
                    "name_monument":name_monument,
                    "rem_monument":rem_monument,
                }

                return redirect("import")

            return redirect("upload")

    def get(self, *args, **kwargs):
        return render (self.request, 'ville/upload.html')


def delete_upload (request):

    files = import_test.import_path_xls()

    for f in files :                  # Ne pas OUBLIER DE REMETTRE AINSI QUE Ligne 124
        if f.endswith(".xls") or f.endswith(".xlsx") : 
            os.remove(f)

    return redirect("upload")


def modif_fiche (request) : 

    modif_fiches = Noms.objects.filter(verification=True)

    context = {
        "modif_fiches" : modif_fiches,
    }

    return render (request, 'ville/modification.html', context)


def del_verif (request, value, slug) :

    fiche = Noms.objects.get(selection=value, slug=slug, verification=True)
    fiche.verification = False
    fiche.save()
    mess = "La fiche \"<b>" + fiche.nom + "</b> <i>(" + fiche.selection + ")</i>" + "\" n'est plus marquée à revoir. Pensez à la réimporter après modification."
    messages.info(request, mess)

    del_fiche(request, value, slug)

    return redirect("upload")

def test (request) :

    context = {}

    return render (request, 'ville/test.html', context)