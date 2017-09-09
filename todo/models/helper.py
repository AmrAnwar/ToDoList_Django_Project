def upload_location(instance, filename):
    """

    :param instance:  can be list, task or sublist
    :param filename: the Image or the attachment name
    :return: string <folder/filename>
    """
    return "%s/%s" % (instance, filename)
