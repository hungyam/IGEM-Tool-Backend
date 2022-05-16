from django.db import models


# Create your models here.
class Species(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class System(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Data(models.Model):
    species = models.ForeignKey('Species', on_delete=models.CASCADE)
    system = models.ForeignKey('System', on_delete=models.CASCADE)
    gene_name = models.CharField(max_length=100)
    protein = models.CharField(max_length=100)

    def __str__(self):
        return self.species.name + ' ' + self.system.name + ' ' + self.gene_name
