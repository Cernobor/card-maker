#!/usr/bin/env bash

# wait-for-it.sh

set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 3306; do
  >&2 echo "Database is unavailable - sleeping"
  sleep 3
done

>&2 echo "Database is up - executing command"
exec $cmd
