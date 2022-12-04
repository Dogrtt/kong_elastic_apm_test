FROM golang:alpine as build

WORKDIR /app

COPY ./apm_plugin/go.mod ./
COPY ./apm_plugin/go.sum ./
RUN go mod download

COPY ./apm_plugin/main.go ./

RUN CGO_ENABLED=0 go build -o /elastic-apm

FROM kong:3.0.1-alpine

USER root

COPY ./kong.yml /etc/kong/kong.otel.yml

COPY --from=build /elastic-apm /usr/local/bin/

USER kong
