from django.core.exceptions import ValidationError

def mobile_check(value):
    allowed_starting = ['055', '050', '053']
    if len(value) == 10 and value.isnumeric() and value.startswith(tuple(allowed_starting)):
        return int(value)
    else:
        # print(len(value))
        # print(value.isnumeric())
        # print(value.startswith(tuple(allowed_starting)))
        raise ValidationError('Please enter a valid mobile number')
