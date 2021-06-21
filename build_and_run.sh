
docker build -t style_transfer -f Dockerfile .

docker rm style_transfer_container 2>&1
docker container run -it -p 5000:5000 --name style_transfer_container style_transfer
