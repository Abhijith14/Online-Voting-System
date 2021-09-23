import mimetypes

from django.http import HttpResponse
from django.shortcuts import render

from .models import add_c_model

from PIL import Image, ImageDraw, ImageFont
import cv2
import pytesseract
from pytesseract import Output

import os.path
import collections
from wsgiref.util import FileWrapper

import project_files

# Create your views here.

threshold = {'President' : 1,
             'Vice President' : 2,
             'General Secretary': 1,
             'Joint Secretary': 1,
             'Treasurer': 1,
             'E.C.Members' : 9,
             'E.C.Member(Women)': 1,
             'Warden': 1}

ocr_dir = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

saved_files = []


def homepage_view(request):
    return render(request, 'home.html', {})


def start_voting(request):
    if request.method == "POST":

        object = add_c_model.objects.all()

        variables = list(request.POST)

        variables.remove('csrfmiddlewaretoken')
        variables.remove('cat')
        variables.remove('subBtn')

        print(variables)

        if len(variables) > 0:
            for i in variables:
                object1 = list(object.filter(id=int(i)).values())
                curr_v = int(object1[0]['Votes'])
                cand = object1[0]['Candidate']
                cate = object1[0]['Category']

                if len(variables) <= threshold[cate]:
                    print(curr_v)
                    data = add_c_model(id=int(i), Candidate=cand, Category=cate, Votes=curr_v+1)
                    data.save()
                else:
                    print("Greater than threshold !!!!")

    return start_category_voting(request)


def start_category_voting(request):

    if request.method == "GET":
        category = request.GET.get('cat')
    elif request.method == "POST":
        category = request.POST.get('cat')

    object = add_c_model.objects.all()
    object = list(object.filter(Category=category).values())

    context = {}

    context['Heading'] = category

    context['Data'] = object

    return render(request, 'add_votes.html', context)


def add_candidates_view(request):
    context = {}

    object = add_c_model.objects.all()
    object = list(object.values())

    print(object[-1]['id'] + 1)

    try:
        context['curr_id'] = object[-1]['id'] + 1
    except:
        context['curr_id'] = 1

    return render(request, 'add_cand.html', context)


def add_candidates_code(request):
    context = {}
    if request.method == "POST":

        name_C = request.POST.get('name_C')
        role_C = request.POST.get('role_C')

        id_C = request.POST.get('id_C')

        print("HELLO", id_C)


        object = add_c_model.objects.all()

        object = list(object.filter(id=id_C).values())

        if len(object) == 0:
            data = add_c_model(id=id_C, Candidate=name_C, Category=role_C)
            data.save()
            context['message'] = "Candidate Added Successfully !!"

        else:
            context['message'] = "Candidate Already Exists... !!"

        object = add_c_model.objects.all()
        object = list(object.values())

        print("Returned id : ", object[-1]['id'] + 1)

        try:
            context['curr_id'] = object[-1]['id'] + 1
        except:
            context['curr_id'] = 1

    else:
        context['message'] = "Data Upload Failed !!"

    return render(request, 'add_cand.html', context)


