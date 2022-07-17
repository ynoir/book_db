#!/bin/bash

python3 manage.py dumpdata books --indent=1 > books.json
