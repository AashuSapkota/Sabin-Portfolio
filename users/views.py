from django.shortcuts import render
from datetime import datetime
from rest_framework.views import APIView
from django.db import transaction
from django.contrib.auth.hashers import make_password

from .models import User, UserRoleModel, UserRolePrevilegeModel, MenuListModel
from .filters import UserRoleFilter, UserFilter
from . import serializers

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
import requests
import json

from .utils import checkUserPrevilege

from restaurant.settings import pagination_size

domainUrl = 'http://127.0.0.1:8088'


class UserLoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        user_email = request.data['user_email']
        password = request.data['password']
        token_url = domainUrl+'/api/token/'
        payload = {
            "user_email": user_email,
            "password": password
        }
        try:
            usr = User.objects.get(user_email = user_email)
            if usr:
                try:
                    response = requests.post(token_url, data=payload)
                    json_data = json.loads(response.text)
                    return Response(json_data, status=response.status_code)
                except Exception as e:
                    err = str(e)
                    return Response({"Error": err}, status=404)
            else:
                return Response({"Error": "User not found with given credentials"}, status=404)
        except User.DoesNotExist:
            return Response({"Error": "User not found with given credentials"}, status=404)



# classes handling CRUD for User Role Model
class CreateUserRoleAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'User Role', 'create_rights')
        if previlege == True:
            print('here')
            try:
                with transaction.atomic():
                    role_name = request.data['role_name']
                    role_description = request.data['role_description']
                    created_on = datetime.now()
                    created_by = request.user.pk
                    try:
                        existing_userrole = UserRoleModel.objects.get(
                            role_name=role_name)
                        if existing_userrole:
                            return Response({"Error": "UserRole with same name already exists"}, status=303)
                    except UserRoleModel.DoesNotExist:
                        user_role = UserRoleModel.objects.create(
                            role_name=role_name, role_description=role_description,
                            created_on=created_on, created_by=created_by
                        )
                        user_role.save()
                        return Response({"Success": "UserRole Created Succesfully"}, status=201)
            except Exception as e:
                err = str(e)
                return Response(err, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class ListUserRoleAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'User Role', 'retrieve_rights')
        if previlege == True:
            queryset = UserRoleModel.objects.filter(
                is_deleted=False).exclude(role_name='super admin')
            filtered_qs = UserRoleFilter(request.GET, queryset=queryset).qs
            paginator = PageNumberPagination()
            paginator.page_size = pagination_size
            result_page = paginator.paginate_queryset(filtered_qs, request)
            serializer = serializers.UserRoleSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class UpdateUserRoleAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'User Role', 'update_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                user_role = UserRoleModel.objects.get(pk=pk)
                serializer = serializers.UserRoleSerializer(user_role)
                return Response(serializer.data)
            except UserRoleModel.DoesNotExist:
                return Response({"Error": "User Role Doesn't Exisis"}, status=404)
            except:
                return Response({"Error": "Something Went Wrong"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)

    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'User Role', 'update_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                with transaction.atomic():
                    user_role = UserRoleModel.objects.get(pk=pk)
                    role_name = request.data['role_name']
                    role_description = request.data['role_description']
                    updated_on = datetime.now()
                    updated_by = request.user.pk
                    user_role.role_name = role_name
                    user_role.role_description = role_description
                    user_role.last_updated_on = updated_on
                    user_role.last_updated_by = updated_by
                    if user_role.role_name == 'super admin':
                        return Response({"Error": "Super Admin Role can't be Provided"}, status=303)
                    else:
                        user_role.save()
                    return Response({"Success": "UserRole Updated Succesfully"}, status=200)
            except Exception as e:
                error = str(e)
                return Response(error, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class DeleteUserRoleAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        print('here in delete')
        previlege = checkUserPrevilege(
            request.user.pk, 'User Role', 'delete_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                with transaction.atomic():
                    user_role = UserRoleModel.objects.get(pk=pk)
                    user_role.is_deleted = True
                    user_role.deleted_on = datetime.now()
                    user_role.save()
                    role_previliges = UserRolePrevilegeModel.objects.filter(
                        role_id=user_role.pk)
                    for role_previlege in role_previliges:
                        role_previlege.delete()
                    return Response({"Success": "UserRole Deleted Succesfully"}, status=200)
            except UserRoleModel.DoesNotExist:
                return Response({"Error": "UserRole Doesn't Exists"}, status=404)
            except Exception as e:
                print(e)
                return Response({"Error": "Something Went Wrong"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


# Classes handling CRUD for User Model

class UserCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'Users', 'create_rights')
        if previlege == True:
            try:
                with transaction.atomic():
                    user_email = request.data['user_email']
                    user_fullname = request.data['user_fullname']
                    password = request.data['password']
                    password = make_password(password)
                    user_role = request.data['user_role']
                    created_by = request.user.pk
                    try:
                        usr_email = User.objects.get(
                            user_email=user_email, is_deleted=False)
                        if usr_email:
                            return Response({'Error': 'User with same email already exists!!'}, status=303)

                    except User.DoesNotExist:
                        user = User.objects.create(user_email=user_email, user_fullname=user_fullname,
                                                    password=password, user_role=user_role,
                                                    created_by=created_by)
                        user.save()
                        return Response({'Success': 'User Created Succesfully'}, status=201)
            except Exception as e:
                error = str(e)
                return Response(error, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class UserListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'Users', 'retrieve_rights')
        if previlege == True:
            filtered_qs = UserFilter(request.GET, queryset=User.objects.filter(is_deleted=False)).qs
            paginator = PageNumberPagination()
            paginator.page_size = pagination_size
            # queryset = User.objects.filter(is_deleted=False)
            # result_page = paginator.paginate_queryset(queryset, request)
            result_page = paginator.paginate_queryset(filtered_qs, request)
            serializer = serializers.UserModelSerializer(
                result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class UserUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'Users', 'update_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                user = User.objects.get(pk=pk)
                serializer = serializers.UserModelSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"Error": "User Doesn't Exists"}, status=404)
            except:
                return Response({"Error": "Something Wens Wrong!"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)

    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'Users', 'update_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                user = User.objects.get(pk=pk)
                user_email = request.data['user_email']
                user_fullname = request.data['user_fullname']
                user_role = request.data['user_role']
                updated_on = datetime.now()
                updated_by = request.user.pk
                user.user_email = user_email
                user.user_fullname = user_fullname
                user.user_role = user_role
                user.last_updated_on = updated_on
                user.last_updated_by = updated_by
                try:
                    usr_email = User.objects.get(
                        user_email=user_email, is_deleted=False)
                    if usr_email.pk != pk:
                        return Response({'Error': 'User with same email already exists!!'}, status=303)
                    elif usr_email.pk == pk:
                        if user.user_role == '0':
                            user.save()
                            return Response({'Success': 'User Updated Succesfully'}, status=200)
                        elif user.user_role != '0':
                            prms = UserRolePrevilegeModel.objects.filter(
                                user_id=pk)
                            for prm in prms:
                                prm.delete()
                            user.save()
                            return Response({'Success': 'User Updated Succesfully'}, status=200)

                except User.DoesNotExist:
                    if user.user_role == '0':
                        user.save()
                        return Response({'Success': 'User Updated Succesfully'}, status=200)
                    elif user.user_role != '0':
                        prms = UserRolePrevilegeModel.objects.filter(
                            user_id=pk)
                        for prm in prms:
                            prm.delete()
                        user.save()
                        return Response({'Success': 'User Updated Succesfully'}, status=200)
            except Exception as e:
                error = str(e)
                return Response(error, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class UserDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'Users', 'delete_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                with transaction.atomic():
                    user = User.objects.get(pk=pk)
                    user.is_deleted = True
                    user.deleted_on = datetime.now()
                    user.deleted_by = request.user.pk
                    user.save()
                    user_previleges = UserRolePrevilegeModel.objects.filter(
                        user_id=user.pk)
                    for user_previlege in user_previleges:
                        user_previlege.delete()
                    return Response({"Success": "User Deleted Succesfully"}, status=200)
            except User.DoesNotExist:
                return Response({"Error": "User Doesn't Exists"}, status=404)
            except:
                return Response({"Error": "Something Went Wrong"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


# handling previleges for user and role permission
class UpdateRolePrevilageAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'User Role', 'update_rights')
        if previlege == True:
            role_id = kwargs['role_id']
            try:
                prms = UserRolePrevilegeModel.objects.filter(role_id=role_id)
                accesses = []
                menu_codes = []
                for previlege in prms:
                    print(previlege.menu_code)
                    menu_access = {
                        "menu_code": previlege.menu_code,
                        "create_rights": previlege.create_rights,
                        "retrieve_rights": previlege.retrieve_rights,
                        "update_rights": previlege.update_rights,
                        "delete_rights": previlege.delete_rights
                    }
                    accesses.append(menu_access)
                    menu_codes.append(previlege.menu_code)
                print(menu_codes)
                menus = MenuListModel.objects.filter(is_root=True)
                for menu in menus:
                    if menu.menu_name not in menu_codes:
                        # print(menu.menu_name)
                        menu_access = {
                            "menu_code": menu.menu_name,
                            "create_rights": False,
                            "retrieve_rights": False,
                            "update_rights": False,
                            "delete_rights": False
                        }
                        accesses.append(menu_access)
                # print(accesses)
                rsp = {"role_id": role_id, "Accesses": accesses}
                return Response(rsp, status=200)
            except UserRolePrevilegeModel.DoesNotExist:
                return Response({"Error": "Role Previlege Doesn't Exists!"}, status=303)
            except Exception as e:
                print(e)
                return Response({"Error": "Something Went Wrong"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=303)

    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'User Role Previlege', 'update_rights')
        if previlege == True:
            print('here')
            role_id = kwargs['role_id']
            try:
                prms = UserRolePrevilegeModel.objects.filter(role_id=role_id)
                with transaction.atomic():
                    if prms:
                        for p in prms:
                            p.delete()
                    role_id = role_id
                    user_id = '-1'
                    accesses = request.data['accesses']
                    for access in accesses:
                        menu_code = access['menu_code']
                        create_rights = access['create_rights']
                        delete_rights = access['delete_rights']
                        retrieve_rights = access['retrieve_rights']
                        update_rights = access['update_rights']
                        try:
                            role_previlege = UserRolePrevilegeModel.objects.get(
                                role_id=role_id, user_id=user_id, menu_code=menu_code)
                            if role_previlege:
                                return Response({"Error": "Role With Same Previlege Already Exists!"}, status=201)
                        except UserRolePrevilegeModel.DoesNotExist:
                            user_role_previlege = UserRolePrevilegeModel.objects.create(
                                role_id=role_id, user_id=user_id, menu_code=menu_code, create_rights=create_rights,
                                delete_rights=delete_rights, retrieve_rights=retrieve_rights, update_rights=update_rights
                            )
                            user_role_previlege.save()
                    return Response({"Success": "Role Previleges Updated Succesfully!!"}, status=200)
            except UserRolePrevilegeModel.DoesNotExist:
                return Response({"Error": "Role Previlege Doesn't Exists"}, status=303)
            except:
                e = str(e)
                return Response({"Error": "Something Went Wrong!", 'E': e}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class UpdateUserPrevilageAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'User Role', 'update_rights')
        if previlege == True:
            user_id = kwargs['user_id']
            try:
                prms = UserRolePrevilegeModel.objects.filter(user_id=user_id)
                accesses = []
                menu_codes = []
                if prms:
                    for previlege in prms:
                        menu_access = {
                            "menu_code": previlege.menu_code,
                            "create_rights": previlege.create_rights,
                            "retrieve_rights": previlege.retrieve_rights,
                            "update_rights": previlege.update_rights,
                            "delete_rights": previlege.delete_rights
                        }
                        accesses.append(menu_access)
                        menu_codes.append(previlege.menu_code)
                    menus = MenuListModel.objects.filter(is_root=True)
                    for menu in menus:
                        if menu.menu_name not in menu_codes:
                            menu_access = {
                                "menu_code": menu.menu_name,
                                "create_rights": False,
                                "retrieve_rights": False,
                                "update_rights": False,
                                "delete_rights": False
                            }
                            accesses.append(menu_access)
                else:
                    menus = MenuListModel.objects.filter(is_root=True)
                    for menu in menus:
                        if menu.menu_name not in menu_codes:
                            menu_access = {
                                "menu_code": menu.menu_name,
                                "create_rights": False,
                                "retrieve_rights": False,
                                "update_rights": False,
                                "delete_rights": False
                            }
                            accesses.append(menu_access)
                rsp = {"user_id": user_id, "Accesses": accesses}
                return Response(rsp, status=200)
            except UserRolePrevilegeModel.DoesNotExist:
                return Response({"Error": "User Previlege Doesn't Exists!"}, status=303)
            except Exception as e:
                print(e)
                return Response({"Error": "Something Went Wrong!!"})
        else:
            return Response({"Error": "Permission Denied"}, status=403)

    def post(self, request, *args, **kwargs):
        print('here in post')
        previlege = checkUserPrevilege(
            request.user.pk, 'User Role Previlege', 'update_rights')
        print(previlege)
        if previlege == True:
            user_id = kwargs['user_id']
            print(user_id)
            try:
                prms = UserRolePrevilegeModel.objects.filter(user_id=user_id)
                print('Prms: ', prms)
                with transaction.atomic():
                    if prms:
                        for p in prms:
                            p.delete()
                    user_id = user_id
                    role_id = '-1'
                    accesses = request.data['accesses']
                    for access in accesses:
                        menu_code = access['menu_code']
                        create_rights = access['create_rights']
                        delete_rights = access['delete_rights']
                        retrieve_rights = access['retrieve_rights']
                        update_rights = access['update_rights']
                        print(menu_code, create_rights, delete_rights,
                              retrieve_rights, update_rights)
                        try:
                            role_previlege = UserRolePrevilegeModel.objects.get(
                                role_id=role_id, user_id=user_id, menu_code=menu_code)
                            if role_previlege:
                                return Response({"Error": "User With Same Previlege Already Exists!"}, status=201)
                        except UserRolePrevilegeModel.DoesNotExist:
                            user_role_previlege = UserRolePrevilegeModel.objects.create(
                                role_id=role_id, user_id=user_id, menu_code=menu_code, create_rights=create_rights,
                                delete_rights=delete_rights, retrieve_rights=retrieve_rights, update_rights=update_rights
                            )
                            user_role_previlege.save()
                    return Response({"Success": "User Previleges Updated Succesfully!!"}, status=200)
            except UserRolePrevilegeModel.DoesNotExist:
                return Response({"Error": "User Previlege Doesn't Exists"}, status=303)
            except Exception as e:
                print(e)
                return Response({"Error": "Something Went Wrong!"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)