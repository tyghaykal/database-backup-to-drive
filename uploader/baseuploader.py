import os
import gzip
import shutil
from datetime import datetime

class BaseUploader:
    def __init__(self, retention_count):
        self.retention_count = retention_count
