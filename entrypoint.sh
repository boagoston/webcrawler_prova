#!/bin/sh
if [ "$1" = "bash" ] || [ "$1" = "sh" ]; then
    exec "$@"
else
    cd /app/webcrawler_servimed/webcrawler_servimed
    exec python3 /app/webcrawler_servimed/webcrawler_servimed/busca_servimed.py "$@"
fi