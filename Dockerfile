FROM wpscanteam/wpscan
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]