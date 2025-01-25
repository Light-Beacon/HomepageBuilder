from .bases import FileBasedPage

class RawXamlPage(FileBasedPage):
    """纯XAML页面"""
    @property
    def display_name(self):
        return self.file.name

    def generate(self, context):
        return self.file.data