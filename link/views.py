from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from .models import MyUrl

import json

from .forms import UrlForm


def base62(number):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    while number > 0:
        yield alphabet[number % 62]
        number /= 62


def id_to_short_url(ID):
    return ''.join(reversed(list(base62(ID))))


def index(request):
    form = UrlForm()
    return render(request, 'link/main.html', {'form': form})


def open(request, query):
    try:
        path = MyUrl.objects.get(short_link=query)
    except MyUrl.DoesNotExist:
        raise Http404
    return HttpResponseRedirect(path.link_to)


def serve(request):
    # d = json.loads(request.body)
    # url = d.get("url", None)

    form = UrlForm(request.POST)

    if not form.is_valid():
        resp = HttpResponse(
            json.dumps({"message": "Invalid url"}),
            content_type="application/json", status=400)
        # resp.status_code = 400
        return resp

    url = form.cleaned_data['url']
    short_url = form.cleaned_data.get('short_url', None)
    if short_url:
        url_obj = MyUrl.objects.filter(short_link=short_url)
        if url_obj.exists():
            resp = HttpResponse(
                json.dumps({"message": "Such url already exists!"}),
                content_type="application/json", status=400)
            # resp.status_code = 400
            return resp
        new_url = MyUrl(link_to=url, short_link=short_url)
        new_url.save()
        short_link = request.build_absolute_uri(short_url)
        return HttpResponse(
            json.dumps({'url': short_link}),
            content_type="application/json")

    url_obj = MyUrl.objects.filter(link_to=url)

    if url_obj.exists():
        short_link = request.build_absolute_uri(url_obj.first().short_link)
    else:
        new_url = MyUrl(link_to=url)
        new_url.save()
        base62id = id_to_short_url(new_url.id)
        new_url.short_link = base62id
        new_url.save()
        short_link = request.build_absolute_uri(base62id)
    return HttpResponse(
        json.dumps({'url': short_link}),
        content_type="application/json")


def get_uri(request):
    return HttpResponse(json.dumps({'uri': request.META['HTTP_HOST']}),
                        content_type="application/json")


def make(request):
    long_url_form = UrlForm(request.POST['long_url'])

    if not long_url_form.is_valid():
        resp = HttpResponse(
            json.dumps({"message": "Invalid url"}),
            content_type="application/json", status=400)
        # resp.status_code = 400
        return resp

    url_obj = MyUrl.objects.filter(link_to=request.POST['short_url'])

    if url_obj.exists():
        resp = HttpResponse(
            json.dumps({"message": "Such url already exists!"}),
            content_type="application/json", status=400)
        # resp.status_code = 400
        return resp

    new_url = MyUrl(link_to=request.POST['long_url'])
    new_url.short_link = request.POST['short_url']
    new_url.save()
    return HttpResponse(
        json.dumps({'url': request.POST['short_url']}),
        content_type="application/json")
