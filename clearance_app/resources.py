from import_export import resources

from .models import MtlItem

class MtlItemResource(resources.ModelResource):
    
    def after_save_instance(self, instance, using_transactions, dry_run):
        if (instance.easting is None) or (instance.northing is None):
            pass
        else:
            instance.geom = instance.get_geom()

    class Meta:
        model = MtlItem
        import_id_fields = ('itp_no_mag',)
        skip_unchanged = True

        fields = ('itp_no_mag',
                  'easting',
                  'northing',
                  'lat',
                  'lon',
                  'water_depth_geoid',
                  'model_depth_geoid',
                  'model_depth_below_ground',
                  'model_weight',
                  'mag_moment',
                  'anomaly_max',
                  'anomaly_min',
                  'dipole_width',
                  'dipole_pp',
                  #'sensor_altitude',
                  'itp_notes',
                  'munition_category',
                  'todo_target',
                  'prio',
                  'section',
                  'cl_date',
                  'cl_time',
                  'vessel',
                  'eod',
                  'surveyor',
                  'clearance_co',
                  'cl_weight',
                  'cl_length',
                  'cl_width',
                  'cl_depth_bg',
                  'tr_comment',
                  'found',
                  'salvaged',
                  'uxo',
                  'to_detonate',
                  'detonated',
                  'safety_dist',
                  'clear',
                  'qa_clear',
                  'description_detail',
                  'qa_comments',)

        export_order = ('itp_no_mag',
                        'easting',
                        'northing',
                        'lat',
                        'lon',
                        'water_depth_geoid',
                        'model_depth_geoid',
                        'model_depth_below_ground',
                        'model_weight',
                        'mag_moment',
                        'anomaly_max',
                        'anomaly_min',
                        'dipole_width',
                        'dipole_pp',
                        #'sensor_altitude',
                        'itp_notes',
                        'munition_category',
                        'todo_target',
                        'prio',
                        'section',
                        'cl_date',
                        'cl_time',
                        'vessel',
                        'eod',
                        'surveyor',
                        'clearance_co',
                        'cl_weight',
                        'cl_length',
                        'cl_width',
                        'cl_depth_bg',
                        'tr_comment',
                        'found',
                        'salvaged',
                        'uxo',
                        'to_detonate',
                        'detonated',
                        'safety_dist',
                        'clear',
                        'qa_clear',
                        'description_detail',
                        'qa_comments',)
        
        use_bulk = True

    def get_export_headers(self):
        headers = []
        for field in self.get_fields():
            model_fields = self.Meta.model._meta.get_fields()
            header = next((x.verbose_name for x in model_fields if x.name == field.column_name), field.column_name)
            headers.append(header)
        return headers
    
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        field_names = [None] * len(self.get_fields())
        headers = dataset.headers
        model_fields = self.Meta.model._meta.get_fields()
        for field in self.get_fields():
            print(f"Processing field: {field.column_name}")
            for x in model_fields:
                if x.name == field.column_name:
                    print(f"Checking model field: {x.name} with verbose name: {x.verbose_name}")

                    field_names[headers.index(x.verbose_name)] = x.name
                
        dataset.headers = field_names