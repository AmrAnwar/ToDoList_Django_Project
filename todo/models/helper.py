from exceptions import AttributeError


def upload_location(instance, filename):
    return "%s/%s" % (instance.title, filename)