Title: First Post of the Fall, Part 2: Flaskadillo
Date: 2018-10-30 16:00
Updated: 2018-10-30 16:00
Category: Python
Tags: Github, Software, Python, Flask

## Flask + ILLO = Flaskadillo

On October 15, 2018, I had the opportunity to 
offer an in-lab learning opportunity (ILLO) at the 
[Lab for Data Intensive Biology](http://ivory.idyll.org/lab/).
The ILLO focused on Flask, a useful Python library
for creating and running web servers. This
library is useful because it has a very low
learning curve, but also has the complexity to
handle complicated, real-world projects.

As a part of this in-lab learning opportunity, 
I created repository with five simple Flask examples
to highlight five useful capabilities of Flask.

The repository is called flaskadillo and it is 
available on [git.charlesreid1.com](https://git.charlesreid1.com/charlesreid1/flaskadillo/)
or on [github.com](https://github.com/charlesreid1/flaskadillo).

The five capabilities covered by the examples in 
flaskadillo are listed below:

1. hello - hello world flask server

2. api - a simple API server

3. jinja - a simple Flask server that makes use of Jinja templates

4. package - a simple demonstration of how to package flask apps

5. tests - a simple demonstration of how to write Flask tests

## Example 1: Hello World

We'll just cover example 1 here, but similar materials
are available for all five examples.

Example 1 consists of a simple flask app, `simple.py`:

```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
```

The [hello](https://git.charlesreid1.com/charlesreid1/flaskadillo/src/branch/master/hello)
directory of the flaskadillo repo covers how to 
install the necessary packages and run the Flask
application.

There is also a unit test, `test_simple.py`, which demonstrates
how to write tests for Flask applications. To run the unit
test, run:

```
pytest
```

## More Information

For instructions on each of the 5 examples, 
visit each of the 5 directories in the 
[flaskadillo repository](https://github.com/charlesreid1/flaskadillo).

### Why flaskadillo?

Because armadillo.

### Why armadillo?

The word armadillo means "little armoured one" in Spanish.

Armadillos are related to anteaters and sloths (all are in the Xenartha superorder).

The Aztecs called them turtle-rabbits.

