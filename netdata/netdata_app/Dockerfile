FROM debian:stretch

ADD files/git-tag /git-tag
ADD files/build.sh /build.sh
ADD files/run.sh /run.sh
ADD files/apps_groups.conf /etc/netdata/apps_groups.conf
ADD files/dns_query.conf /etc/netdata/go.d/dns_query.conf

RUN chmod +x /build.sh /run.sh && sync && sleep 1 && /build.sh

WORKDIR /
#ENV NETDATA_PORT=19999 SMTP_TLS=on SMTP_STARTTLS=on SMTP_SERVER=smtp.gmail.com SMTP_PORT=587 SMTP_FROM=localhost
EXPOSE 19999
VOLUME /etc/netdata/override
ENTRYPOINT ["/run.sh"]

