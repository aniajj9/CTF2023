FROM debian:bullseye

RUN set -ex \
    && apt-get -o Acquire::GzipIndexes=false update \
    && apt-get install -y --no-install-recommends apt-show-versions gdebi-core wget ca-certificates \
    && wget -O /tmp/webmin.deb https://sourceforge.net/projects/webadmin/files/webmin/1.910/webmin_1.910_all.deb/download \
    && gdebi -n /tmp/webmin.deb \
    && apt-get purge -y --auto-remove gdebi-core \
    && rm -rf /var/lib/apt/lists/* /tmp/webmin.deb

ADD entrypoint.sh /
EXPOSE 10000

RUN set -ex \
    && sed -i 's/passwd_mode=.*/passwd_mode=2/' /etc/webmin/miniserv.conf \
    && chmod +x /entrypoint.sh \
    && echo 'root:SuperDuperSecurePassword' | chpasswd

ENTRYPOINT ["/entrypoint.sh"]