from django.db import models


class Gmina(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Obwód(models.Model):
    name = models.TextField()
    gmina = models.ForeignKey(Gmina)
    carts = models.IntegerField(default=0)
    voters = models.IntegerField(default=0)

    def __str__(self):
        return self.name