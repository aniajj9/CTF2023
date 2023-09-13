# Challenges for Bankdata CTF 2023
This repository contains the challenges for the internal Bankdata CTF in 2023.

## Challenge Format
To contribute, follow [the format described here](https://github.com/eskildsen/ctfd-cli). By following the format, it is possible to use the referred tool, to automatically import the challenges into an existing CTFd instance.

Flag format is `CTF{something_g0es_h4r4}`.

## Infrastructure Setup
There is generally two types of challenges: challenges with a online server and the ones without, which typically only contains downloadable files. 

### Tuning CTFd - Caching
The downloadable files will be uploaded to CTFd, if using the [tool described above](##_Challenge_Format). For larger files and to optimize deployment, these files should either be catched by a front-end proxy or uploaded to a cloud storage somewhere else. CTFd is not very good at handling large load.

For smaller events with < 50 participants, CTFd should be strong enough to handle the file upload traffic as well.

### Tuning CTFd - Configuration
I recommend just running CTFd using the provided Dockerfiles, barebone is fine as well, but setup is a bit more cubersome. No matter the deployment method, ensure to set the `WORKERS=(2 x $num_cores) + 1`. I do not recommend deploying CTFd with less than 4 CPU cores. CTFd is generally limited by the CPU - not the memory.

You also want to configure the `SQLALCHEMY_MAX_OVERFLOW=50` which is the amount of database connections it should allow to pool. Somewhere between 30 and 100 should do it.

For extra performance, consider running the database server on a separate machine than the CTFd instance - this also allows running multiple instances of CTFd in parallel, thereby allowing to handle much larger loads.

### Where to run Challenges
As CTFd can consume quite a lot of resources, you generally don't want to run CTFd on the same server, as you are running your challenges on. Challenges should ideally be distributed across several servers.

The only requirement for the server running the challenges is that it has `docker` installed, and some kind of network proxy - recommendation is `nginx`. In general we have always been running the challenges on Linux servers, but Windows works as well.

### How to run Challenges
As long as the challenges follows the format above, then any challenge requiring a backend will be able to start out using the following command:
```
$ docker-compose up --build -d
```

The `-d` parameter backgrounds the execution, whereas `--build` discards any cache, which is useful if you make any manual changes. The command needs to be executed in the directory of the challenge - e.g. next to the file `docker-compose.yml`. All challenges with a backend will have this file.

In general, the `docker-compose.yml` file lists one or more *containers*, which should be started. In the example below we are running the two containers 'ingress' and 'web'. As 'web' does not have any ports exposed, then you will only be able to connect to the 'ingress'. 

```yaml
services:
  ingress:
    image: nginx:alpine
    restart: always
    ports: 
      - 127.0.0.1:5007:80

  calculator-service:
    build: src
    restart: always
```

In the example 'ingress' binds to port '127.0.0.1:5007' - this is not exposed externally. Thus, from the server you should be able to run the command successfully and see some response from the webserver:
```
$ curl 127.0.0.1:5007
```

This challenge can then be placed behind a proxy running on the host, e.g. `nginx` which then proxies requests to the docker container. An example nginx-configuration could be as below, placed in /etc/nginx/sites-enabled/calculator.conf:
```
server {
    listen 443 ssl;
    server_name calculator.wep.dk;
    ssl_certificate /etc/letsencrypt/live/calculator.wep.dk/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/calculator.wep.dk/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://127.0.0.1:5007;
        proxy_redirect off;
    }
}

server {
    listen 80;
    server_name calculator.wep.dk;
    return 301 https://$host$request_uri;
}
```

Here we used Let's Encrypt/certbot to mange SSL. In general I recommend deploying challenges under HTTPS, but majority should work fine if you choose to just expose the port `5007` directly. If you do not want to put a TLS-proxy in front of a challenge, then simply change the `docker-compose.yml` file:

```yaml
    ports: 
      - 0.0.0.0:5007:80
```


## Docker Cheatsheet
To list running containers:
```
$ docker ps
```

To bring up a challenge, make sure to be in the same folder as the `docker-compose.yml` file. Then run the command:
```
$ docker-compose up --build -d
```

To *temporarily* take down a challenge, without destroying data inside the database and then later restarting it:
```
$ docker-compose stop
$ docker-compose up --build -d
```

To take down a challenge *permanently* (and delete any stored state):
```
$ docker-compose down
```

## Docker Network Limitations

Docker assigns IP's from it's configured network range. If you deploy 20+ containers on one host, you might end up in a situation where docker fails to create a new network. Thus, change the network address space of docker by creating the file `/etc/docker/daemon.json` and then **reload docker**:
```
{
   "default-address-pools": [
        {
            "base":"172.17.0.0/12",
            "size":16
        },
        {
            "base":"192.168.0.0/16",
            "size":20
        },
        {
            "base":"10.99.0.0/16",
            "size":24
        }
    ]
}
```