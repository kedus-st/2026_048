from rest_framework import serializers
from . import models


class MtlItemRestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MtlItem
        fields = ('itp_no_mag', 'kp', 'kp_offset', 'easting', 'northing', 'found', 'uxo', 'salvaged',
                  'clear', 'cl_date', 'description_detail', 'cl_weight', 'cl_length', 'cl_width', 'eod', 'surveyor',
                  'qa_clear')
        lookup_field = 'itp_no_mag'
        extra_kwargs = {'url': {'lookup_field': 'itp_no_mag'}}


class MtlItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.MtlItem
        fields = (
            'id',
            'itp_no_mag',
            #'kp',
            #'kp_offset',
            'easting', 'northing', 'found', 'uxo', 'salvaged',
                  'clear', 'cl_date', 'description_detail', 'cl_weight', 'cl_depth_bg', 'cl_length', 'cl_width', 'eod', 'surveyor', 'qa_comments',
                  'qa_clear')
        datatables_always_serialize = ('id',)

class HyperMtlItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.MtlItem
        fields = ['itp_no_mag', 'kp', 'kp_offset', 'easting', 'northing', 'found', 'uxo', 'salvaged',
                  'clear', 'cl_date', 'description_detail', 'cl_weight', 'cl_length', 'cl_width', 'eod', 'surveyor',
                  'qa_clear']

class WetStoreContainerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.MtlItem
        fields = (
            'id',
            'wsc_id',
            'easting', 'northing')
        datatables_always_serialize = ('id',)

class WetStoreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.MtlItem
        fields = (
            'id',
            'ws_id',
            'easting_tl', 'northing_tl',
            'orientation', 'cell_count', 'width', 'height')
        datatables_always_serialize = ('id',)


