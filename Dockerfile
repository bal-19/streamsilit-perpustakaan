FROM python:3.10.14-bookworm

WORKDIR /app

RUN ln -fs /usr/share/zoneinfo/Asia/Jakarta /etc/localtime \
    && echo "Asia/Jakarta" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

COPY . .

RUN python -m venv venv

RUN venv/bin/pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD [ "venv/bin/streamlit", "run", "search.py", "--server.port=8501", "--server.enableCORS=false" ]