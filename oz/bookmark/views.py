from django.shortcuts import render, get_object_or_404
from bookmark.models import Bookmark
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, get_object_or_404


def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(id__gte=50)
    context = {
        'bookmarks': bookmarks
    }
    return render(request, 'bookmark_list.html', context)

def bookmark_detail(request, id):
    bookmark = get_object_or_404(Bookmark, id=id)

    context = {'bookmark' : bookmark}
    return render(request, 'bookmark_detail.html', context)

