# 3183 a.k.a. toet
mvc to pdf in a django style 

```python
> python
Type "help", "copyright", "credits" or "license" for more information.
>>> from operator import sub
>>> 
>>> mvc = ['m','v','c']
>>> pdf = ['p', 'd', 'f']
>>> 
>>> a = list(map(ord, mvc))
>>> b = list(map(ord, pdf))
>>> c = list(map(sub, a, b))
>>>
>>> project_name = list(map(abs, c))
>>> print(project_name)
[3, 18, 3] 
```
## Installation

`pip install git+https://github.com/kinderp/3183#egg=3183
`

## Description

3183 is a mvc2pdf tool, it can help you in creating and formatting your pdf report.
Create your layout and form at canvas level is difficult so 3183 gives you a series
of reusable predefined blocks (e.g. `TextField`, `ImageField`, `TableView` ecc) that 
you can use in order to crate more quickly your pdf document. Moreover using a mvc
approach: separating bussign logic from rendering should be traslated in a more readable
maintanable and modifiable code.

## Basic concepts

In a 3183 point of view a pdf document is a layered object.
At the top level there is the`Template` . A template is a
container of `View`s. Views deal with rendering of the `Model`s
so the same model can have different layouts; in other words the
same data (defined in the model) can be displayed in different
ways just using different views

## Model

A model can be definied like below:

```python
class HeaderModel(Model):
    def __init__(self,**kwargs):
        """Init custom Model (Header)
        Parameters: 
            kwargs : { '_title': 'Titolo centrale', '_session': 'Sessione di prova'}
        """
        super(HeaderModel, self).__init__(**kwargs)
        self.session = TextField(text="{}".format(self._session))
        self.title = TextField(text="{}".format(self._title))
        self.logo = ImageField('./sanofi.png', width=50, height=50)
```

So i want to insert 3 fields in my report: 2 `TextField` and 1 `ImageField`
But i need some view to give my data a rendering layout.

### Instantiate a custom model

Before talking about views, let's see how to instantiate a custom model and in particular how to pass dynamic values needed to set Field types in the model.

In your custom model you have to instantiate your fields e.g. `TextField` but values to be filled in are known only by the controller which will instantiate the view and implicitly the model.

Controllers, Views and Models need a valid contract to exachange data.
That's kwargs!

As you maybe noticed above, `__init__` method uses `**kwargs` argument in its definition and
passes that one to its `__init__` super method.

```python
super(HeaderModel, self).__init__(**kwargs):
```

Doing that in the child's code, all the keyworded function parameters in kwargs will be present as instance attributes
in your custom model class. It's a good idea using a prefix underscore when naming your kwargs attributes (e.g. `_session`, `_title`) in order to do not override existing attributes.

You can use this method to pass values in this direction [Controller]->[View]->[Model].

As you can see in the code above `self._session` `self._title` are not explicitly defined but they are used after super() call and came from kwargs dict. 

So here a correct way to pass dynamic values to view and its inner model from a controller.

```python
data_header =  { '_title': 'Titolo centrale', '_session': 'Sessione di prova'}
h = HeaderView(**data_header)
```

It's a good idea documenting kwargs' contents in a docstring.

What Model's __init__ method does is to update its `self.__dict__` with `kwargs`

```python
from abc import ABC

class Model(ABC):
    """
    Defined here interface for model types 
    """
    def __init__(self, **kwargs):
        """
        Init generic model

        Parameters:
            kwargs: it's a dict that will contain data model from controller obj
        """
        self.__dict__.update(kwargs)
```



## View

A view for a model can be defined like below

```python
class HeaderView(TableView):
     def __init__(self, **kwargs):
        self.model = HeaderModel(**kwargs)
        self.fields = [['session', 'title', 'logo']]
        self.span = False

        super(HeaderView, self).__init__(self)
```

In this case i used a `TableView`, my data will be rendered
as a table!

Maybe you noticed 3 class attributes there:

* `model`: a model instance you want to render
* `fields`: fields of your model you want to show in the view
* `span`: use span in rows if possible

All these ones are required but another one does exist: `body_header`
Read next section for a deep intro about View attributes

### TableView


Field        | Required | Description
------------ | ---------|-------------|
`model`      | `True`   | ``
`fields`     | `True`   |
`span`       | `True`   |
`body_header`| `False`  |

#### View.model

#### View.fields

#### View.span

#### View.body_header

### FormView