def find_text_distance(txt_passed, font):
    bimg = Image.open("project_files/blank.png")
    draw2 = ImageDraw.Draw(bimg)
    draw2.text(xy=(0, 0), text='{}'.format(str(txt_passed).replace(" ", "-")), fill=(0, 0, 0), font=font)
    bimg.save("project_files/test.png")

    pytesseract.pytesseract.tesseract_cmd = ocr_dir

    img = cv2.imread("project_files/test.png")

    d = pytesseract.image_to_data(img, output_type=Output.DICT)

    for i in d['text']:
        if i == str(txt_passed).replace(" ", "-"):
            ind1 = d['text'].index(i)
            x1 = d['left'][ind1]
            y1 = d['top'][ind1]
            w1 = d['width'][ind1]
            h1 = d['height'][ind1]
            x2 = x1 + w1
            y2 = y1 + h1

    dist = ((((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5)

    return dist


def heading(img, txt):
    font = ImageFont.truetype('project_files/fonts/Montserrat-ExtraBold.ttf', 70)
    draw = ImageDraw.Draw(img)

    x = ((1761049**0.5) - find_text_distance(txt, font))/2
    y = 154

    draw.text(xy=(x, y), text=txt, fill=(0, 0, 0), font=font)


def names(img, txt, num):
    font = ImageFont.truetype('project_files/fonts/Montserrat-ExtraBold.ttf', 40)
    draw = ImageDraw.Draw(img)

    x = 150
    y = 500 + num

    draw.text(xy=(x, y), text=txt, fill=(0, 0, 0), font=font)


def votes(img, txt, num):
    font = ImageFont.truetype('project_files/fonts/Montserrat-ExtraBold.ttf', 40)
    draw = ImageDraw.Draw(img)

    x = 1100
    y = 500 + num

    draw.text(xy=(x, y), text=txt, fill=(0, 0, 0), font=font)


def create_img(data):

    global saved_files

    category_txt = data[0]['Category']

    newImg = 'project_files/design.png'  # Design
    img = Image.open(newImg)

    heading(img, category_txt)

    for i in range(len(data)):
        names(img, data[i]['Candidate'], 43 + (97 * i))
        votes(img, str(data[i]['Votes']), 43 + (97 * i))


    base_dir = 'project_files/output/'
    filename = '{}'.format(category_txt) + ".png"

    n = 1
    while os.path.isfile(base_dir+filename):
        filename = '{}'.format(category_txt) + "(" + str(n) + ").png"
        n = n + 1

    print("Saving ", filename)
    saved_files.append(filename)

    img.save(base_dir+filename)


def splitting_data(data):
    rem = len(data) % 10
    rem = data[-rem:]
    temp = []
    c = 0
    for i in range(10, len(data), 10):
        temp.append(data[c:i])
        c = c + 10

    temp.append(rem)
    return temp


def sort_by_votes(listele):

    # print(listele)

    temp = {}
    final_list = []
    c = 0
    for i in listele:
        print(i)
        temp[c] = i['Votes']
        c = c + 1

    print(temp)

    # temp = collections.OrderedDict(sorted(temp.items(), reverse=True))
    temp = collections.OrderedDict(sorted(temp.items(), reverse=True, key=lambda kv: (kv[1], kv[0])))

    print(temp)

    for i in list(temp.keys()):
        final_list.append(listele[i])

    print(final_list)

    return final_list


def download_file(file, filename):
    f = open(file, "rb")
    response = HttpResponse(FileWrapper(f), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    f.close()
    return response


def get_results(request):
    objects = add_c_model.objects.all()
    objects = list(objects.values())
    l1, l2, l3, l4, l5, l6, l7, l8 = [], [], [], [], [], [], [], []
    for i in objects:
        if i['Category'] == "President":
            l1.append(i)
        elif i['Category'] == "Vice President":
            l2.append(i)
        elif i['Category'] == "General Secretary":
            l3.append(i)
        elif i['Category'] == "Joint Secretary":
            l4.append(i)
        elif i['Category'] == "Treasurer":
            l5.append(i)
        elif i['Category'] == "E.C.Members":
            l6.append(i)
        elif i['Category'] == "E.C.Member(Women)":
            l7.append(i)
        elif i['Category'] == "Warden":
            l8.append(i)

    # create_img(l3)
    # create_img(sort_by_votes(l2))
    #
    #
    dataset = [sort_by_votes(l1), sort_by_votes(l2), sort_by_votes(l3), sort_by_votes(l4), sort_by_votes(l5),
               sort_by_votes(l6), sort_by_votes(l7), sort_by_votes(l8)]

    for i in dataset:
        if len(i) > 10:
            splitted = splitting_data(i)
            for splt in splitted:
                create_img(splt)
        else:
            create_img(i)

    print(saved_files)

    image1 = Image.open('project_files/output/' + saved_files[0]).convert('RGB')

    imagelist = []

    for i in saved_files[1:]:
        imagelist.append(Image.open('project_files/output/' + i).convert('RGB'))



    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    image1.save(BASE_DIR + r'\results\results.pdf', save_all=True, append_images=imagelist)


    return homepage_view(request)

    # response = download_file(file="project_files/result/results.pdf", filename="results.pdf")
    #
    # return response


