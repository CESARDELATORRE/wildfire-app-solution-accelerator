$tags="1.0"
$imageName="mecsolutionaccelerator/rtsp-video-streamer:${tags}"

docker build --tag=${imageName} --file=./Dockerfiles/rtsp .
