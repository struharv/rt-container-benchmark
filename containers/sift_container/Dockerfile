FROM debian:stretch
RUN apt-get update
RUN apt-get install libc6 libc6-dev -y
COPY sift /sift
ENTRYPOINT ["/sift"]
