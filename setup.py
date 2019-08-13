from setuptools import setup

setup(
    name = "3183",
    version = "0.0.1",
    author = "Antonio Caristia (kinderp)",
    author_email = "a.caristia@gmail.com",
    description = ("mvc2pdf in a django style"),
    license = "GPL",
    keywords = "",
    url = "https://github.com/kinderp/3183",
    packages=['3183', '3183.examples', '3183.fields', '3183.models', '3183.styles', '3183.utils', '3183.views'],
    install_requires=[
          'Pillow','reportlab',
    ],
    include_package_data=True,
    zip_safe=False
)

