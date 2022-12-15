# syntax=docker/dockerfile:1

FROM python:bullseye
ARG BACKEND_TGZ
EXPOSE 5000

# Create the venv and do requirements.txt separately, because they're
# items that change seldom and are time consuming. Splitting it from 
# the tgz installation (which changes frequently) lets docker's caching
# make our build iteration faster.
WORKDIR /app
RUN python -m venv .venv
COPY requirements.txt .
RUN .venv/bin/pip install -r requirements.txt


# ...and now install the actual app
COPY ${BACKEND_TGZ} settings.toml logging*.cfg ./
RUN . .venv/bin/activate && pip install ${BACKEND_TGZ}

CMD [ ".venv/bin/flask", "--app", "backend.app", "--debug", "run", "--host=0.0.0.0" ]