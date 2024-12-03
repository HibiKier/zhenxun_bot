FROM python:3.11-slim-bookworm

EXPOSE 8080

WORKDIR /app/zhenxun

COPY . /app/zhenxun

RUN apt update && \
    apt upgrade -y && \
    apt install -y --no-install-recommends \
    gcc \
    g++ && \
    apt clean

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

VOLUME /app/zhenxun/data /app/zhenxun/data

VOLUME /app/zhenxun/resources /app/zhenxun/resources

VOLUME /app/zhenxun/.env.dev /app/zhenxun/.env.dev

RUN playwright install --with-deps chromium

CMD ["python", "bot.py"]
