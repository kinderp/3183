# 3183
mvc to pdf in a django style 

```python
> python
Python 3.7.3 (default, Apr 09 2019, 05:18:21) [GCC] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from operator import sub
>>> 
>>> mvc = ['m','v','c']
>>> pdf = ['p', 'd', 'f']
>>> 
>>> a = list(map(ord, mvc))
>>> b = list(map(ord, pdf))
>>> c = list(map(sub, mvc, pdf))
>>>
>>> c = list(map(sub, a, b))
>>> project_name = list(map(abs, c))
>>> print(project_name)
[3, 18, 3] 
```

## Description

3183 is a mvc2pdf tool, it can help you in creating and formatting your pdf report.
Create your layout and form at canvas level is difficult so 3183 gives you a series
of reusable predefined blocks (e.g. `TextField`, `ImageField`, `TableView` ecc) that 
you can use in order to crate more quickly your pdf document. Moreever using a mvc
approach: separating bussign logic to rendering should be traslated in more readable
maintable and modifiable code.

## Basic concepts

In a 3183 point of view a pdf document is a layered object.
At the top level there is the`Template` . A template is a
container of `View`s. Views deal with rendering of the `Model`s
so the same model can have different layouts in other words the
same data (defined in the model) can be displayed in different
ways using different views

## Model

A model can be definied like below:

```python
class HeaderModel(Model):
    session = TextField(text="prova")
    title = TextField(text='titolo')
    logo = ImageField('./sanofi.png', width=50, height=50)

```

So i want to insert 3 fields in my view: 2 `TextField` and 1 `ImageField`
But i need some view to give my data a rendering layout.

## View

A view for a model can be defined like below

```python
class HeaderView(TableView):
     model = HeaderModel()
     fields = [['session', 'title', 'logo']]
     span = False

     def __init__(self):
        super(HeaderView, self).__init__(self)

     def render(self):
        return super().render()
```

In this case i used a `TableView`, my data will be rendered
in a table!

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

Controller classes has not been created yet, so data are hardcoded in main.py.
If you run `python main.py` in the root dir project a pdf like below will be generated:


![header](https://github.com/kinderp/3183/blob/master/result.png)
