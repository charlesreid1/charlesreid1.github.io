Title: A Singleton Config Class in Python
Date: 2020-03-10 22:00
Category: Python
Tags: python, programming, patterns, design patterns, registry, computer science
Status: draft

singleton Config class

behavior - constructor takes an argument, then can use class to refer to it

principle - define one config file location, and be done with it

environment variables, private variables, directly stored values and parsed values

separation of concerns - returning sections of the config to components, let them handle their own option parsing

e.g., don't want new doctypes to have to change code in 10 places

