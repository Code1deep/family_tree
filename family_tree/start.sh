#!/bin/bash
gunicorn family_tree.wsgi:app
