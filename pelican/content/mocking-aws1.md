Title: Mocking AWS in Unit Tests
Date: 2019-09-23 9:00
Category: Python
Tags: python, pytest, tests, aws, mock, mocking

## Table of Contents

* [Overview](#overview)
* [A Simple Example: Mocking API Responses](#a-simple-example-mocking-api-responses)
    * [The Genuine AWS Call](#the-genuine-aws-call)
    * [The Mocked AWS Call](#the-mocked-aws-call)

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

class TestMo(unittest.TestCase):
    def test_main(self):
        with mock.patch("mo.sm_client") as sm:
            ...
            sm_client.list_secrets = mock.MagicMock( ... )
            ...
```

Any calls made to `sm_client` in the `mo` module will be mocked
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
