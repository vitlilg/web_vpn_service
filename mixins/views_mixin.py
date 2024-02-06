from rest_framework.viewsets import GenericViewSet


class ListSerializerClassMixin(GenericViewSet):
    list_serializer_class = None

    def get_serializer(self, *args, **kwargs):
        if not self.serializer_class:
            raise NotImplementedError('Please set the value of the serializer_class attribute')
        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list' and self.list_serializer_class:
            return self.list_serializer_class
        return self.serializer_class
