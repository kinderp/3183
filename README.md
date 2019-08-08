# 3183
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

As you maybe noticed, `__init__` method uses `**kwargs` argument in its definition and
passes that one to its `__init__` father method.

```python
super(HeaderModel, self).__init__(**kwargs:
```

Doing that, all the keyworded function parameters in kwargs will be present as instance attributes
in your custom model class.

As you can see in the code above `self._session` `self._title` are not explicitly defined but came from
kwargs dict. 

So here a correct way to instantiate your custom model class.

```python
data_header =  { '_title': 'Titolo centrale', '_session': 'Sessione di prova'}
h = HeaderView(**data_header)
```



What Model's __init__ method does is to update its `self.__dict__` with `kwargs`

```
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


