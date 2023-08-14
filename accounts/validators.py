from django.core.exceptions import ValidationError
import os
def allow_only_image(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions = ['.PNG','.jpg','.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extensions.Supported extensions:'+str(valid_extensions))
    