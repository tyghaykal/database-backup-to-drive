from .baseuploader import BaseUploader

class LocalSaver(BaseUploader):
    def __init__(self, retention_count):
        super().__init__(retention_count)
