#!/usr/bin/env bash

set -e

pypgstac migrate \
		--dsn "postgres://$POSTGRES_USER:$POSTGRES_PASS@$POSTGRES_HOST_READER:5432/$POSTGRES_DBNAME"
