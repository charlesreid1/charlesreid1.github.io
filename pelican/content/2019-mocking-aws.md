Title: Mocking AWS in Unit Tests
Date: 2019-09-23 9:00
Category: Python
Tags: python, pytest, tests, aws, mock, mocking

[TOC]

## Overview

This post covers a technique for mocking AWS in unit tests so that you can test functionality that normally
requires API calls and handling responses, by mocking those responses instead of making actual API calls.

## A Simple Example: Mocking API Responses

### The Genuine AWS Call

Let's start with an example of an AWS API call. Here's how our program will be structured:
start with a driver `lister.py` that creates an AWS secrets manager client and defines a 
function to list secrets using the secrets manager client, then a test for it in `test_lister.py`
that mocks the AWS call.

This example is simple and uses just one function, `list_secrets()`,
which returns a JSON response that looks something like this:

```text
{
  "SecretList": [
    {
      "ARN": "arn:aws:secretsmanager:us-east-1:000000000000:secret:prefix/secret1-abc123",
      "Name": "prefix/es_source_ip",
      "LastChangedDate": "2019-09-23 17:29:16.267000-07:00",
      "LastAccessedDate": "2019-09-23 17:00:00-07:00",
      "SecretVersionsToStages": {
        "658c3b41-0806-48b9-b05d-ea7dc2dbf237": [
          "AWSCURRENT"
        ],
        "f37ccfe2-16e0-4305-a250-ef89d2c47ece": [
          "AWSPREVIOUS"
        ]
      }
    },
    {
      "ARN": "arn:aws:secretsmanager:us-east-1:000000000000:secret:prefix/secret2-def789",
      "Name": "prefix/secret2",
      "LastChangedDate": "2019-09-22 17:05:01.431000-07:00",
      "LastAccessedDate": "2019-09-22 17:00:00-07:00",
      "SecretVersionsToStages": {
        "95AE5F8B-34E7-4EDF-A672-9E3AF1A4732E": [
          "AWSCURRENT"
        ],
        "F29E224A-BC03-4780-B64E-EA666B99D952": [
          "AWSPREVIOUS"
        ]
      }
    }
  ]
}
```

Using the secrets manager API:

**`lister.py`**:

```python
import boto3

sm_client = boto3.client('secretsmanager')

def print_secret_names():
    s = sm_client.list_secrets()
    for secret in s['SecretList']:
        if 'Name' in secret and 'LastAccessedDate' in secret:
            print(f"Secret Name: {secret['Name']} (last accessed: {secret['LastAccessedDate']})")

if __name__=="__main__":
    print_secret_names()
```

If we run this file, we'll see a list of secrets in the real secrets manager -
that is, the secrets manager that is linked to the boto credentials in `~/.aws`,
so the secrets we see are the actual secrets in the secret manager:

```text
$ python lister.py
Secret Name: prefix/secret1 (last accessed: 2019-09-23 17:00:00-07:00)
Secret Name: prefix/secret2 (last accessed: 2019-09-23 17:00:00-07:00)
Secret Name: prefix/secret3 (last accessed: 2019-09-23 17:00:00-07:00)
```


### The Mocked AWS Call

It is important to only mock the functionality we need.
We should mock the returned JSON, but only the `Name`
and `LastAccessedDate` fields.

To mock the call to `list_secrets()`, we start by importing
`mock` from `unittest`. Then we import the file that has the
function we want to test. We also import any other modules
we need.

Next, we are mocking a call to a method of an object,
which we can do by creating a context via `with mock.patch()`
(and passing it a string with the name of the object we want
to mock, or patch).

```python
import unittest
from unittest import mock
import lister
import datetime

class TestLister(unittest.TestCase):
    def test_main(self):
        with mock.patch("lister.sm_client") as sm:
            ...
            sm.list_secrets = mock.MagicMock( ... )
            ...
```

Any calls made to `sm_client` in the `lister` module will be mocked
using the `mock.MagicMock` object that we define in the context,
so we craft the response we want before we call the method we 
want to test (which in turn will call `sm_client.list_secrets()`).

The full version of the test looks like this:

**`test_lister.py`**:

```python
import unittest
from unittest import mock
import lister
import datetime

class TestLister(unittest.TestCase):
    def test_main(self):
        with mock.patch("lister.sm_client") as sm:
            return_json = {
                "SecretList": [
                    {
                        "Name": "fakesecret1",
                        "LastAccessedDate": datetime.datetime.now()
                    },
                    {
                        "Name": "fakesecret2",
                        "LastAccessedDate": datetime.datetime.now()
                    }
                ]
            }
            sm.list_secrets = mock.MagicMock(return_value = return_json)
            lister.print_secret_names()

if __name__=="__main__":
    unittest.main()
```

