from django.db import models


# Create your models here.
class Species(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class System(models.Model):
    name = models.CharField(max_length=100, unique=True)
    species = models.ForeignKey('Species', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Taxonomy(models.Model):
    species = models.ForeignKey('Species', on_delete=models.CASCADE)
    Assembly = models.CharField(max_length=100)
    Organism = models.CharField(max_length=1000)

    def __str__(self):
        return self.species.name + ' ' + self.Assembly

class Uniport(models.Model):
    species = models.ForeignKey('Species', on_delete=models.CASCADE)
    system = models.ForeignKey('System', on_delete=models.CASCADE)
    Accession = models.CharField(max_length=100)
    Entry = models.CharField(max_length=100)

    def __str__(self):
        return self.species.name + ' ' + self.system.name + ' ' + self.Accession


class Data(models.Model):
    Assembly = models.CharField(max_length=100)
    LociID = models.CharField(max_length=100)
    Accession = models.CharField(max_length=100)
    ContigID = models.CharField(max_length=100)
    Start = models.CharField(max_length=100)
    End = models.CharField(max_length=100)
    species = models.ForeignKey('Species', on_delete=models.CASCADE)
    system = models.ForeignKey('System', on_delete=models.CASCADE)
    Organism = models.CharField(max_length=1000, default='')
    Entry = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.species.name + ' ' + self.system.name + ' ' + self.Accession
