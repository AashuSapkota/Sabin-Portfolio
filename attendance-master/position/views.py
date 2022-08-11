from django.shortcuts import render, redirect
from .models import PositionListModel
from django.views import View
from django.http import HttpResponse
from django.db import transaction


def PositionListView(request):
    context = {}
    positions = PositionListModel.objects.all()
    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        position = positions.get(id=ID)
        context['position'] = position
    template_name = 'position/position_list_view.html'
    context['positions'] = positions
    return render(request, template_name, context)


class PositionCreateView(View):
    template_name = 'position/position_create_view.html'
    context_object_name = 'position'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            position_name = request.POST['position_name']
            position_description = request.POST['position_description']
            if not PositionListModel.objects.filter(position_name=position_name).exists():
                position = PositionListModel(position_name=position_name, position_description=position_description)
                position.save()
                return redirect('position:position_list')
            else:
                return HttpResponse('Position Already Exists!!')


class PositionUpdateView(View):
    template_name = 'position/position_update_view.html'
    context_object_name = 'position'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        if PositionListModel.objects.filter(pk=pk).exists():
            position = PositionListModel.objects.get(pk=pk)
            return render(request, self.template_name, {'position':position})
        return redirect('position:position_list')
    
    def post(self, request, *args, **kwargs):
        pk=kwargs['pk']
        with transaction.atomic():
            position_name = request.POST['position_name']
            position_description = request.POST['position_description']
            if PositionListModel.objects.filter(pk=pk).exists():
                position = PositionListModel.objects.get(pk=pk)
                position.position_name = position_name
                position.position_description = position_description
                position.save()
                return redirect('position:position_list')
            return HttpResponse('Error:Position does not exists!!')


def PositionDeleteView(request, pk):
    position = PositionListModel.objects.get(id=pk)
    position.delete()
    return redirect('position:position_list')