class NoSuchXmlFilesException(Exception):
    """This exceptions occurs when there is absolutely no files by given provider"""
    pass


class NoSuchOneXmlFileException(Exception):
    """This exceptions occurs when there is one of files by given provider is absent"""
    pass

class NoGoodValuesException(Exception):
    pass