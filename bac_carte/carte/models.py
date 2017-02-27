import os
from django.db import models
from django.utils.safestring import mark_safe


class Marque(models.Model):
    name = models.CharField(max_length=75,
                            help_text="Nom de la marque")

    def __str__(self):
        return self.name


class Composant(models.Model):
    name = models.CharField(max_length=75,
                            help_text="Nom du composant")

    def __str__(self):
        return self.name


class Utilisation(models.Model):
    name = models.CharField(max_length=75,
                            help_text="Nom de l'utilisation")

    def __str__(self):
        return self.name


class TissuImage(models.Model):
    name = models.CharField(max_length=75,
                            help_text="Nom de l'image")
    image = models.ImageField()

    def image_tag(self):
        return mark_safe("<img src='{}' />".format(self.image.url))

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.name


class Carte(models.Model):
    marque = models.ForeignKey(Marque)
    ref = models.CharField(max_length=75,
                           help_text="Référence",
                           unique=True)
    largeur = models.FloatField(help_text="Largeur",
                                blank=True,
                                null=True)
    raccord = models.FloatField(help_text="Raccord",
                                blank=True,
                                null=True)
    prix = models.FloatField(help_text="Prix",
                              blank=True,
                              null=True)
    compositions = models.ManyToManyField(Composant,
                                          through='Composition',
                                          help_text="Composition",
                                          blank=True)
    utilisations = models.ManyToManyField(Utilisation,
                                         help_text="Utilisation",
                                         blank=True)
    images = models.ManyToManyField(TissuImage,
                                    help_text="Pictogramme d'information",
                                    blank=True)

    def images_latex(self):
        a = ""
        for image in self.images.all():
            a += "\includegraphics[width=2cm]{%s}" % (image.image.file)
        return a

    def __str__(self):
        return self.ref


class Composition(models.Model):
    carte = models.ForeignKey(Carte)
    composant = models.ForeignKey(Composant)
    pourcentage = models.FloatField(help_text="Pourcentage du composant dans"
                                              "le tissu")

    def __str__(self):
        return "{}% - {}".format(self.composant,
                                 self.pourcentage * 100)
