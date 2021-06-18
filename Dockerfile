FROM wpscanteam/wpscan
COPY entrypoint.sh /entrypoint.sh
USER root
RUN apk add curl
ENTRYPOINT ["/entrypoint.sh"]