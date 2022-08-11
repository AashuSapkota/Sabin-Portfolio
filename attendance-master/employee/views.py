from datetime import datetime
from django.db.models import base
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.contrib import messages
import cv2
import base64
import io
import numpy as np
from PIL import Image
from io import BytesIO
from django.core.files import File
import _pickle as pkl
import json
import face_recognition as fr

from department.models import DepartmentListModel
from employee.models import EmployeeListModel
from level.models import LevelListModel
from position.models import PositionListModel
from .models import EmployeeLogmodel


def EmployeeListView(request):
    context = {}
    employees = EmployeeListModel.objects.all()
    if request.method == 'POST' and request.is_ajax:
        ID = request.POST.get('id')
        employee = employees.get(id=ID)
        context['employee'] = employee
    template_name = 'employee/employee_list_view.html'
    context['employees'] = employees
    return render(request, template_name, context)


class EmployeeRegisterView(View):
    template_name = 'employee/employee_register_view.html'
    context_object_name = 'employee'

    def get(self, request, *args, **kwargs):
        departments = DepartmentListModel.objects.all()
        positions = PositionListModel.objects.all()
        levels = LevelListModel.objects.all()
        context = {'departments': departments,
                   'positions': positions, 'levels': levels}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                emp_firstname = request.POST['emp_firstname']
                emp_middlename = request.POST['emp_middlename']
                emp_lastname = request.POST['emp_lastname']
                emp_gander = request.POST['emp_gender']
                emp_DOB = request.POST['emp_DOB']
                emp_contact_number = request.POST['emp_contact_number']
                emp_mail = request.POST['emp_mail']
                emp_address = request.POST['emp_address']
                emp_department_id = request.POST['emp_department']
                emp_position_id = request.POST['emp_position']
                emp_level_id = request.POST['emp_level']
                emp_joining_date = request.POST['emp_joining_date']
                emp_img_object = request.FILES['emp_image']
                emp_img = Image.open(emp_img_object)
                thumb_io = BytesIO()
                emp_img.save(thumb_io, format='JPEG')
                thumb_io.seek(0)
                emp_img = thumb_io.read()
                img_data = BytesIO(emp_img)
                Image.open(img_data)
                thumb_file = File(thumb_io, name='emp.jpg')
                print("Image Data:", img_data)
                try:
                    emp_document = request.FILES['emp_document']
                except:
                    emp_document = None

                # base64_string = request.FILES['emp_image']
                # imgdata = base64.b64decode(base64_string)
                # emp_image = Image.open(io.BytesIO(imgdata))
                # thumb_io = BytesIO()
                # emp_image.save(thumb_io, format='JPEG')
                # thumb_file = File(thumb_io, name='emp.jpg')
                department = DepartmentListModel.objects.get(
                    pk=emp_department_id)
                position = PositionListModel.objects.get(pk=emp_position_id)
                level = LevelListModel.objects.get(pk=emp_level_id)
                employee = EmployeeListModel.objects.create(
                    emp_firstname=emp_firstname,
                    emp_middlename=emp_middlename,
                    emp_lastname=emp_lastname,
                    emp_gender=emp_gander,
                    emp_DOB=emp_DOB,
                    emp_contact_number=emp_contact_number,
                    emp_mail=emp_mail,
                    emp_address=emp_address,
                    emp_department=department,
                    emp_position=position,
                    emp_level=level,
                    emp_joining_date=emp_joining_date,
                    emp_image=thumb_file,
                    emp_document=emp_document
                )
                employee.save()
        except Exception as e:
            messages.warning(request, "Something went wrong.")
            print(e)
        return redirect("employee:employee_list")


class VerifyImage:
    def __init__(self, image):
        self.captured_image = image

    def verify(self):
        profiles = EmployeeListModel.objects.all()
        known_faces = [json.loads(pkl.loads(i.emp_image_binary))[
            'encoded_emp_image'] for i in EmployeeListModel.objects.all()]
        captured_image_read = self.captured_image
        captured_image_encoding = fr.face_encodings(captured_image_read)
        if len(captured_image_encoding) > 0:
            result = fr.compare_faces(
                known_faces, captured_image_encoding[0], tolerance=0.5)
            return result
        else:
            return [False]


