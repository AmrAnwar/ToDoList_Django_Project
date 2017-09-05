from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages

from ..models import List, Task, Sublist


def remove_redirect(request, key=None, pk=None):
    message = "you don't have permission"
    if key == 'list':
        my_object = get_object_or_404(List, pk=pk)
        reverse_str = reverse("lists-list")
        if my_object.user == request.user:
            message = "List was deleted"
            my_object.delete()
    elif key == 'task':
        my_object = get_object_or_404(Task, pk=pk)
        reverse_str = reverse("lists-detail", kwargs={"pk": my_object.list.pk})
        if request.user == my_object.user or request.user == my_object.list.user:
            message = "Task was deleted"
            my_object.delete()
    elif key == 'sublist':
        my_object = get_object_or_404(Sublist, pk=pk)
        reverse_str = reverse("tasks-detail", kwargs={"pk": my_object.task.pk})
        if request.user == my_object.task.user or my_object.task.list.user:
            message = "Sublist was deleted"
            my_object.delete()
    else:
        raise Http404
    messages.success(request, message)
    return HttpResponseRedirect(reverse_str)