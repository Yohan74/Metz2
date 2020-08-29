from django.db import models

# Create your models here.

SELECTION = (
    # ('NOM1', 'NOM2'),                 # NOM1 apparait             / NOM2 apparait dans le path
    # ('Quartier', 'Quartier'),
    ('Eglise', 'Eglise'),
    ('Cathédrale', 'Cathédrale'),
    ('Fermes-Châteaux','Fermes-Châteaux'),
    ('Maisons','Maisons'),
    ('Greniers','Greniers'),
    ('Musées','Musées'),
    ('Ponts','Ponts'),
    ('Plans de la ville','Plans'),
    ('Remparts - Fortifications','Remparts-Fortifications'),
    ('Hôtels particuliers','Hôtels_particuliers'),
)

class Noms (models.Model):
    selection = models.CharField(choices=SELECTION, max_length=25)
    nom = models.CharField(max_length=120)
    slug = models.SlugField()
    # image = models.ImageField(upload_to="static/img/", null=True)
    verification = models.BooleanField(default=False)
    creation = models.DateTimeField(auto_now_add=True, auto_now=False)      # True / False
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__ (self):       
        return self.nom


class Dates (models.Model):
    nom = models.ForeignKey(Noms, on_delete=models.CASCADE)
    date = models.CharField(max_length=120)
    historique = models.TextField()
    remarque = models.CharField(max_length=120, null=True, blank=True)

    def __str__ (self):       
        return self.date


