from django.shortcuts import render
from .models import project
from app1.models import datastore


import numpy as np


# Create your views here.

def find_invalid_votes(voted, cats, threshold):

    count_m = []

    for i in voted:
        i = i.split("$")
        count_m.append(i[0])

    count_l = []

    for j in cats:
        count_l.append(count_m.count(j))

    print(count_l)
    print(threshold)

    remove_list = []

    for i in range(len(count_l)):
        if count_l[i] != threshold[i]:
            remove_list.append(i)

    remove_list_main = []

    for i in remove_list:
        remove_list_main.append(cats[i])

    print(voted)

    temperory = tuple(voted)

    temperory = list(temperory)

    t = -1
    for i in enumerate(voted):
        variable = i[1].split("$")

        t = t + 1

        if variable[0] in remove_list_main:
            print(i[0])
            temperory.pop(i[0] - t)

    print(temperory)

    return temperory


def winner(request):
    complete = project.objects.all()
    maindata = datastore.objects.all()
    maindata = list(maindata.values())
    cats = []
    thres = []
    cands = []
    for i in maindata:
        cats.append(i['Categories'])
        thres.append(i['Threshold'])
        cands.append(i['Candidates'].split(','))

    results = np.zeros(np.shape(cands), dtype=int)

    complete = list(complete.values())

    for data in complete:
        voted = data['Data'].split(',')

        voted = find_invalid_votes(voted, cats, thres)

        for i in voted:
            variable = i.split("$")

            curr_ind_1 = cats.index(variable[0])
            curr_ind_2 = cands[curr_ind_1].index(variable[1])

            results[curr_ind_1][curr_ind_2] = results[curr_ind_1][curr_ind_2] + 1
        print()
    election_results = {}

    for i in cats:
        election_results[i] = {}

    c = 0
    for i in range(len(cands)):
        for j in range(len(cands[0])):
            election_results[cats[c]][cands[i][j]] = results[i][j]
        c = c + 1

    for i in election_results.keys():
        election_results[i] = dict(sorted(election_results[i].items(), key=lambda item: item[1], reverse=True))

    context = {
        "result": election_results
    }

    return render(request, 'index.html', context)

