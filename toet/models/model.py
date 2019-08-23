from abc import ABC

import os

from toet.utils import Translator

class Model(ABC):
    """
    Defined here interface for model types
    """

    def __init__(self, __t=None, **kwargs):
        """
        Init generic model

        Parameters:
            kwargs: it's a dict that will contain data model from controller obj
        """
        self.__dict__.update(kwargs)

    def _(self, child, __t):
        if __t is not None:
            CLIENT_TRANSLATIONS_DIR = os.getenv('TOET_TRANSLATIONS_DIR')
            SRC_LANG = os.getenv('TOET_SRC_LANG', 'en')
            DEST_LANG = os.getenv('TOET_DEST_LANG', 'it')
            LOAD_FROM_DISK = bool(int(os.getenv('TOET_LOAD_VOCABULARIES')))
            if LOAD_FROM_DISK:
                translated__t = Translator(src=SRC_LANG, dest=DEST_LANG,
                                           disk=True, write=False,
                                           translation_dir=CLIENT_TRANSLATIONS_DIR).translate(child)
                #_translate_from_disk(child)
            else:
                translated__t = Translator(src=SRC_LANG, dest=DEST_LANG,
                                           disk=False,
                                           write=False).translate(__t)
                #bulk_translate_from_web(__t)
            self.__dict__.update(translated__t)
            self.__dict__.update({'_t': translated__t})

