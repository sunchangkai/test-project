FROM ghcr.io/appleboy/drone-ssh:1.7.3

RUN apt-get update && \
    apt-get install -y dotnet-sdk-3.1

ENV PATH="${PATH}:/usr/share/dotnet"

COPY entrypoint.sh /bin/entrypoint.sh

ENTRYPOINT ["/bin/entrypoint.sh"]
