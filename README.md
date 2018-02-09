get-secret
----------

[![Build Status](https://travis-ci.org/TunedMystic/get-secret.svg?branch=master)](https://travis-ci.org/TunedMystic/get-secret)

Simple tool to fetch secrets for your application.

Installation
---
`pip install get-secret`

Usage
---
```
from get_secret import get
api_key = get('API_KEY', default='xyz-123')
```
