FROM kong:2.0.2-alpine
ENV KONG_DATABASE off
ENV KONG_DECLARATIVE_CONFIG /usr/local/kong/declarative/kong.yml
ENV KONG_PROXY_ACCESS_LOG /dev/stdout
ENV KONG_ADMIN_ACCESS_LOG /dev/stdout
ENV KONG_PROXY_ERROR_LOG /dev/stderr
ENV KONG_ADMIN_ERROR_LOG /dev/stderr
ENV KONG_ADMIN_LISTEN 0.0.0.0:8001
ENV KONG_PROXY_LISTEN 0.0.0.0:80

EXPOSE 80 8001
COPY kong.yml /usr/local/kong/declarative/kong.yml

USER root
