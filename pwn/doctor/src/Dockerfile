FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y socat gcc-multilib

COPY flag /
COPY baby_bof /


EXPOSE 1337
CMD ["socat", "-T60", "TCP-LISTEN:1337,reuseaddr,fork,su=root", "EXEC:/baby_bof"]