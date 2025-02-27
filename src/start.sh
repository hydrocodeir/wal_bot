#!/bin/bash


alembic upgrade head

exec python3 bot.py