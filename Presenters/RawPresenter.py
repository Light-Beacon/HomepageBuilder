from .base import Presenter_Base
class RawPresenter(Presenter_Base):
    def build(card):
        return card['data']