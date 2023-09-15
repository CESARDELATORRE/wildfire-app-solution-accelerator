# rtsp-video-streamer-container
A container in Python that streams any video through a RTSP uri. Can be tested with VLC media player.

# Basic Procedure:

## 1. Copy the video you want to stream as RTSP

Copy the video you want to stream as RTSP within the folder **"src"** and name your video as **"video.mp4"** (Possibly replacing the existing "video.mp4")

## 2. Build the Docker image with:

From Windows PowerShell:

```powershell
./build-streamer-image.ps1
```

## 3. Run the container with:

From Windows PowerShell:

```powershell
./run-streamer-local.ps1
```

You will see the following output:

```powershell
> .\run-streamer-local.ps1

Environment: server_ip 127.0.0.1, server_port 8554, uri video
Example full URI: rtsp://127.0.0.1:8554/video
```

Take note or copy the RTSP url above.
You can use the local IP, or localhost or your real network adapter IP.

```
rtsp://127.0.0.1:8554/video

rtsp://localhost:8554/video

rtsp://my_IP:8554/video
```

## 5. Test the RTSP streaming with 

If you don't have it installed, install "VLC media player" from:

A. Microsoft Windows Apps Store:
https://apps.microsoft.com/store/detail/vlc/XPDM1ZW6815MQM

B. Videolan.org
https://www.videolan.org/vlc/index.wa.html


Run VLC media player and open the RTSP url and watch the video.






