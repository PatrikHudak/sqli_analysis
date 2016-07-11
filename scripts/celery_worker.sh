#!/bin/bash
# Runs celery worker for the analysis engine

celery -A engine worker --loglevel info
