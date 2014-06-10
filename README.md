witchform
=========

Experiments with declarative workflows through a set of forms.


Quick Summary
-------------

Django's form wizard is far too complicated if the flow through a set of forms depends on answers within the forms. 
 
Witchform doesn't use procedural statements (if, else etc.) to traverse through a set of forms and determine which are relevant to the end user. Instead, each form declares properties which other forms can read. Upon loading a set of forms (a 'cauldron') the relationships between forms can be built based on these dependancies.

This project uses Django to demonstrate the idea via 8 forms which will help you choose a suitable pet.
