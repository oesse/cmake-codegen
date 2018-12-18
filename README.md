# Complex Code Generation with CMake

In this repository a minimal CMake build infrastructure is provided that can
handle a specific complex code generation use case:

1. The content of the input file defines the number and names of the files that
   need to be generated
2. The generated files need to be compiled and should be "linkable"

## How to use the example

The example consists of a code generator, `generator.py`, an interface
definition file, `interfaces.txt` and a main application, `main.cpp` that is
the consumer of the generated library. The generator will provide a header /
implementation for each line in the interface definition file that defines a
class with a single method `name()`. The class name is the content of the
corresponding line in the interface file. Finally, the application uses one of
these generated classes to print the name of that class.

Build and run the example (in a UNIX like environment):
```sh
mkdir build && cd build
cmake .. && make
./main
```

Now, change the `Y.hpp` and `Y` class to something like `Thing.hpp` and `Thing`
respectively in `main.cpp` and add a new line in `interfaces.txt` with the
content
```
Thing
```
Run `make` again (without rerunning `cmake`) and now the application will print:
```
$ ./main
Hello from Thing!
```


## The Why

Now, the main point of this exercise is to have reliable incremental builds. If
the interface definition file changes in a way that will add additional
generated files or removes generated files the dependency graph has to be
regenerated. This should happen automatically without having to remove the
build directory, cache, any file inside the build directory, or changing
anything else than the actual change to the interface definition file. Running
`make` should be sufficient.

_There should never be a need to do a clean build for common changes!_

## The How

A few ingredients are required to make this work in CMake.

First, the generator provides a `--print-dependencies` flag that will just
print all the files that would be generated from a interface file. This
information is used to build a correct dependency graph between the interface
file and the generated files. Second, the interface file itself will be added
to the `CMAKE_CONFIGURE_DEPENDS` property. This will result in CMake
reconfiguring itself, i.e. recreating the dependency graph, whenever the
interface file changes.

With those things in place, you can define a CMake target that will compile the
generated code and setup the include directories for all targets that link
against it.