When the test file is run via Python, we see the fake secrets:

```text
$ python test_lister.py
Secret Name: fakesecret1 (last accessed: 2019-09-23 20:31:49.186874)
Secret Name: fakesecret2 (last accessed: 2019-09-23 20:31:49.186880)
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

## Where To Patch: A Common Gotcha

The single most confusing thing about `mock.patch` is that you patch a name
where it is *looked up*, not where it is *defined*. This trips up almost
everyone the first time they reach for `unittest.mock`.

In our example above, `lister.py` does `import boto3` at the top and then binds
a client to a module-level name:

```python
sm_client = boto3.client('secretsmanager')
```

That means the name `sm_client` now lives in the `lister` module's namespace.
The patch target `"lister.sm_client"` works because that is the exact
namespace where our code looks the name up when it runs.

A very natural (but broken) instinct is to try to patch `boto3` itself:

```python
# This looks reasonable, but does nothing useful.
with mock.patch("boto3.client") as bc:
    bc.return_value.list_secrets = mock.MagicMock(return_value=return_json)
    lister.print_secret_names()
```

This patch replaces `boto3.client` in the `boto3` module, but `lister.py`
already called `boto3.client('secretsmanager')` at import time and stored the
result in `lister.sm_client`. That reference is unaffected by the patch, so
the real AWS client is still used and the test either makes a real API call or
fails with a credentials error.

The rule of thumb: find the line in your code that actually uses the name,
then patch it in *that* module's namespace. If `lister.py` did the import
inside the function instead:

```python
def print_secret_names():
    import boto3
    sm_client = boto3.client('secretsmanager')
    ...
```

then `"lister.boto3"` would be the correct patch target, because that is where
`boto3` is looked up at call time.

Once test files grow past a handful of nested `with mock.patch(...)` blocks,
the `mocker` fixture from
[`pytest-mock`](https://pypi.org/project/pytest-mock/) is a cleaner way to
express the same patches without the indentation pyramid.

## When To Reach For `moto` Instead

`unittest.mock` is a good fit when you need to stub out a single call or two,
but it has real limits:

- You hand-craft the response payload, so nothing checks that the shape you
  invented actually matches the real AWS API.
- Multi-step flows (create a secret, then list it, then rotate it) require
  hand-wiring the state changes between mock calls.
- Every new AWS method you touch is another `mock.MagicMock(...)` to author
  and maintain.

For anything beyond a small handful of calls, [`moto`](https://github.com/getmoto/moto)
is usually the better tool. `moto` runs an in-process fake of the AWS services
themselves, so your code calls `boto3` normally and gets back responses whose
shapes match the real API. You can create resources, list them, mutate them,
and delete them the same way you would in production.

Here is the same test written against `moto`:

**`test_lister_moto.py`**:

```python
import boto3
import lister
from moto import mock_secretsmanager

@mock_secretsmanager
def test_print_secret_names(capsys):
    client = boto3.client("secretsmanager", region_name="us-east-1")
    client.create_secret(Name="fakesecret1", SecretString="hunter2")
    client.create_secret(Name="fakesecret2", SecretString="correct horse")

    # Reset lister's cached client so it picks up the moto-patched boto3.
    lister.sm_client = boto3.client("secretsmanager", region_name="us-east-1")

    lister.print_secret_names()

    captured = capsys.readouterr()
    assert "fakesecret1" in captured.out
    assert "fakesecret2" in captured.out
```

A few things to notice:

- The `@mock_secretsmanager` decorator patches `botocore` at the HTTP layer,
  so the "where to patch" gotcha from the previous section does not apply -
  any `boto3` client constructed inside the decorated scope talks to the fake.
- We exercise the real `create_secret` and `list_secrets` code paths. If AWS
  changes a field name, or our code assumes a field that the API does not
  actually return, the test will notice.
- We assert on the *output* of `print_secret_names()` via `capsys`, not just
  that it ran without exceptions.

`moto` also supports a standalone [server mode](https://docs.getmoto.org/en/latest/docs/server_mode.html)
that speaks the AWS wire protocol on a local port, which is useful for
integration tests that span multiple services or non-Python clients.

The rough guideline: reach for `unittest.mock` when you are stubbing a single
call to isolate one unit of code, and reach for `moto` when the test needs the
service to *behave* like AWS across several calls.
