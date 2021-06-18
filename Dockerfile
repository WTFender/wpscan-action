FROM wpscanteam/wpscan
COPY entrypoint.sh /entrypoint.sh
COPY example.json /example.json
COPY webhook.py /webhook.py
USER root
RUN apk add curl python3
RUN pip install requests
ENTRYPOINT ["/entrypoint.sh"]