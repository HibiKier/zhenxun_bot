FROM python:3.11-slim-bookworm

EXPOSE 8080

WORKDIR /app/zhenxun

COPY . /app/zhenxun

RUN pip install poetry -i https://mirrors.aliyun.com/pypi/simple/

RUN poetry install

VOLUME /app/zhenxun/data /app/zhenxun/data

VOLUME /app/zhenxun/resources /app/zhenxun/resources

RUN poetry run playwright install --with-deps chromium

CMD ["poetry", "run", "python", "bot.py"]