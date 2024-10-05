# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.12-alpine AS builder
EXPOSE 8000
WORKDIR /src
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt --no-cache-dir
COPY ./src /src

# ENTRYPOINT ["python3"] 
# CMD ["manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "-k", "uvicorn.workers.UvicornWorker", "treyd.asgi:application"]

# FROM builder as dev-envs
# RUN <<EOF
# apk update
# apk add git
# EOF

# RUN <<EOF
# addgroup -S docker
# adduser -S --shell /bin/bash --ingroup docker vscode
# EOF
# # install Docker tools (cli, buildx, compose)
# COPY --from=gloursdocker/docker / /
# CMD ["manage.py", "runserver", "0.0.0.0:8000"]