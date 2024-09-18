FROM ubuntu:20.04 AS builder

RUN apt-get update && apt-get install -y gcc make

WORKDIR /build

COPY src/* ./

RUN make

FROM ghcr.io/svuctf/base-v2/xinetd:latest

COPY init.sh /init.sh
COPY xinetd.conf /etc/xinetd.conf

# Set up permissions and base directories
RUN chmod +x /init.sh && \
    chown -R ctf:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    mkdir -p /home/ctf/lib64 && \
    mkdir -p /home/ctf/dev && \
    mkdir -p /home/ctf/bin && \
    mkdir -p /home/ctf/lib/x86_64-linux-gnu && \
    mkdir -p /home/ctf/lib32

# Set up device nodes
RUN mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

# Copy necessary libraries and binaries
RUN cp -R /lib* /home/ctf && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin && \
    cp /bin/base64 /home/ctf/bin

# Copy challenge files
COPY --from=builder /lib/x86_64-linux-gnu/libc.so.6 /home/ctf/lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2 /home/ctf/lib64/
COPY --from=builder --chmod=500 /build/canary /home/ctf/canary

CMD ["xinetd", "-dontfork"]
