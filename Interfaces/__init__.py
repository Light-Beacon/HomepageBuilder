from Core.ModuleManager import script,invoke_module as invoke, require
from Core.ModuleManager.page import page_class_handles
from Core.IO import file_reader, file_writer, read_string, write_string
from Core.logger import Logger
from Core.utils.encode import encode_escape, decode_escape
from Core.utils.formatter import format_code
from Core.i18n import locale
from Core.utils import enable_by
from Core.page import PageBase, FileBasedPage
from Core.config import enable_by_config,DisabledByConfig, config