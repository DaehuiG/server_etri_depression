FROM pytorch/pytorch:2.7.0-cuda12.6-cudnn9-runtime

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

RUN apt-get update && apt-get install -y \
	supervisor \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install vllm

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY fastapi_app/ ./fastapi_app/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN mkdir /models

EXPOSE 8000
EXPOSE 8001

CMD ["/usr/bin/supervisord"]
