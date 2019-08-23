import sys
sys.path.append("/home/antonio/dev/3183")
from toet.utils import Translator

# Toet uses google translate to help you in translating your pdfs.
# Toet can translate before of pdf generation using pre generated
# vocabularies or in real-time during rendering phase.
# First approach (vocabularies) should be always preferable for
# all the static text of your documents (like table header) due to
# the delay that translation process introduces.
#
# Naturally texts coming from your data source can be translated
# on the fly during rendering phase as well.
#
# In order to create vocabularies files you need:
#
# (1) define in your .py a __t class attribute like below
#
#   __t = {
#        "_t_from" : "From",
#        "_t_to" : "To",
#        "_t_parts" : "Parts",
#        "_t_locations" : "Locations",
#        "_t_available_languages" : "Available Languages",
#   }
#
# (2) set dir that will contains vocabularies files
#
#   TRANSLATION_dir = /somewhere/in/your/disk
#
# (3) specify which modules and classes you want to translate 
#     setting up a INDEX var.
#     Only classes with __t class atribute defined will be taken
#     in consideration; if not they will be skipped  even if they
#     appears in INDEX.
#
# (4) Set source and destination languages for the translation


TRANSLATION_DIR = '/home/antonio/dev/sign_in_sheet/translations'

INDEX = {
   '/tmp/aaa/sign_in_sheets_translator': ['SummaryModel', 'SessionModel',
                                          'InstructorModel']
}


#list_languages = [('en','it'),('en','fr'),('en','de'),('en','ko'),('en','ja'),]
list_languages = [('en','it'),('en','fr'),]

Translator.bulk_generate_vocabularies(TRANSLATION_DIR, INDEX, src_dest=list_languages)
