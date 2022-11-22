FROM wpscanteam/wpscan
WORKDIR /code
USER root
RUN apk add curl python3 py3-pip
COPY src/requirements.txt .
RUN pip3 install -r requirements.txt
COPY src .
ENTRYPOINT [ "/bin/sh" ]
CMD ["entrypoint.sh"]
