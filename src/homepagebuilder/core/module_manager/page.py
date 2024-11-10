from ..utils.event import listen_event
from ..logger import Logger
from ..i18n import locale as t

logger = Logger('Module')

scripted_page_classes = []
def page_class_handles(*names, show_in_list:bool = False):
    def deco(cls):
        scripted_page_classes.append((names,cls,show_in_list))
    return deco

@listen_event('project.import.pages.return')
def add_scripted_pages(project,**_):
    if len(scripted_page_classes) < 1:
        return
    logger.info(t('module.page.import.start'))
    for names,cls,show_in_list in scripted_page_classes:
        logger.info(t('module.page.import.one.init',name=names[0]))
        page = cls(project)
        if show_in_list:
            project.pagelist.append(names[0])
        for name in names:
            logger.info(t('module.page.import.one.add',name=name))
            project.pages[name] = page
    logger.info(t('module.page.import.success'))