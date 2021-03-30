#!/bin/bash
sudo sysctl -w vm.max_map_count=262144
mkdir -p ./docker-persistence/es/data
sudo chmod 777 ./docker-persistence/es/data

docker-compose up -d
docker cp ./engines/engine.json `docker ps -aqf "name=harness-cli"`:/data/engine.json
docker-compose exec harness-cli bash

#
hctl add /data/engine.json

#
docker-compose logs -f harness

#
python ./samples/import_handmade.py --file ./samples/sample-handmade-data.txt

python ./samples/import_handmade_cz.py --file ./samples/cz-sample-data.txt

#
hctl train 2


#
docker-compose down -v
sudo rm -rf docker-persistence
