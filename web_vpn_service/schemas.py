from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import get_doc


class SwaggerSchema(AutoSchema):
    def get_summary(self):
        method_mapping = {
            'GET': 'Get',
            'POST': 'Create',
            'PUT': 'Full update',
            'PATCH': 'Partial update',
            'DELETE': 'Delete',
        }
        serializer = self.get_request_serializer()
        try:
            model = serializer.Meta.model._meta
        except AttributeError:
            return None
        model_description = model.verbose_name or model.getdoc
        start_summary = method_mapping.get(self.method)
        return f'{start_summary} {model_description}'

    def get_description(self):
        """ override this for custom behaviour """
        serializer = self.get_request_serializer()
        try:
            model = serializer.Meta.model
            model_doc = model.__doc__
        except AttributeError:
            model_doc = None
        action_or_method = getattr(self.view, getattr(self.view, 'action', self.method.lower()), None)
        view_doc = get_doc(self.view.__class__)
        action_doc = get_doc(action_or_method)
        return action_doc or view_doc or model_doc
