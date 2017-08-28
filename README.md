# About Topsy

This project is an experiment in using "ports and adapters" style architecture with the Django
framework. The example is a note-taking app called Topsy, which allows users to create notes,
organize them into boards, and share them with other users. For the purposes of the example, we're
assuming a (non-existent) single page web app that fetches data from Django views which return JSON.

The project consists of two Django apps:

* notes: handles content creation, viewing, and management

* accounts: handles account creation and management

In addition to the standard models and views within each app, you will find files containing
entities and use cases.

**Entities** are simple value object classes that correspond to the models.

**Use cases** are functions that manipulate entities according to the business rules of the app. The
use cases are methods of a class that is instantiated with a storage adapter, allowing us to
decouple them from the Django ORM.

The views are responsible for passing user input to use cases and returning the result of the use
case to the user (or returning an error). No business logic code is stored in Django views or
models, thus decoupling all domain code from the framework, and from any knowledge of the storage
and HTTP layers.

## Inspiration for this project

* [Hexagonal Architecture](http://alistair.cockburn.us/Hexagonal+architecture)

* [The Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html)

* [The Clean Architecture in Python](https://www.youtube.com/watch?v=DJtef410XaM)

## Alternatives

* Leonardo Giordani [wrote a post](http://blog.thedigitalcatonline.com/blog/2016/11/14/clean-architectures-in-python-a-step-by-step-example/) and [published a repo](https://github.com/lgiordani/rentomatic) applying this architecture to Django

* Jordi Fierro [wrote a post](https://engineering.21buttons.com/clean-architecture-in-django-d326a4ab86a9) and [published a repo](https://github.com/jordifierro/abidria-api) exploring the same ideas with Django
