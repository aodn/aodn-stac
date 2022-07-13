.PHONY: run
up:
	docker-compose up

down:
	docker-compose stop

migrate:
	docker-compose exec app-pgstac \
		/code/migrate.sh

# This is running locally, because Alex is lazy!
add-collection:
	pypgstac --dsn postgres://username:password@localhost:5432/postgis \
		load collections 4402cb50-e20a-44ee-93e6-4728259250d2_stac-collection.json

# This is running locally too
add-item:
	pypgstac --dsn postgres://username:password@localhost:5432/postgis \
		load items IMOS_Argo_TPS-20000101T000000_FV01_yearly-aggregation-South_Pacific_C-20130501T180000Z_stac-item.json
