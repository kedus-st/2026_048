from import_export import resources

from .models import Orders

class OrdersResource(resources.ModelResource):
    class Meta:
        model = Orders
        import_id_fields = ('id',)
        skip_unchanged = True

        fields = ('id', 'title', 'ship', 'order_date', 'ordered_by', 'description', 'count', 'link', 'status', 'delivery_date')
        export_order = ('id', 'title', 'ship', 'order_date', 'ordered_by', 'description', 'count', 'link', 'status', 'delivery_date')

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