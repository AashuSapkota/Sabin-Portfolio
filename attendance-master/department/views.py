from django import views
from django.shortcuts import redirect, render
from .models import DepartmentListModel
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.http import HttpResponse
from django.db import transaction


def DepartmentListView(request):
    context = {}
    departments = DepartmentListModel.objects.all()
    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        department = departments.get(id=ID)
        context['department'] = department
    template_name = 'department/department_list_view.html'
    context['departments'] = departments
    return render(request, template_name, context)


class DepartmentCreateView(View):
    template_name = 'department/department_create_view.html'
    context_object_name = 'department'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            department_name = request.POST['department_name']
            department_code = request.POST['department_code']
            department_description = request.POST['department_description']
            if not DepartmentListModel.objects.filter(department_name=department_name, department_code=department_code).exists():
                department = DepartmentListModel(
                    department_name=department_name,
                    department_code=department_code,
                    department_description=department_description)
                department.save()
                return redirect('department:department_list')
            else:
                return HttpResponse("Department Already Exists!")


class DepartmentUpdateView(View):
    template_name = 'department/department_update_view.html'
    context_object_name = 'department'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        if DepartmentListModel.objects.filter(pk=pk).exists():
            department = DepartmentListModel.objects.get(pk=pk)
            return render(request, self.template_name, {'department': department})
        return redirect('department:department_list')
    
    def post(self, request, *args, **kwargs):
        pk=kwargs['pk']
        with transaction.atomic():
            department_name = request.POST['department_name']
            department_code = request.POST['department_code']
            department_description = request.POST['department_description']
            if DepartmentListModel.objects.filter(pk=pk).exists():
                department = DepartmentListModel.objects.get(pk=pk)
                department.department_name = department_name
                department.department_code = department_code
                department.department_description = department_description
                department.save()
                return redirect('department:department_list')
            return HttpResponse('Error:Department does not exists!!')
        


def DepartmentDeleteView(request, pk):
    department = DepartmentListModel.objects.get(id=pk)
    department.delete()
    return redirect('department:department_list')