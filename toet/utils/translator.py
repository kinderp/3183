from googletrans import Translator as GoogleTranslator
from types import SimpleNamespace
import os
import sys
import json
import time

class Translator:
    """3183 Translator Class.

    It reads translator class attribute __t  and gets translations:

    (a) from disk (it needs to generate vocabularies, disk=True).
    (b) from web  (default behaviour, disk=False).

    Be sure to define __t class attribute in your class to get translations.

    (disk=True, write=False):
    Get translations from disk (vocabularies files) and if a file does not
    exist raise an error and do not translate and create missing files.
    Before doing that you should generate vocabularies with generate_vocabularies.

    (disk=False, write=False):
    Get translations from web and do not write translations in voabularies
    files.

    (disk=True and write=True)
    Get translations from disk and if a file does not exit translate that one
    from web and write it onto the disk.

    (disk=False and write=True)
    Get translation from web and write vocabuaries onto the disk.

    (translation_dir):
    Set translation_dir in __init__ method to define either where your
    vocabularies will be created (write=True) or where to get vocabularies
    (disk=True) for translations.

    If translation_dir won't be set a new dir named "translations" will be
    created into the current dir.
    In both cases a new subdir in "translations" dir will be created for each
    class with a __t attribute defined.


        translations/
        ├── SessionModel
        │   ├── en-de.json
        │   ├── en-fr.json
        │   ├── en-it.json
        │   ├── en-ja.json
        │   └── en-ko.json
        └── SummaryModel
            ├── en-de.json
            ├── en-fr.json
            ├── en-it.json
            ├── en-ja.json
            └── en-ko.json

    Translations files are in json format with two keys:
    1. origin: original   __t content
    2. text  : translated __t content

    (e.g.)
        {
        "origin": {
            "_t_starts": "Starts",
            "_t_end": "End",
            "_t_break": "Breaks",
            "_t_sesion_location": "Session Location",
            "_t_participants": "Participants",
            "_t_signatures": "SIGNATURES",
            "_t_part": "Part",
            "_t_observations": "Observarions"
        },
        "text": {
            "_t_starts": "inizia",
            "_t_end": "Fine",
            "_t_break": "Pause",
            "_t_sesion_location": "Posizione della sessione",
            "_t_participants": "I partecipanti",
            "_t_signatures": "FIRME",
            "_t_part": "Parte",
            "__t_observations": "osservazioni"
        }

    """

    def __init__(self, src='en', dest='it', disk=False, write=False, translation_dir='./translations'):
        """

        Args:
            src             (str ): source translation language
            dest            (str ): dest   translation language

            disk            (bool): True = load translation from disk
                                           Note: it needs vocabularies.
                                           Use generate_vocabularies() for that.
                                           Set translation_dir to the correct
                                           path where you saved your
                                           vocabularies.
                                   False = load translation from web (Google)

            write           (bool): if translations comes from web (disk=False)
                                    it writes translations on the disk. So it
                                    will generate vocabularies on the fly.
                                    Set translation_dir to the path where you
                                    want to save your vocabularies.
                                    It could overwrite your old vocabularies.
                                    if translations comes from disk (disk=True)
                                    and a file vocabulary does not exist it'll
                                    translate that one from web and then store
                                    ii on the disk.

            translation_dir (str ): dir where are located or where will be
                                    created tranlations tree with vocabularies
                                    files. Use this var in conjunction with disk
                                    or write var.
        """
        self.TRANSLATION_DIR = translation_dir
        self.src = src
        self.dest = dest
        self.disk = disk
        self.write = write
        self.gt = GoogleTranslator()
        if self.disk == True or self.write == True:
            # if write in or load from vocabularies
            # i need to know where is located on the disk
            if self.TRANSLATION_DIR is None:
                raise ValueError("You MUST set translation_dir in __init__\n")

    def _translation_filename(self, class_name, src, dest):
        """Generate translation filename"""
        translation_subdir = "{}/{}".format(self.TRANSLATION_DIR, class_name)
        if not os.path.exists(translation_subdir):
            os.makedirs(translation_subdir)
        return "{}/{}/{}-{}.json".format(self.TRANSLATION_DIR, class_name, src, dest)

    def _translate_from_disk(self, class_name, src=None, dest=None):
        """Load translation from disk"""
        if src is None: src=self.src
        if dest is None: dest=self.dest
        translation_filename = self._translation_filename(class_name, src=src, dest=dest)
        # TODO: if file vocabulary does not exist and self.write is True
        #       translate frm web and write a new file.
        with open(translation_filename, "r") as translation_file:
            return json.load(translation_file)

    def bulk_translate_from_web(self, index_words_to_translate, src=None,
                                dest=None, obj=False):
        """Get translations from Google

        It sends only a request for all the keys in __t
        So translates all the values of keys in __t (index_words_to_translate) in a
        single request.

        index_words_to_translate:

           {
                "_t_from" : "From",
                "_t_to" : "To",
                "_t_parts" : "Parts",
                "_t_locations" : "Locations",
                "_t_available_languages" : "Available Languages",
            }

        inverted_index:

            {
                'From': '_t_from',
                'To': '_t_to',
                'Parts': '_t_parts',
                'Locations': '_t_locations',
                'Available Languages': '_t_available_languages'
            }

        Args:
            index_words_to_translate (dict): A dict containing all the string
                                             to be translated
            src  (str): source translation lang
            dest (str): dest translation lang
            obj (bool): define response format.
                        if True response is a dict with the same keys of the
                        origin dict (index_words_to_translate) and values
                        translated to the dest lang.
                        if False response is an object with attributes coming
                        from keys of the origin dict (index_words_to_translate)
        Retrurns:
            given in input a index_words_to_translate like below:

                {
                    "_t_from" : "From",
                    "_t_to" : "To",
                    "_t_parts" : "Parts",
                    "_t_locations" : "Locations",
                    "_t_available_languages" : "Available Languages",
                }

            if obj is False it returns a dict like below (e.g. en->it) :

                {
                    "_t_from" : "Da",
                    "_t_to" : "A",
                    "_t_parts" : "Parti",
                    "_t_locations" : "Luoghi",
                    "_t_available_languages" : "Lingue Disponibili",
                }

            if obj is True it returns an obj with these attributes:

                translated._t_from                <- 'Da'
                translated._t_to                  <- 'A'
                translated._t_parts               <- 'Parti'
                translated._t_locations           <- 'Luoghi'
                translated._t_available_languages <- 'Lingue Disponibili'
        """
        if src is None: src=self.src
        if dest is None: dest=self.dest

        inverted_index = {index_words_to_translate[key]: key for key in index_words_to_translate}
        list_of_words = [index_words_to_translate[key] for key in index_words_to_translate]
        translations = self.gt.translate(list_of_words, src=src, dest=dest)
        translated = {inverted_index[elem.origin]: elem.text for elem in translations}
        if not obj: return translated
        else: return SimpleNamespace(**translated)

    def translate_from_web(self, index_words_to_translate, src=None,
                           dest=None, obj=False):
        """Get translations from Google

        It sends a request for each key in __t (index_words_to_translate)
        See bulk_translate_from_web() for better performance.
        """
        if src is None: src=self.src
        if dest is None: dest=self.dest

        translated = {}
        for index in index_words_to_translate:
            print(index_words_to_translate[index])
            translated[index] = self.gt.translate(index_words_to_translate[index], src=src, dest=dest).text
        if not obj:return translated
        else: return SimpleNamespace(**translated)

    def _write_translations(self, origin_text, translated_text, class_name,
                            src=None, dest=None):
        """Write translation on disk"""
        if src is None: src=self.src
        if dest is None: dest=self.dest

        translation_filename = self._translation_filename(class_name, src=src, dest=dest)
        tmp = {
            "origin" : origin_text,
            "text": translated_text,
        }
        with open(translation_filename, "w") as translation_file:
            json.dump(tmp, translation_file, indent=4)

    def translate(self, child=None, to_translate=None, src=None, dest=None):
        if src is None: src=self.src
        if dest is None: dest=self.dest
        translated = None
        if self.disk:
            # translate from disk (vobabularies)
            if child is None: raise ValueError("You need to set child in __init__")
            translated = self._translate_from_disk(child)
        else:
            # translate from web (google)
            if to_translate is None: raise ValueError("You need to set to_translate in __init__")
            translated = self.bulk_generate_vocabularies(to_translate)
        return translated['text']

    @classmethod
    def write_translations(cls, TRANSLATION_DIR, origin_text, translated_text, class_name, src, dest):
        """Write translation on disk"""

        def translation_filename(class_name, src, dest):
            """Generate translation filename"""
            translation_subdir = "{}/{}".format(TRANSLATION_DIR, class_name)
            if not os.path.exists(translation_subdir):
                os.makedirs(translation_subdir)
            return "{}/{}/{}-{}.json".format(TRANSLATION_DIR, class_name, src, dest)

        translation_filename = translation_filename(class_name, src=src, dest=dest)
        tmp = {
            "origin" : origin_text,
            "text": translated_text,
        }
        with open(translation_filename, "w") as translation_file:
            json.dump(tmp, translation_file, indent=4)

    @classmethod
    def bulk_generate_vocabularies(cls, TRANSLATION_DIR='./translations', INDEX={}, src_dest=[('en', 'it'),], delay=2*60):


        """Create translations (vocabularies) for all the classes in INDEX

        A translations request is sent for all the classes in a module.
        A delay is applied before proceding wiht the next requests.

        SummaryModel.__t = {
                            "__t_from" : "From",
                            "__t_to" : "To",
                            "__t_parts" : "Parts",
                            "__t_locations" : "Locations",
                            "__t_available_languages" : "Available Languages",
                           }

        SessionModel.__t = {
                            "__t_starts" : "Starts",
                            "__t_end" : "End",
                            "__t_break" : "Breaks",
                            "__t_sesion_location" : "Session Location",
                            "__t_participants": "Participants",
                            "__t_signatures": "SIGNATURES",
                            "__t_part": "Part",
                            "__t_observations": "Observations",
                           }

        src_dest:

            [('en','it'),('en','fr'),]

        self.INDEX:
            A dict where keys are modules and values classes in that module

            {'sign_in_sheets_translator': ['SummaryModel', 'SessionModel']}

        __t_index:
            A dict containing __t for each class in a module

            {
                'SummaryModel': {
                    '__t_from': 'From',
                    '__t_to': 'To',
                    '__t_parts': 'Parts',
                    '__t_locations': 'Locations',
                    '__t_available_languages': 'Available Languages'
                },
                'SessionModel': {
                    '__t_starts': 'Starts',
                    '__t_end': 'End',
                    '__t_break': 'Breaks',
                    '__t_sesion_location':'Session Location',
                    '__t_participants': 'Participants',
                    '__t_signatures': 'SIGNATURES',
                    '__t_part': 'Part',
                    '__t_observations': 'Observations'
                }
            }

        inverted_index:

            {
                'From': ['__t_from'],
                'To': ['__t_to'],
                'Parts': ['__t_parts'],
                'Locations': ['__t_locations'],
                'Available Languages': ['__t_available_languages'],
                'Starts': ['__t_starts'],
                'End': ['__t_end'],
                'Breaks': ['__t_break'],
                'Session Location': ['__t_sesion_location'],
                'Participants': ['__t_participants'],
                'SIGNATURES': ['__t_signatures'],
                'Part': ['__t_part'],
                'Observations': ['__t_observations']
            }

        list_of_words:
            All the words to be translated

            ['From', 'To', 'Parts', 'Locations', 'Available Languages',
             'Starts', 'End', 'Breaks', 'Session Location', 'Participants',
             'SIGNATURES', 'Part', 'Observations']


        translated:
            A dict containing all the translations for all
            the classes in a module

        (en-it)
            {
                '__t_from': 'A partire dal',
                '__t_to': 'A',
                '__t_parts': 'Parti',
                '__t_locations': 'sedi',
                '__t_available_languages': 'Lingue disponibili',
                '__t_starts': 'inizia',
                '__t_end': 'Fine',
                '__t_break': 'Pause',
                '__t_sesion_location': 'Posizione della sessione',
                '__t_participants': 'I partecipanti',
                '__t_signatures': 'FIRME',
                '__t_part': 'Parte',
                '__t_observations': 'osservazioni'
            }
        """
        def get_module_name_and_path(absolute_path):
            splitted = absolute_path.split('/')
            module_name = splitted[-1]
            path = "/".join(splitted[:-1])
            return module_name, path

        for elem in src_dest:
            for a_module in INDEX:
                if "/" in a_module:
                    module_name, path = get_module_name_and_path(a_module)
                    if path not in sys.path:
                         sys.path.append(path)
                else:
                    module_name = a_module
                list_clsses_in_a_module = INDEX[a_module]
                inverted_index = {}
                translated = {}
                list_of_words = []
                __t_index = {}
                for a_class in list_clsses_in_a_module:
                    import_statement = "from {a_module} import {a_class}".format(a_module=module_name, a_class=a_class)
                    exec(import_statement)
                    class_attribute_name = "_{}__t".format(a_class)
                    __t = getattr(eval(a_class), class_attribute_name)
                    __t_index[a_class] = __t
                    for key in __t:
                        if __t[key] in inverted_index:
                            inverted_index[__t[key]].append(key)
                        else:
                            inverted_index[__t[key]] = []
                            inverted_index[__t[key]].append(key)
                        list_of_words.append(__t[key])

                # at this point list_of_words contains all texts to be
                # translated for all classes in a module (see INDEX).
                # Let's traduce all those ones

                # uncomment for debug
                #print("data for module: {}\n".format(a_module))
                #print("__t_index: \n{}\n".format(json.dumps(__t_index, indent=4, sort_keys=True)))
                #print("inverted_index: \n{}\n".format(json.dumps(inverted_index, indent=4, sort_keys=True)))

                #translations = self.gt.translate(list_of_words, src=elem[0],dest=elem[1])

                translations =  GoogleTranslator().translate(list_of_words, src=elem[0],dest=elem[1])
                for response in translations:
                    original_keys = inverted_index[response.origin]
                    for orignal_key in original_keys:
                       translated[orignal_key] = response.text

                #print("translated: \n{}\n".format(json.dumps(translated, indent=4, sort_keys=True)))

                for a_class in __t_index:
                    # rebuild __t dict with translated text
                    # for each class in a module
                    translated__t = {}
                    original__t = __t_index[a_class]
                    for key in original__t:
                        translated__t[key] = translated[key]

                    #print("{}.original__t: \n{}\n".format(a_class,json.dumps(original__t, indent=4, sort_keys=True)))
                    #print("{}.translated__t: \n{}\n".format(a_class, json.dumps(translated__t, indent=4, sort_keys=True)))
                    # wirte translation for a class
                    cls.write_translations(TRANSLATION_DIR, original__t, translated__t, a_class, src=elem[0], dest=elem[1])

                # to avoid ip banning from bigg
                print("Please wait, Translator is running. It'll take a while...\n")
                time.sleep(delay)
