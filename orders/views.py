from django.shortcuts import render
from datetime import datetime
from rest_framework.views import APIView
from django.db import transaction

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import OrderModel, OrderDetailModel

from users.utils import checkUserPrevilege

from .import serializers
from costcenter.models import ItemsModel, TableModel


class CreateTableOrderAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        previlege = checkUserPrevilege(request.user.pk, 'Orders', 'create_rights')
        if previlege == True:
            try:
                with transaction.atomic():
                    table_id = request.data['table_id']
                    item_id = request.data['item_id']
                    item_quantity = request.data['item_quantity']
                    try:
                        table = TableModel.objects.get(pk=table_id)
                        if table.is_occupied == False:
                            latest_ordermaster_id = OrderModel.objects.filter(table_id=table_id).last()
                            print('latest_ordermaster_id: ', latest_ordermaster_id)
                            if latest_ordermaster_id is None:
                                latest_ordermaster_id = 1
                                print('latest_ordermaster_id: ', latest_ordermaster_id)
                            else:
                                latest_ordermaster_id = latest_ordermaster_id.order_masterid + 1
                                print('latest_ordermaster_id: ', latest_ordermaster_id)
                            order = OrderModel.objects.create(table_id=table_id, order_masterid=latest_ordermaster_id)
                            order.save()
                            updated_ordermaster_id = order.order_masterid
                            item_rate = ItemsModel.objects.get(pk=item_id).item_rate
                            total_price = int(item_rate) * int(item_quantity)
                            order_detail = OrderDetailModel.objects.create(
                                            order_masterid=updated_ordermaster_id,
                                            item_id = item_id,
                                            item_quantity = item_quantity,
                                            item_rate = item_rate,
                                            total_price = total_price
                                            )
                            order_detail.save()
                            table.is_occupied=True
                            table.save()
                            return Response({"Success":"Order Saved Succesfully"}, status=201)
                        elif table.is_occupied == True:
                            latest_ordermaster_id = OrderModel.objects.filter(table_id=table_id).last()
                            print(latest_ordermaster_id)
                            pass
                    except TableModel.DoesNotExist:
                        return Response({"Error":"Table Doesn't Exists!!"}, status=303)
            except Exception as e:
                print(e)
        else:
            return Response({"Error":"Permission Denied"}, status=403)