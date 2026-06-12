from django.shortcuts import render
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_datatables_editor.viewsets import DatatablesEditorModelViewSet

from . import models
from . import serializers

class MtlItemViewset(DatatablesEditorModelViewSet):
    queryset = models.MtlItem.objects.all()
    serializer_class = serializers.MtlItemSerializer
    permission_classes = [IsAuthenticated, ]

# html restapi html als beispiel
def client(request):
    return render(request, "restapi2.html")


@api_view(['GET', 'POST'])
def api_list_mtl_items(request):
    if request.method == "GET":
        mtl_items = models.MtlItem.objects.all()
        serializer = serializers.MtlItemRestSerializer(mtl_items, many=True)

        return Response(serializer.data)
    else:  # Post
        serializer = serializers.MtlItemRestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # Successful post
        return Response(serializer.errors, status=400)  # Invalid data


@api_view(['GET', 'DELETE', 'PUT'])
def api_mtl_item_details(request, itp_no_mag):
    try:
        mtl_item = models.MtlItem.objects.get(itp_no_mag = itp_no_mag)
    except:
        return Response(status=404)

    if request.method == 'GET':
        serializer = serializers.MtlItemRestSerializer(mtl_item)
        return Response(serializer.data)
    elif request.method == 'PUT':  # Update
        serializer = serializers.MtlItemRestSerializer(mtl_item, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Update table in DB
            return Response(serializer.data)

        return Response(serializer.errors, status=400)  # Bad request
    elif request.method == 'DELETE':
        mtl_item.delete()
        return Response(status=204)


# Hyperlinked serializer
class HyperMtlItemViewSet(viewsets.ModelViewSet):
    queryset = models.MtlItem.objects.all().order_by('itp_no_mag')
    serializer_class = serializers.HyperMtlItemSerializer
    # renderer_classes = [dt_renderers.DatatablesRenderer]
    lookup_field = 'itp_no_mag'
    # permission_classes = [IsAuthenticated,]
    permission_classes = [AllowAny]
    renderer_classes = [renderers.JSONRenderer]