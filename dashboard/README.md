# ProSafeAI China


💡 ** About Us **



## Introduction


## Links



## Development Docker Setup
### run the docker container from the docker image "prosafeai_web:latest":(ONLY FOR ONCE)
docker run -it -p 9913:22 -p 18080:8080 -p 18000:8000 --name prosafeai_web_backend prosafeai_web:latest /bin/bash

### In the docker container: start the SSHD, WEB, Backend services:
/home/start_prosafeai_service.sh

### WEB
http://10.38.49.30:18080/#/index

### Backend
http://10.38.49.30:18000/

### How to connect to Development Docker from VS Code
In VSCode .ssh config, add the following item:
Host ProSafeAi_Docker:
    HostName 10.38.49.30
    User root
    port 9913