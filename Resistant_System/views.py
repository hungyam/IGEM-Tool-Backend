import django.db
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
import csv


# Create your views here.

# Import data in batches from CSV files
# The fields from left to right are (species, system, gene_name, protein_name)
def reloadData(request):
    file = csv.reader(open('./Resistant_System/csv/init.csv'), delimiter=' ')
    dataList = []
    Species.objects.all().delete()
    System.objects.all().delete()
    Data.objects.all().delete()
    for row in file:
        species = Species(name=row[0])
        system = System(name=row[1])
        try:
            species.save()
        except django.db.IntegrityError:
            species = Species.objects.get(name=row[0])
            pass
        try:
            system.save()
        except django.db.IntegrityError:
            system = System.objects.get(name=row[1])
        data = Data(species=species, system=system, gene_name=row[2], protein_name=row[3])
        dataList.append(data)

    Data.objects.bulk_create(dataList)
    return JsonResponse({
        "code": 200,
        "mes": "success"
    })


# Get all data --- `GET /data`
# Get data by key word --- `POST /data`
@csrf_exempt
def data(request):
    dataList = []
    if request.method == 'GET':
        data = Data.objects.all()
    elif request.method == 'POST':
        request_body = request.body.decode('utf-8')
        request_dict = json.loads(request_body)
        type = request_dict['type']
        keyword = request_dict['keyword']
        if type == 'species':
            data = Data.objects.filter(species__name__regex=keyword)
        elif type == 'system':
            data = Data.objects.filter(system__name__regex=keyword)
        else:
            data = Data.objects.filter(gene_name__regex=keyword) | Data.objects.filter(protein_name__regex=keyword)

    for curr in data:
        dataList.append({
            "species": curr.species.name,
            "system": curr.system.name,
            "gene": curr.gene_name,
            "protein": curr.protein
        })

    return JsonResponse({
        "code": 200,
        "data": dataList
    })


# Get all species --- `GET /species`
def species(request):
    dataList = []
    if request.method == 'GET':
        data = Species.objects.all()
        for curr in data:
            dataList.append(curr.name)

    return JsonResponse({
        "code": 200,
        "species": dataList
    })


# Get all kinds of resistant system --- `GET /system`
def system(request):
    dataList = []
    if request.method == 'GET':
        data = System.objects.all()
        for curr in data:
            dataList.append(curr.name)

    return JsonResponse({
        "code": 200,
        "species": dataList
    })
