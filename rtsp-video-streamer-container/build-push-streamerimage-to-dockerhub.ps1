$tags="1.0"
$imageName="wildfireaccelerator/rtsp-video-streamer:${tags}"

docker build --tag=${imageName} --file=./Dockerfiles/rtsp .

docker push ${imageName}
