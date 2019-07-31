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
