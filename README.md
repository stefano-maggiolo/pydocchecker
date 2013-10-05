Pydoc Checker
=============

A Python module validating the arguments of methods and functions.


What is it?
-----------

Pydoc Checker modifies the functions and methods in your code adding a
run-time validation of the type of the arguments, of the return value,
and of the exceptions raised. The required types must be described in
the pydoc of the method.


What should I do?
-----------------

You should record the expected types in the pydoc of the function or
method, like in this example.

```python
def retrieve(hash_table, key, default_value=None):
    """Retrieve the element associated to key from hash_table.

    hash_table (HashTable): the hash table in which to search.
    key (unicode): the key to search.
    default_value (HashTableValue|None): if key is not in hash_table,
        and default_value is not None, default_value is returned.

    return (HashTableValue|None): the object associated to key.

    raise (KeyError): if key is not in hash_table and no default_value
        is provided.

    """
    <implementation>
```

If Pydoc Checker was called after the definition of this function,
then right before each call to ```retrieve```, some code will be
executed to ensure that all passed values are of the correct
type. Also, after ```retrieve``` was executed, Pydoc Checker will
ensure that the return value is of the correct type, or, if the
function raised, that the exception was expected.

In addition to this, it also checks the default argument values, like
```None``` for ```default_value``` in the example.

To enable Pydoc Checker, you just need to call ```check_all(pkgs)```
at the beginning of your program, where pkgs is a list of the
(top-level) packages you want to check. Subpackages will be checked
too.

```python
#!/usr/bin/env python

"""Entry point of the program."""

from myprogram import run

if __name__ == "__main__":
    import pydocchecker
    pydocchecker.check_all(["my_package"])
    main()
```

Finally, you should use only new-style classes (that is, a class
should derive, directly or indirectly, from ```object```.


It sounds like a lot of work
----------------------------

Nobody said it was easy to write maintainable code that can be
understand by a new member of a team. Having proper pydoc strings
allows to have this nice check, but, if you do not do it already, the
real advantage is giving you incentives to write proper code
documentation.


If I wanted a typed language, I would have used Java
----------------------------------------------------

If you pass the wrong object to a function, it is wrong both in Java
and in Python.

Python is awesome for fast, short scripts. It is great for small
project. It starts to have some drawbacks for medium to large
project. Having additional confidence on such a Python project is
never a wrong idea.


Will it slow down my program?
-----------------------------

Depending on your style of programming, it could add a noticeable
overhead. I suggest to run Pydoc Checker during manual and automated
testing.


How do I write a type annotation?
---------------------------------

The recognizable type annotations respect the following grammar.

```
<type> := [a-zA-Z0-9_]+ |
          <list> |
          <tuple> |
          <set> |
          <dict> |
          <type>|<type>
<list> := [<type>]
<tuple> := (<type>, <type>, ..., <type>)
<set> := (<type>)
<dict> := {<type>: <type>} |
          {<id>: <type>, ..., <id>: <type>}
```

There are two kinds of dictionaries: if a single pair (key, value) is
given, then it is assumed to be an "homogeneous" dict, that is, all
keys are of the same type and all values are of the same type; if
there are zero, two, or more pairs, then it is assumed to be a
string-indexes associative array, and the type is satisfied if all
keys are present in the actual dictionary, and the type of the values
match.


Where do I see my errors?
-------------------------

Errors (that is, passing or returning the wrong type, or an unexpected
exception) are outputted using the ```warn``` function of the
```warnings``` module.

If you choose to see debug information on the internals of Pydoc
Checker, then the logs are printed using ```q```, so by default are
streamed to ```/tmp/q```.


Is it configurable?
-------------------

```check_all``` accepts these optional arguments.

- ```none_always_valid``` (boolean, default False): whether to
  consider ```None``` an instance of any type, instead then just of
  object and ```NoneType```.  In the latter case, use an annotation
  like ```<type>|None``` to accept also None values.

- ```complain_for_missing_pydoc``` (boolean, default False): whether
  to log a warning also for missing pydocs, or missing type
  descriptions.

- ```debug``` (integer, default 0): the higher, the more log lines
  will be printed in ```/tmp/q```; valid values are between 0 and 5.


How do I install it?
----------------

To install Pydoc Checker, just clone the repository or download a
tarball, and run the following.

```bash
sudo ./setup.py install
```


TODOs
-----

- Fallback on the pydoc of the parent class' method if the child does
  not have a pydoc or does not describe some argument.

- Unambiguous syntax for the two types of dictionaries.

- Better checking when two classes have the same name. At the moment,
  passing an object of any of the two types is accepted, but there
  should be some heuristic using the imports of the specific module.

- Check also inner functions.

- Check for exceptions, making sure that a warning is issued only if
  at least one type annotation is found in the pydoc.

- If a type is not found, and there is not a default argument for that
  type, postpone the error to when the function is called, as it might
  just be that the type is not imported (and the function is never
  called).
