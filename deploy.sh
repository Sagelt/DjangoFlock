#!/bin/bash

# git commit
git push heroku master
heroku run python DjangoFlock/manage.py migrate events
heroku scale web=1
