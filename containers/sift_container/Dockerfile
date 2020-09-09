FROM debian:buster
RUN apt-get update
RUN apt-get install libc6 libc6-dev -y
COPY run.sh /run.sh
COPY sift /sift
COPY 8MBimg.pgm /8MBimg.pgm
ENTRYPOINT ["sh", "run.sh"]
