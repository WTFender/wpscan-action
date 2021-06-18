FROM wpscanteam/wpscan
COPY entrypoint.sh /entrypoint.sh
COPY example.json /example.json
USER root
RUN apk add curl
ENTRYPOINT ["/entrypoint.sh"]