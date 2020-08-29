import os
import glob
import xlrd
import datetime

from ville import views


def import_ext_xls() :



    # uploaded_file = views.upload()

    # fs = views.upload()
    # print("name import : ",name_data)
    # print("fs import : ",fs)

    # print("TEST de LANCEMENT")


    # num_monument = 9
    # name_monument = "Cathédrale"
    # rem_monument = "ou Eglise"

    # dict_monument = {
    #         "XIV°": "Il est situé au n° 20 de la rue Chèvremont  Son portail et sa tour carrée sont remarquables  La vierge de sa belle niche d'angle a disparue.  La cour intérieure, entourée de bâtiments, débouche à l'arrière sur des jardins.      &&&  Le nom est certainement du à son escarpement.      de la rue des Jardins.",
    #         "1518-1527": "Le Maître verrier Valentin BOUSCH y vécu. Il y possédait ses ateliers dans lesquels il conçu les vitraux de la Cathédrale. &&&",
    # }

    # return num_monument, name_monument, rem_monument, dict_monument

    # name_data = "Chalverson.xls"
    # name_data = "Burtaigne.xls"
   
    # CUR_DIR = os.path.dirname(__file__)
    # DATA_DIR = os.path.join(CUR_DIR, name_data)

    # CUR_DIR = os.path.join(os.getcwd(),"media")
    # DATA_DIR = os.path.join(CUR_DIR, name_data)

    # print("c'est le CUR_DIR :",CUR_DIR)
    # print("c'est le DATA_DIR :",DATA_DIR)
                                                                # # POUR MEMOIRE : cell = cell(row,col)

    CUR_DIR2 = os.path.join(os.getcwd(),"media/**")
    files = glob.glob(CUR_DIR2, recursive=True)

    #################################################### Gestion feuille XLS

    # document = xlrd.open_workbook(DATA_DIR)
    document = xlrd.open_workbook(files[1])


    feuille_1 = document.sheet_by_index(0)

    num_monument = str(int(feuille_1.cell_value(0, 0)))
    name_monument = (feuille_1.cell_value(0, 1))
    name_monument = " ".join(name_monument.split())
    rem_monument = (feuille_1.cell_value(0, colx=2))

    cols = feuille_1.ncols      # Nombre de colonne
    rows = feuille_1.nrows      # Nombre de ligne


    #################################################### COLONNE DATE : 
    list_dates = []
    for r in range(2, rows):
        if feuille_1.cell_type(rowx=r, colx=0) == 1 or feuille_1.cell_type(rowx=r, colx=0) == 6  :          # Cellule Texte ou Vide
            list_dates += [feuille_1.cell_value(rowx=r, colx=0)]
        elif feuille_1.cell_type(rowx=r, colx=0) == 3:                                                      # Cellule Date
            ms_date_number = feuille_1.cell_value(rowx=r, colx=0)
            year, month, day, hour, minute, second = xlrd.xldate_as_tuple(ms_date_number, document.datemode)
            py_date = datetime.datetime(year, month, day)
            py_date = py_date.strftime("%d-%m-%Y")
            list_dates += [py_date]
        elif feuille_1.cell_type(rowx=r, colx=0) == 2:                                                      # Cellule Nombre
            py_num = str(int(feuille_1.cell_value(rowx=r, colx=0)))
            list_dates += [py_num]
        else :                                                                                              # Cellule "autre"  /!\ WARNING /!\
            list_dates += [feuille_1.cell_value(rowx=r, colx=0)]


    #################################################### COL HITORIQUE :
    list_historique= []
    for r in range(2, rows):
        list_historique += [feuille_1.cell_value(rowx=r, colx=1)]


    #################################################### COL REMARQUE :
    list_remarque = []
    for r in range(2, rows):
        list_remarque += [feuille_1.cell_value(rowx=r, colx=2)]


    #########################################################  TEST

    # Il FAUT GARDER LA COMPARAISON ENTRE LES LISTES : len(list_dates) == len(list_historique) == len(list_remarque)
    nb_list_dates = len(list_dates)
    nb_list_historique = len(list_historique)
    nb_list_remarque = len(list_remarque)


    #########################################################  Création des listes

    i = 0

    while i < nb_list_dates :
        if list_dates[i] != "" and list_historique[i] != "" and list_dates[i-1] == "" and list_historique[i-1] == ""  :
            list_dates[i-1] = list_historique[i-1] = list_remarque[i-1] = "&&&"
        i += 1

    list_historique = ' '.join(list_historique)
    list_historique = list_historique.split("&&&")

    list_dates = ' '.join(list_dates)
    list_dates = list_dates.split("&&&")

    list_remarque = ' '.join(list_remarque)
    list_remarque = list_remarque.split("&&&")

    for dates in reversed(list_dates) :
        if dates == "" or dates == " " :
            list_dates.remove(dates)
    for n, m in enumerate(list_dates) :
        m = m.strip()
        list_dates[n] = m

    for historique in reversed(list_historique) :
        if historique == "" or historique == " " :
            list_historique.remove(historique)
    for n, m in enumerate(list_historique) :
        m = m.strip()
        list_historique[n] = m


    for remarque in reversed(list_remarque) :
        if remarque == "" :
            list_remarque.remove(remarque)
    for n, m in enumerate(list_remarque) :
        m = m.strip()
        list_remarque[n] = m



    list_monument = zip(list_dates,list_historique,list_remarque)

    return num_monument, name_monument, rem_monument, list_monument, files
