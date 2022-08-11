from django.shortcuts import render
from datetime import datetime
from rest_framework.views import APIView
from django.db import transaction

from .models import CostCenterModel, ItemCategoriesModel, ItemsModel, TableModel
from .import serializers

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from users.utils import checkUserPrevilege
from restaurant.settings import pagination_size

from .filters import CostCenterFilter, ItemCategoryFilter, ItemFilter, TableFilter
from users.models import UserRolePrevilegeModel

import base64
import io
from io import BytesIO
from PIL import Image
from django.core.files import File

# CRUD for CostCenter
class CreateCostCenterAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(request.user.pk, 'CostCenter', 'create_rights')
        if previlege == True:
            try:
                with transaction.atomic():
                    costcenter_name = request.data['costcenter_name']
                    costcenter_description = request.data['costcenter_description']
                    created_on = datetime.now()
                    created_by = request.user.pk
                    try:
                        existing_costcenter = CostCenterModel.objects.get(costcenter_name=costcenter_name)
                        if existing_costcenter:
                            return Response({"Error":"CostCenter with same name already exists!!"}, status=303)
                    except CostCenterModel.DoesNotExist:
                        costcenter = CostCenterModel.objects.create(
                                        costcenter_name = costcenter_name,
                                        costcenter_description = costcenter_description,
                                        created_on = created_on,
                                        created_by = created_by
                                        )
                        costcenter.save()
                        return Response({"Success":"CostCenter Created Succesfully!!"}, status=201)
            except Exception as e:
                print(e)
                return Response({"Error":"Something Went Wrong!!"})

        else:
            return Response({"Error":"Permission Denied"}, status=403)


class ListCostCenterAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'CostCenter', 'retrieve_rights')
        if previlege == True:
            queryset = CostCenterModel.objects.filter(is_deleted=False)
            filtered_qs = CostCenterFilter(request.GET, queryset=queryset).qs
            paginator = PageNumberPagination()
            paginator.page_size = pagination_size
            result_page = paginator.paginate_queryset(filtered_qs, request)
            serializer = serializers.CostCenterSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class UpdateCostCenterAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'CostCenter', 'update_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                user_role = CostCenterModel.objects.get(pk=pk)
                serializer = serializers.CostCenterSerializer(user_role)
                return Response(serializer.data)
            except CostCenterModel.DoesNotExist:
                return Response({"Error": "User Role Doesn't Exisis"}, status=404)
            except:
                return Response({"Error": "Something Went Wrong"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)

    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'CostCenter', 'update_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                with transaction.atomic():
                    costcenter = CostCenterModel.objects.get(pk=pk)
                    costcenter_name = request.data['costcenter_name']
                    costcenter_description = request.data['costcenter_description']
                    updated_on = datetime.now()
                    updated_by = request.user.pk
                    costcenter.costcenter_name = costcenter_name
                    costcenter.costcenter_description = costcenter_description
                    costcenter.last_updated_on = updated_on
                    costcenter.last_updated_by = updated_by
                    costcenter.save()
                    return Response({"Success": "CostCenter Updated Succesfully"}, status=200)
            except Exception as e:
                error = str(e)
                return Response(error, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class DeleteCostCenterAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'CostCenter', 'delete_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                with transaction.atomic():
                    costcenter = CostCenterModel.objects.get(pk=pk)
                    costcenter.is_deleted = True
                    costcenter.deleted_on = datetime.now()
                    costcenter.deleted_by = request.user.pk
                    costcenter.save()
                    return Response({"Success": "UserRole Deleted Succesfully"}, status=200)
            except CostCenterModel.DoesNotExist:
                return Response({"Error": "UserRole Doesn't Exists"}, status=404)
            except Exception as e:
                print(e)
                return Response({"Error": "Something Went Wrong"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


# CRUD for ItemCategory
class CreateItemCategoryAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(request.user.pk, 'ItemCategory', 'create_rights')
        if previlege == True:
            try:
                with transaction.atomic():
                    category_name = request.data['category_name']
                    category_description = request.data['category_description']
                    try:
                        base64_string = request.data['category_image']
                        imgdata = base64.b64decode(base64_string)
                        print('Imgdata: ', imgdata)
                        category_image = Image.open(io.BytesIO(imgdata))
                        print(category_image)
                        thumb_io = BytesIO()
                        category_image.save(thumb_io, format='JPEG')
                        category_thumb_file = File(thumb_io, name='item_category.jpg')
                    except Exception as e:
                        print('Exception: ', e)
                        category_thumb_file = None
                    created_on = datetime.now()
                    created_by = request.user.pk
                    try:
                        existing_category = ItemCategoriesModel.objects.get(category_name=category_name)
                        if existing_category:
                            return Response({"Error":"ItemCategory with same name already exists!!"}, status=303)
                    except ItemCategoriesModel.DoesNotExist:
                        itemcategory = ItemCategoriesModel.objects.create(
                                        category_name = category_name,
                                        category_description = category_description,
                                        category_image = category_thumb_file,
                                        created_on = created_on,
                                        created_by = created_by
                                        )
                        itemcategory.save()
                        return Response({"Success":"ItemCategory Created Succesfully!!"}, status=201)
            except Exception as e:
                print(e)
                return Response({"Error":"Something Went Wrong!!"})

        else:
            return Response({"Error":"Permission Denied"}, status=403)


class ListItemCategoryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'ItemCategory', 'retrieve_rights')
        if previlege == True:
            queryset = ItemCategoriesModel.objects.filter(is_deleted=False)
            filtered_qs = ItemCategoryFilter(request.GET, queryset=queryset).qs
            paginator = PageNumberPagination()
            paginator.page_size = pagination_size
            result_page = paginator.paginate_queryset(filtered_qs, request)
            serializer = serializers.ItemCategorySerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class UpdateItemCategoryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'ItemCategory', 'update_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                item_category = ItemCategoriesModel.objects.get(pk=pk)
                serializer = serializers.ItemCategorySerializer(item_category)
                return Response(serializer.data)
            except CostCenterModel.DoesNotExist:
                return Response({"Error": "User Role Doesn't Exisis"}, status=404)
            except:
                return Response({"Error": "Something Went Wrong"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)

    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'ItemCategory', 'update_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                with transaction.atomic():
                    itemcategory = ItemCategoriesModel.objects.get(pk=pk)
                    category_name = request.data['category_name']
                    category_description = request.data['category_description']
                    try:
                        base64_string = request.data['category_image']
                        imgdata = base64.b64decode(base64_string)
                        category_image = Image.open(io.BytesIO(imgdata))
                        thumb_io = BytesIO()
                        category_image.save(thumb_io, format='JPEG')
                        category_thumb_file = File(thumb_io, name='item_category.jpg')
                    except Exception as e:
                        print('Exception: ', e)
                        category_thumb_file = None
                    category_image = category_thumb_file
                    updated_on = datetime.now()
                    updated_by = request.user.pk
                    itemcategory.category_name = category_name
                    itemcategory.category_description = category_description
                    itemcategory.category_image = category_image
                    itemcategory.last_updated_on = updated_on
                    itemcategory.last_updated_by = updated_by
                    itemcategory.save()
                    return Response({"Success": "ItemCategory Updated Succesfully"}, status=200)
            except Exception as e:
                error = str(e)
                return Response(error, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class DeleteItemCategoryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'ItemCategory', 'delete_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                with transaction.atomic():
                    itemcategory = ItemCategoriesModel.objects.get(pk=pk)
                    itemcategory.is_deleted = True
                    itemcategory.deleted_on = datetime.now()
                    itemcategory.deleted_by = request.user.pk
                    itemcategory.save()
                    return Response({"Success": "ItemCategory Deleted Succesfully"}, status=200)
            except CostCenterModel.DoesNotExist:
                return Response({"Error": "ItemCategory Doesn't Exists"}, status=404)
            except Exception as e:
                return Response({"Error": "Something Went Wrong"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


# CRUD for Items
class CreateItemAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(request.user.pk, 'Items', 'create_rights')
        if previlege == True:
            try:
                with transaction.atomic():
                    item_name = request.data['item_name']
                    item_description = request.data['item_description']
                    item_category = request.data['item_category']
                    item_rate = request.data['item_rate']
                    try:
                        base64_string = request.data['item_image']
                        imgdata = base64.b64decode(base64_string)
                        item_image = Image.open(io.BytesIO(imgdata))
                        thumb_io = BytesIO()
                        item_image.save(thumb_io, format='JPEG')
                        item_thumb_file = File(thumb_io, name='items.jpg')
                    except Exception as e:
                        item_thumb_file = None
                    created_on = datetime.now()
                    created_by = request.user.pk
                    try:
                        existing_item = ItemsModel.objects.get(item_name=item_name)
                        if existing_item:
                            return Response({"Error":"Item with same name already exists!!"}, status=303)
                    except ItemsModel.DoesNotExist:
                        item = ItemsModel.objects.create(
                                        item_name = item_name,
                                        item_description = item_description,
                                        item_category = item_category,
                                        item_rate = item_rate,
                                        item_image = item_thumb_file,
                                        created_on = created_on,
                                        created_by = created_by
                                        )
                        item.save()
                        return Response({"Success":"Item Created Succesfully!!"}, status=201)
            except Exception as e:
                print(e)
                return Response({"Error":"Something Went Wrong!!"})

        else:
            return Response({"Error":"Permission Denied"}, status=403)


class ListItemAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'Items', 'retrieve_rights')
        if previlege == True:
            queryset = ItemsModel.objects.filter(is_deleted=False)
            filtered_qs = ItemFilter(request.GET, queryset=queryset).qs
            paginator = PageNumberPagination()
            paginator.page_size = pagination_size
            result_page = paginator.paginate_queryset(filtered_qs, request)
            serializer = serializers.ItemsSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class UpdateItemAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'Items', 'update_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                items = ItemsModel.objects.get(pk=pk)
                serializer = serializers.ItemsSerializer(items)
                return Response(serializer.data)
            except CostCenterModel.DoesNotExist:
                return Response({"Error": "Items Doesn't Exisis"}, status=404)
            except:
                return Response({"Error": "Something Went Wrong"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)

    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'Items', 'update_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                with transaction.atomic():
                    item = ItemsModel.objects.get(pk=pk)
                    item_name = request.data['item_name']
                    item_description = request.data['item_description']
                    item_category = request.data['item_category']
                    item_rate = request.data['item_rate']
                    try:
                        base64_string = request.data['item_image']
                        imgdata = base64.b64decode(base64_string)
                        item_image = Image.open(io.BytesIO(imgdata))
                        thumb_io = BytesIO()
                        item_image.save(thumb_io, format='JPEG')
                        item_thumb_file = File(thumb_io, name='item.jpg')
                    except Exception as e:
                        print('Exception: ', e)
                        item_thumb_file = None
                    updated_on = datetime.now()
                    updated_by = request.user.pk
                    item.item_name = item_name
                    item.item_description = item_description
                    item.item_category = item_category
                    item.item_rate = item_rate
                    item.item_image = item_thumb_file
                    item.last_updated_on = updated_on
                    item.last_updated_by = updated_by
                    item.save()
                    return Response({"Success": "Item Updated Succesfully"}, status=200)
            except Exception as e:
                error = str(e)
                return Response(error, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class DeleteItemAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'Items', 'delete_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                with transaction.atomic():
                    item = ItemsModel.objects.get(pk=pk)
                    item.is_deleted = True
                    item.deleted_on = datetime.now()
                    item.deleted_by = request.user.pk
                    item.save()
                    return Response({"Success": "Item Deleted Succesfully"}, status=200)
            except CostCenterModel.DoesNotExist:
                return Response({"Error": "Item Doesn't Exists"}, status=404)
            except Exception as e:
                return Response({"Error": "Something Went Wrong"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


# CRUD for Tables
class CreatetableAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(request.user.pk, 'Table', 'create_rights')
        if previlege == True:
            try:
                with transaction.atomic():
                    table_name = request.data['table_name']
                    table_code = request.data['table_code']
                    try:
                        existing_table = TableModel.objects.get(table_name=table_name)
                        if existing_table:
                            return Response({"Error":"Table with same name already exists!!"}, status=303)
                    except TableModel.DoesNotExist:
                        table = TableModel.objects.create(
                                        table_name = table_name,
                                        table_code = table_code,
                                        created_by = request.user.pk
                                        )
                        table.save()
                        return Response({"Success":"Table Created Succesfully!!"}, status=201)
            except Exception as e:
                print(e)
                return Response({"Error":"Something Went Wrong!!"})

        else:
            return Response({"Error":"Permission Denied"}, status=403)


class ListTableAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'Table', 'retrieve_rights')
        if previlege == True:
            queryset = TableModel.objects.filter(is_deleted=False)
            filtered_qs = TableFilter(request.GET, queryset=queryset).qs
            paginator = PageNumberPagination()
            paginator.page_size = pagination_size
            result_page = paginator.paginate_queryset(filtered_qs, request)
            serializer = serializers.TableSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class UpdateTableAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'Table', 'update_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                table = TableModel.objects.get(pk=pk)
                serializer = serializers.TableSerializer(table)
                return Response(serializer.data)
            except CostCenterModel.DoesNotExist:
                return Response({"Error": "Table Doesn't Exisis"}, status=404)
            except:
                return Response({"Error": "Something Went Wrong"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)

    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'table', 'update_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                with transaction.atomic():
                    table = TableModel.objects.get(pk=pk)
                    table_name = request.data['table_name']
                    table_code = request.data['table_code']
                    updated_on = datetime.now()
                    updated_by = request.user.pk
                    table.table_name = table_name
                    table.table_code = table_code
                    table.last_updated_on = updated_on
                    table.last_updated_by = updated_by
                    table.save()
                    return Response({"Success": "Table Updated Succesfully"}, status=200)
            except Exception as e:
                error = str(e)
                return Response(error, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)


class DeleteTableAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(
            request.user.pk, 'Table', 'delete_rights')
        if previlege == True:
            pk = kwargs['pk']
            try:
                with transaction.atomic():
                    table = TableModel.objects.get(pk=pk)
                    table.is_deleted = True
                    table.deleted_on = datetime.now()
                    table.deleted_by = request.user.pk
                    table.save()
                    return Response({"Success": "Table Deleted Succesfully"}, status=200)
            except CostCenterModel.DoesNotExist:
                return Response({"Error": "Table Doesn't Exists"}, status=404)
            except Exception as e:
                return Response({"Error": "Something Went Wrong"}, status=303)
        else:
            return Response({"Error": "Permission Denied"}, status=403)




