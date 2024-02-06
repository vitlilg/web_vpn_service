FROM python:3.11.5

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./

EXPOSE 8000

RUN pip3 install -r requirements.txt

COPY ./ ./

RUN LD_LIBRARY_PATH=/usr/app/libs/64/

RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
