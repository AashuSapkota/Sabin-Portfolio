from django.shortcuts import redirect, render
from .models import LevelListModel
from django.views import View
from django.http import HttpResponse
from django.db import transaction


def LevelListView(request):
    context = {}
    levels = LevelListModel.objects.all()
    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        level = levels.get(id=ID)
        context['level'] = level
    template_name = 'level/level_list_view.html'
    context['levels'] = levels
    return render(request, template_name, context)


class LevelCreateView(View):
    template_name = 'level/level_create_view.html'
    context_object_name = 'level'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            level_name = request.POST['level_name']
            level_description = request.POST['level_description']
            if not LevelListModel.objects.filter(level_name=level_name).exists():
                 level = LevelListModel(level_name=level_name, level_description=level_description)
                 level.save()
                 return redirect('level:level_list')
            else:
                return HttpResponse('Level Already Exists!!')


class LevelUpdateView(View):
    template_name = 'level/level_update_view.html'
    context_object_name = 'level'

    def get(self, request, *args, **kwargs):
        pk=kwargs['pk']
        if LevelListModel.objects.filter(pk=pk).exists():
            level = LevelListModel.objects.get(pk=pk)
            return render(request, self.template_name, {'level':level})
        return redirect('level:level_list')
    
    def post(self, request, *args, **kwargs):
        pk=kwargs['pk']
        with transaction.atomic():
            level_name = request.POST['level_name']
            level_description = request.POST['level_description']
            if LevelListModel.objects.filter(pk=pk).exists():
                level = LevelListModel.objects.get(pk=pk)
                level.level_name = level_name
                level.level_description = level_description
                level.save()
                return redirect('level:level_list')
            return HttpResponse('Error:Level does not exists!!')


def LevelDeleteView(request, pk):
    level = LevelListModel.objects.get(id=pk)
    level.delete()
    return redirect('level:level_list')