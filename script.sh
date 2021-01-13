#!/bin/bash
sudo sysctl -w vm.max_map_count=262144
mkdir -p ./docker-persistence/es/data
sudo chmod 777 ./docker-persistence/es/data

docker-compose up -d
docker cp ./templates/universal-recommender/engine.json `docker ps -aqf "name=harness-cli"`:/data/engine.json
docker-compose exec harness-cli bash

#
cd /data/universal-recommender
hctl add engine.json

#
python ./samples/import_handmade.py --file ./samples/sample-handmade-data.txt

#
hctl train 1


#
docker-compose down -v
sudo rm -rf docker-persistence
