import io
import os

from django.core.files.storage import get_storage_class
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

from web_vpn_service import celery_app


@celery_app.task(serializer='pickle')
def convert_model_image_to_webp_format(obj, attr: str = 'file') -> tuple[bool, str]:
    old_file = getattr(obj, attr, None)
    if not old_file:
        return False, f'Model {obj._meta.object_name} does not have attribute f{attr}'
    old_file_name = old_file.name
    new_file = convert_image_to_webp_format(old_file_name)
    if new_file:
        setattr(obj, attr, new_file)
        obj.save(update_fields=[attr])
        storage = get_storage_class()()
        storage.delete(old_file_name)
    return True, ''


def convert_image_to_webp_format(file_name: str) -> InMemoryUploadedFile | None:
    old_file_name_parts = file_name.split('.')
    file_extension = old_file_name_parts[-1]
    if isinstance(file_extension, str) and file_extension.lower() in ['jpeg', 'jpg', 'png']:
        storage = get_storage_class()()
        file_st = storage.open(file_name, 'rb')
        image = Image.open(file_st)
        buffer = io.BytesIO()
        image = image.convert('RGB')
        image.save(buffer, format='webp')
        file_st.close()
        new_file_name = old_file_name_parts[0]
        new_file = InMemoryUploadedFile(
            buffer, None, f'{new_file_name}.webp', 'image/webp', buffer.seek(0, os.SEEK_END), None,
        )
        return new_file
