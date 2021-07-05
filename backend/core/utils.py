class NestedUpdateCreate:
    '''
    For the .set() method-
    https://docs.djangoproject.com/en/dev/ref/models/relations/#django.db.models.fields.related.RelatedManager.remove
    '''
    def __init__(self, Parent, Child, related_name, validated_data=None):
        self.parent = Parent
        self.child = Child
        self.related_name = related_name
        self.validated_data = validated_data

    def get_or_create_packages(self, child_data):
        child_ids = []
        for data in child_data:
            child_instance, _ = self.child.objects.get_or_create(pk=data.get('id'), defaults=data)
            child_ids.append(child_instance.pk)
        return child_ids

    def create_or_update_packages(self, child_inst):
        '''
        Since m2m and foreignkey accept objects in their set
        '''
        child_instances = []
        for data in child_inst:
            child_instance, _ = self.child.objects.update_or_create(pk=data.get('id'), defaults=data)
            child_instances.append(child_instance)
        return child_instances

    def create(self, validated_data):
        child_instance = validated_data.pop(self.related_name, [])
        parent_instance = self.parent.objects.create(**validated_data)
        rn = getattr(parent_instance, self.related_name)
        rn.set(self.get_or_create_packages(child_instance))
        return parent_instance

    def update(self, instance, validated_data):
        child_instance = validated_data.pop(self.related_name, [])
        rn = getattr(instance, self.related_name)
        rn.set(self.create_or_update_packages(child_instance))

        return