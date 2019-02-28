# Use the `golang` image to build a statically linked binary.
# https://blog.codeship.com/building-minimal-docker-containers-for-go-applications/
#
# Tested with:
# golang@sha256:4826b5c314a498142c7291ad835ab6be1bf02f7813d6932d01f1f0f1383cdda1
FROM golang as gobin

# Clone the improbable-eng/grpc-web repo.
WORKDIR /go/src/github.com/improbable-eng
RUN git clone https://github.com/improbable-eng/grpc-web.git

# Use `dep` to ensure the correct versions of vendor dependencies are used.
# See: https://github.com/improbable-eng/grpc-web/issues/174
WORKDIR /go/src/github.com/improbable-eng/grpc-web
RUN go get github.com/golang/dep/cmd/dep
RUN dep ensure

# Build a static binary for `grpcwebproxy`.
WORKDIR /go/src/github.com/improbable-eng/grpc-web/go/grpcwebproxy
ENV CGO_ENABLED='0' GOOS='linux'
RUN go install

# Use the `alpine` image to get `ca-certificates`.
#
# Tested with:
# alpine@sha256:7df6db5aa61ae9480f52f0b3a06a140ab98d427f86d8d5de0bedab9b8df6b1c0
FROM alpine as certs
RUN apk update
RUN apk add ca-certificates

# Build the image from the `scratch` (empty) container by copying the binary
# and SSL certificates into an approapriate location.
FROM scratch
COPY --from=gobin ["/go/bin/grpcwebproxy", "/bin/"]
COPY --from=gobin ["/go/src/github.com/improbable-eng/grpc-web/misc/localhost.*", "/misc/"]
COPY --from=certs ["/etc/ssl/*", "/etc/ssl/"]

# Start the `grpcwebproxy` binary as the main process.
ENTRYPOINT ["/bin/grpcwebproxy"]

# Provide default arguments for `grpcwebproxy`.  These will normally be
# overridden when running the container.  Using ENV for HOST and PORT would
# be better here, but ENV variables don't expand without a shell.
#
# See: https://github.com/moby/moby/issues/5509#issuecomment-42173047
#
# Instead, `dev.localdomain` is used for the host.  This can be set when
# running the container by using the argument:
#
#    `--add-host dev.localdomain:192.0.2.1
#
# Replace 192.0.2.1 with the IP address of the host.
#
# Port 50051 is used because it's the most common port used in the GRPC
# quickstart examples.
CMD ["--server_tls_cert_file=/misc/localhost.crt", \
     "--server_tls_key_file=/misc/localhost.key", \
     "--backend_addr=dev.localdomain:50051", \
     "--backend_tls_noverify"]