FormView is like a web form, it renders your data in rows one item at time.
If you don't need any complicated layout (otherwise you should take a look at
`TableView`) and you just want to write some rows of text applying some style
maybe `FormView` could help you.

Below a code example on how to use a `FormView.

Even in this case we have: `self.model`, `self.fields` attributes.
Those ones have the same meaning and behaviour as usal (as explained
in previous sections) but you should take attention to `self.style`;
it defines rendering style for your text rows.

```python

class SummaryModel(Model):

    def __init__(self, **kwargs):
        """Init custom Model (Summary)

        Parameters:
            kwargs : {
                        "_event_name": "Nome evento",
                        "_session_id": "1234abc",
                        "_vendor": "ACME Labs",
                        "_start_date": "01/01/2017",
                        "_end_date": "01/01/2017",
                        "_parts": "1"

            }

        """
        super(SummaryModel, self).__init__(**kwargs)
        self.event_name_and_session_id = TextField("{} - {}".format(self._event_name,
                                                                    self._session_id))
        self.vendor = TextField("{}".format(self._vendor))
        self.start_and_end_date_parts = TextField("From {} to {} (Parts: {})".format(self._start_date,
                                                                                     self._end_date,
                                                                                     self._parts))
from reportlab.lib.enums import TA_CENTER


class SummaryView(FormView):
    def __init__(self, **kwargs):
        self.model = SummaryModel(**kwargs)
        self.fields = [
                        ['event_name_and_session_id'],
                        ['vendor']
        ]

        self.styles = {
            'event_name_and_session_id': {
                'style': 'Normal',
                'space': 4.5,
                'commands': [
                                ('alignment', TA_CENTER),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 18),
                            ]
            },
            'vendor': {
                'style': 'Normal',
                'commands': [
                                ('alignment', TA_CENTER),
                                ('fontSize', 12)
                            ]
            }
        }


        super(SummaryView, self).__init__(self)

```
```python
   data_summary = {
                        "_event_name": "Nome evento",
                        "_session_id": "1234abc",
                        "_vendor": "ACME Labs"
    }

    s_ = SummaryView(**data_summary)
    rendered_fields = s_.render()
```

## Translator

3183 offers you a pratical way to translate your docs.
Basically translation process is just a request to google translate service.
You can choose to translate in two different ways:

* realtime
* batch

In the realtime way, translation is made during rendering phase; this method
should be used only when you can't do otherwise, for example when you get data
to be translated during rendering phase and not before (e.g. data in a table 
body coming from a db or other data sources).

The latter one (batch) is always preferable because of the delay introduced by
translation process. So it is better translate your static data (e.g. header in
a table) before rendering phase, saving your translations in vocabularies files
and use those ones during rendering phase to speed up the whole process.

Batch mode depends on vocaularies files. Let's see how to create those ones for
your custom model classes.
Every 3183 custom model class can define a magic class attribute `__t`. It is just
a dict like below:

```python
__t = {
        "_t_from" : "From",
        "_t_to" : "To",
        "_t_parts" : "Parts",
        "_t_locations" : "Locations",
        "_t_available_languages" : "Available Languages",
    }
```


Every keys in `__t` will be automatically translated when `_()` model magic function
will be called. See below how to invoke `_()`in a custom model class named SummaryModel:

```python
super(SummaryModel, self)._('SummaryModel', SummaryModel.__t)
```

After calling `_()` you can get your translations in two ways in your code:

1. Using `self._t` : it's an instance attribute containing the same keys of `__t` (class attribute) with the translations as values.
2. Each keys in `__t` as instance attributes (e.g. `self._t_from`, `self._t_to`, `self._t_parts` and so on )

`_()` is defined in base `Model` class (infact it is called using `super`)

Below `_()` implementation:

```python
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
```

As you can see `_()` uses four env vars:

* TOET_TRANSLATIONS_DIR
* TOET_SRC_LANG
* TOET_DEST_LANG
* TOET_LOAD_VOCABULARIES

Name         | Description   | Values 
------------ | ------------- | -------------
TOET_TRANSLATIONS_DIR  | absolute path of dir containing translations vocabularies files | `str` (e.g. `/somewhere/in/your/disk`) 
TOET_SRC_LANG          | source translation lang      | `str` (e.g. `en`)
TOET_DEST_LANG         | destination translation lang | `str` (e.g. `it`)
TOET_LOAD_VOCABULARIES | load translations from disk  | `int` (e.g. `1` or `0`)

See [here](https://github.com/kinderp/3183/blob/master/examples/vocabularies_generator.py) for a working
code example or below for a teorical one of a vocabularies generator

```python
from toet.utils import Translator

