from app1.models import datastore


def access_main_model(request):
    complete = datastore.objects.all()
    complete = list(complete.values())

    for i in complete:
        i.pop('id')

    context = {'complete': complete}
    return context
