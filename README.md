# Domain Specific Language for Source Code Formatting

## Description

This simple domain specific language enables the user to define a set of rules for formatting source code. The user can define custom structures to be recognized making the DSL suitable for processing code written in a wide range of programming languages. The user can also specify the operators which are present in the target language and specify which operators should have spacing (e.g. binary operators should have spacing while unary operators should not). This enables the formatter to correctly format recognized expressions in the code. If a line of code is not recognized as one of the defined structures or expression types, the entire line will be copied to the output file with no processing except for the indentation.

## Setup

Requirements:
- Python 3

Clone the repository:

```
$ git clone git@github.com:simsimkic/dsl.git
```

Create a pyhton virtual environment and activate it:

```
$ cd dsl
$ python -m venv venv
$ source venv/bin/activate
```

Install the project dependencies:

```
$ pip install -r requirements.txt
```

## Usage

Create a text file with the formatting rules. For example:

```
global:
    block: boundaries: parentheses
           begin : {
           end: }
           indent : 2
    ;
    format :
        MainStructure:
            "If: key_word='if' cond_open='(' cond=Exp cond_close=')' '{' block=Block '}' ;"
        ;
    ;

operators <, >, <=, >=, ==, !=, +, -, *, /:
    spacing : true
    ;

operators ++, -- :
    spacing : false
```

This file defines defines a Java-style `if` structure, with 2 spaces used for indentation and with spacing for Java binary operators. When defining structures, the user has access to the following predefined rules:
- `Exp`       - matches assignments, unary expressions as well as expressions with multiple binary operators.
- `Block`     - matches a block of code which can contain multiple statements or structures.
- `Statement` - matches a structure or expression. If a line of code is not recognized as neither, it will be copied to the output file with the correct indentation but no other processing.

To format a file with these rules, run the file `main.py`:

```
$ python main.py
```

When prompted, enter the path to the file with formatting rules, as well as the input file with the code and the name of the output file.







