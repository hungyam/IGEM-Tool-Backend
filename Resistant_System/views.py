from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
import csv


# Create your views here.

# Import data in batches from CSV files
# The fields from left to right are (species, system, gene_name, protein_name)
def reloadData(request):
    Species.objects.all().delete()
    System.objects.all().delete()
    Data.objects.all().delete()
    Taxonomy.objects.all().delete()
    Uniport.objects.all().delete()
    return JsonResponse({
        "code": 200,
        "mes": "success"
    })


# Get all data --- `GET /data`
# Get data by key word --- `POST /data`
def data(request, page):
    pageSize = 50
    dataList = []
    request_body = request.body.decode('utf-8')
    request_dict = json.loads(request_body)
    system = request_dict['system']
    species = request_dict['species']
    name = request_dict['name']
    data = Data.objects.all()
    if system:
        data = data.filter(system__name__regex=system)
    if species:
        data = data.filter(species__name__regex=species)
    if name:
        data = data.filter(Accession__regex=name)
    length = len(data)
    data = data[page * pageSize: (page + 1) * pageSize]

    for curr in data:
        dataList.append({
            "id": curr.id,
            "assembly": curr.Assembly,
            "lociid": curr.LociID,
            "accession": curr.Accession,
            "contigid": curr.ContigID,
            "start": curr.Start,
            "end": curr.End,
            "species": curr.species.name,
            "system": curr.system.name,
            "organism": curr.Organism,
            "entry": curr.Entry
        })

    return JsonResponse({
        "code": 200,
        "data": dataList,
        "length": length
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


# Download All Data --- `GET /download`
# Download Data by id list --- `POST /download`
def download(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="ResistantSystemDataAll.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['id', 'Assembly', 'LociID', 'Accession', 'ContigID', 'Start', 'End', 'System', 'Species'])
    if request.method == 'GET':
        data = Data.objects.all()
        for curr in data:
            row = [curr.id, curr.Assembly, curr.LociID, curr.Accession, curr.ContigID, curr.Start, curr.End,
                   curr.system.name, curr.species.name]
            writer.writerow(row)
    elif request.method == 'POST':
        request_body = request.body.decode('utf-8')
        request_dict = json.loads(request_body)
        idList = request_dict['index']
        for id in idList:
            curr = Data.objects.get(id=id)
            row = [curr.id, curr.Assembly, curr.LociID, curr.Accession, curr.ContigID, curr.Start, curr.End,
                   curr.system.name, curr.species.name]
            writer.writerow(row)
    return response


def upload_page(request):
    return render(request, './UploadPage.html')


def upload_csv(request, type):
    system = request.POST.get('system')
    species = request.POST.get('species')
    species_obj = Species.objects.filter(name=species).first()
    system_obj = None
    if not species_obj:
        species_obj = Species(name=species)
        species_obj.save()

    if type == 1 or type == 2:
        system_obj = System.objects.filter(name=system, species=species_obj).first()
        if not system_obj:
            system_obj = System(name=system, species=species_obj)
            system_obj.save()

    dataList = []
    file = request.FILES.get('file')
    file_data = file.read().decode("utf-8")
    lines = file_data.split('\n')
    if type == 0:
        for line in lines:
            line = line.split(',')
            if len(line) > 1:
                data = Taxonomy(species=species_obj,
                                Assembly=line[0],
                                Organism=line[1])
                dataList.append(data)
        Taxonomy.objects.bulk_create(dataList)
    elif type == 1:
        for line in lines:
            line = line.split('\t')
            if len(line) > 1:
                data = Uniport(species=species_obj,
                               system=system_obj,
                               Accession=line[0],
                               Entry=line[1])
                dataList.append(data)
        Uniport.objects.bulk_create(dataList)
    else:
        for line in lines:
            line = line.split('\t')
            if len(line) > 1:
                data = Seed(Assembly=line[0],
                            LociID=line[1],
                            Accession=line[2],
                            ContigID=line[3],
                            Start=line[4],
                            End=line[5],
                            species=species_obj,
                            system=system_obj)
                dataList.append(data)
        Seed.objects.bulk_create(dataList)
    return JsonResponse({'msg': 'success'})


def mes(request):
    data = {}
    species_count = Species.objects.count()
    system_count = System.objects.count()
    data['species_count'] = species_count
    data['system_count'] = system_count
    data['archaea_count'] = 3412
    data['bacteria_count'] = 62291
    archaea = []
    for curr in System.objects.filter(species__name='Archaea'):
        obj = {'value': Data.objects.filter(system=curr).count(), 'name': curr.name}
        archaea.append(obj)
    data['archaea'] = archaea
    bacteria = []
    for curr in System.objects.filter(species__name='Bacteria'):
        obj = {'value': Data.objects.filter(system=curr).count(), 'name': curr.name}
        bacteria.append(obj)
    data['bacteria'] = bacteria
    return JsonResponse({'code': 200, 'data': data})


def join_table(request):
    Data.objects.all().delete()
    coursor = connection.cursor()
    coursor.execute(
        'SELECT Seed.*, Taxonomy.Organism, Uniport.Entry FROM Resistant_System_seed AS Seed LEFT JOIN Resistant_System_taxonomy AS Taxonomy ON Taxonomy.species_id = Seed.species_id AND Taxonomy.Assembly = Seed.Assembly LEFT JOIN Resistant_System_uniport AS Uniport ON Seed.species_id = Uniport.species_id AND Seed.system_id = Uniport.system_id AND Seed.Accession = Uniport.Accession')
    raw = coursor.fetchall()
    data_list = []
    for row in raw:
        organism = row[9]
        if not organism:
            organism = ''
        entry = row[10]
        if not entry:
            entry = ''
        data = Data(Assembly=row[1],
                    LociID=row[2],
                    Accession=row[3],
                    ContigID=row[4],
                    Start=row[5],
                    End=row[6],
                    species_id=row[7],
                    system_id=row[8],
                    Organism=organism,
                    Entry=entry)
        data_list.append(data)
    Data.objects.bulk_create(data_list)
    return JsonResponse({'code': 200})