class EmployeeCameraView(View):
    template_name = 'employee/employee_camera_view.html'

    def get(self, request, *arags, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        base64_string = request.POST['mydata']
        imgdata = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(imgdata))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

        obj = VerifyImage(image)
        status = obj.verify()
        indices = [i for i, x in enumerate(status) if x]
        profiles = EmployeeListModel.objects.all()
        data = []
        for i in indices:
            profile = {'emp_firstname': profiles[i].emp_firstname,
                       'emp_middlename': profiles[i].emp_middlename,
                       'emp_lastname': profiles[i].emp_lastname,
                       'emp_image_url': profiles[i].emp_image.url,
                       'index': profiles[i].pk,
                       }
            data.append(profile)
        return JsonResponse({'data': data})


class EmployeeDetailView(DetailView):
    model = EmployeeListModel
    template_name = 'employee/employee_detail_view.html'


def EmployeeDeleteView(request, pk):
    employee = EmployeeListModel.objects.get(id=pk)
    employee.delete()
    return redirect('employee:employee_list')


def FetchProfile(request):
    print("Inside fetch profile")
    id = request.POST['id'].split('-')
    pk = id[1]
    print("Printing pk:", pk)
    if pk != 'unknown':
        if EmployeeListModel.objects.filter(pk=pk).exists():
            employee = EmployeeListModel.objects.get(pk=pk)
            data = {
                'status': 'found',
                'emp_id': employee.pk,
                'emp_firstname': employee.emp_firstname,
                'emp_lastname': employee.emp_lastname,
            }
        else:
            data = {'status': 'notfound'}
    else:
        data = {'status': 'notfound'}
    return JsonResponse(data)


class EmployeeIdentificationView(View):
    template_name = 'employee/employee_identification.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax and self.request.method == 'POST':
            print("Inside Post View")
            emp_id = request.POST['emp_id']
            log_type = request.POST['log_type']
            employee = EmployeeListModel.objects.get(pk=emp_id)
            print('employee: ',employee)

            if not EmployeeLogmodel.objects.filter(emp_name=emp_id).exists():
                if log_type == 'I':
                    print("Log doesn't exists")
                    print("Log Type is I")
                    print('before log saved')
                    log = EmployeeLogmodel.objects.create(
                        emp_name=employee, log_type=log_type, check_in_datetime=datetime.now())
                    log.save()
                    print('after log saved')
                    print("Log Type:", log_type)
                    print("Emp ID:", emp_id)
                    return HttpResponse('Checked In succesfully!!')
                
                if log_type == 'O':
                    log = EmployeeLogmodel.objects.create(
                        emp_name=employee, log_type=log_type, check_out_datetime=datetime.now())
                    log.save()
                    return HttpResponse('Checked Out succesfully!!')

            if EmployeeLogmodel.objects.filter(emp_name=employee):
                employee = EmployeeLogmodel.objects.filter(emp_name=employee)
                old_data=[]
                new_data=[]
                for emp in employee:
                    if emp.check_in_datetime != None and emp.check_out_datetime != None:
                        old_data.append(emp)
                    else:
                        new_data.append(emp)

                print('old_data: ', old_data)
                print('new_data: ', new_data)
                print('length: ',len(new_data))
                if len(new_data) == 0:
                    if log_type == 'I':
                        print('New Entry')
                        employee = EmployeeListModel.objects.get(pk=emp_id)
                        log = EmployeeLogmodel.objects.create(
                            emp_name=employee, log_type=log_type, check_in_datetime=datetime.now())
                        log.save()
                        print('saved')
                        try:
                            print('return')
                            return JsonResponse('Checked In succesfully!!')
                        except Exception as e:
                            print('Exception: ', e)
                if len(new_data) > 0:
                    for emp in new_data:
                        in_date = emp.check_in_datetime.strftime('%D')
                        out_date = emp.check_out_datetime

                        print('in date:', in_date)
                        print("Out Date:", out_date)
                        print('log_type:', log_type)
                        today = datetime.today().strftime('%D')
                        if in_date == today and out_date == None and log_type == 'O':
                            print("Today")
                            emp.check_out_datetime = datetime.now()
                            emp.save()
                        return HttpResponse('Checked Out succesfully!!')

def EmployeeLogEntryView(request):
    if request.method == 'POST':
        emp_id = request.POST['emp_id'],
        emp_name = request.POST['emp_name']
        log_type = request.POST['log_type']
        print("EmpID:", emp_id)
        print("EmpName:", emp_name)
        print("LogTYpe:", log_type)
