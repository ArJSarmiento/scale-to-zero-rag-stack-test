FROM public.ecr.aws/docker/library/python:3.11.0-slim-bullseye
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

ENV PORT=8000
WORKDIR /var/task

COPY requirements.txt ./
RUN python -m pip install -r requirements.txt

COPY *.py ./
CMD exec uvicorn --port=$PORT main:app