TRANSLATION_DIR = '/somewhere/in/your/disk/translations'

INDEX = {
   '/absolete/path/of/a/module/module_name': ['CustomModelClass1', 'CustomModelClass2',
                                              'CustomModelClass3']
}

list_languages = [('en','it'),('en','fr'),('en','de'),('en','ko'),('en','ja'),]
Translator.bulk_generate_vocabularies(TRANSLATION_DIR, INDEX, src_dest=list_languages)
```

All is in `bulk_generate_vocabularies`, it will get and translate `__t` in every class 
defined in `INDEX` (`CustomModelClass1`, `CustomModelClass2`, `CustomModelClass3`) if `__t`
is not defined in these classes nothing will happen, so take attention. Keys in `INDEX` are
absolute paths  (without .py at the end) of modules containing those classes.
`TRANSLATION_DIR` is absolute path of the dir where toet will save your vocabularies.
So remember to set `TOET_LOAD_VOCABULARIES` to the same value of `TRANSLATION_DIR`to load 
correctly your vocabularies.

After runnning a vocabularies generator your translations file will be saved in `TRANSLATION_DIR`
and you can set the 4 vars and call you render function

```python
        os.environ['TOET_LOAD_VOCABULARIES'] = "1"
        os.environ['TOET_TRANSLATIONS_DIR'] = "/somewhere/in/your/disk/translations"
        os.environ['TOET_SRC_LANG'] = 'en'
        os.environ['TOET_DEST_LANG'] = 'ko'
        my_render_function()
```

Take in consideration that vocabularies files are just simple json files (see below) you are
free to edit it to improve translation.

```json
{
    "origin": {
        "_t_from": "From",
        "_t_to": "To",
        "_t_parts": "Parts",
        "_t_locations": "Locations",
        "_t_available_languages": "Available Languages"
    },
    "text": {
        "_t_from": "A partire dal",
        "_t_to": "A",
        "_t_parts": "Parti",
        "_t_locations": "sedi",
        "_t_available_languages": "Lingue disponibili"
    }
}
```

## Template

As you can see below to create a pdf i just have to instantiate
a template, my previous view (see above) and finally build the doc.

```python
if __name__ == '__main__':
    doc = SimpleDocTemplate('test.pdf', pagasize=A4)
    story = Story()

    some_space = Spacer(1,10)

    h = HeaderView()

    rendered_fields = h.render()
    story.add(rendered_fields) 

    doc.build(story.get())

```

Below an image of the result.
As you can see you have a row with the 3 fields `session`, `title`, `logo` that you have defined in your model

![header](https://github.com/kinderp/3183/blob/master/header.png)

## Usage

Controller classes have not been created yet, so data are hardcoded in main.py.
If you run `python main.py` in the root dir project a pdf like below will be generated:


![header](https://github.com/kinderp/3183/blob/master/result.png)

At this point you can start to play with 3183, let suppose you wanna modify Session data in your pdf in this way:

* Delete Bullet3 in the first row
* Put session_id field below session_title (2 columns intead of just one)
* Add a location row
* Put language below version
* Add a enrolment row

those ones are the only changes you need to do

```python
class SessionModel(Model):
    session_type = TextField(text="Session Type: ")
    s1 = BulletTextField(text='VILT')
    s2 = BulletTextField(text='ILT')
    #s3 = BulletTextField(text='Bullet 3')

    session_title = TextField(text='Session Title: ')
    session_id = TextField(text="Session Id: ")

    location = TextField(text="Location (country, site)")

    version = TextField(text="Version 1.0")
    language = TextField(text="Language: English")

    start_date = TextField("Start date: 01/01/2017")
    end_date = TextField("End date: 01/01/2017")
    duration = TextField("Duration: 1h20m")
    enrolment = TextField("Enronlment: ")

class SessionView(TableView):
    model = SessionModel()
    #fields = [
    #          ['session_type', 's1', 's2', 's3'],
    #          ['session_title', 'session_id'],
    #          ['version', 'language'],
    #          ['start_date', 'end_date', 'duration']
    #]

    fields = [
              ['session_type', 's1', 's2'],
              ['session_title'],
              ['session_id'],
              ['location'],
              ['version'],
              ['language'],
              ['enrolment'],
              ['start_date', 'end_date','duration']
             ]

```

and thse the result

![header](https://github.com/kinderp/3183/blob/master/result2.png)


