
docker compose logs

docker ps

ctop  # view or run shell from there

docker exec -it <container_id> /bin/bash


# size of images
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# size of containers
docker ps -a --size --format "table {{.Names}}\t{{.Image}}\t{{.Size}}"

#
docker image rm <name>


docker build -f Dockerfile.tst .
