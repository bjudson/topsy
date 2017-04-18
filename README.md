# About Topsy

This project is an experiment in using "ports and adapters" style architecture with the Django
framework. The example is a note-taking app called Topsy, which allows users to create notes,
organize them into boards, and share them with other users. For the purposes of the example, we're
assuming a (non-existent) single page web app that fetches data from Django views which return JSON.

The project consists of three Django apps:

* notes: handles content creation, viewing, and management

* accounts: handles account creation and management

* payments: handles integration with Stripe

In addition to the standard models and views within each app, you will find files containing
entities and use cases.

Entities are simple value object classes that correspond to the models.

Use cases are functions that manipulate entities according to the business rules of the app. The
use cases are methods of a class that is instantiated with a storage adapter, allowing us to
decouple them from the Django ORM.

The views are responsible for passing user data to use cases and returning the result of the use
case to the user (or returning an error). No business logic code is stored in Django views or
models, thus decoupling all domain code from the framework, and from any knowledge of the storage
and HTTP layers.

What this means is that the project does not use a lot of Django extras that couple different
layers of the app (eg ModelForm class, which couples HTML forms to models). It also means that as a
developer, you will have a lot more flexibility. [examples]

Inspiration for this project:

* [Hexagonal Architecture](http://alistair.cockburn.us/Hexagonal+architecture)

* [The Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html)

* [The Clean Architecture in Python](https://www.youtube.com/watch?v=DJtef410XaM)
