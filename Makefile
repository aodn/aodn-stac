.PHONY: run
up:
	docker-compose up

down:
	docker-compose stop

migrate:
	docker-compose exec app-pgstac \
		/code/migrate.sh

# This is running locally, because Alex is lazy!
add-collections:
	pypgstac --dsn postgres://username:password@localhost:5432/postgis load collections documents/*.json

# This is running locally too
add-items:
	cat documents/IMOS_Argo_South_Pacific-items/*_stac-item.json | jq -c > temp.json \
	&& pypgstac --dsn postgres://username:password@database:5432/postgis load items temp.json --method ignore \
	&& rm temp.json
