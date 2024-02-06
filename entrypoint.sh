#!/bin/sh
# entrypoint.sh

# Run migrations
python3 manage.py migrate

# Then run the main container command (passed to us as arguments)
exec "$@"
