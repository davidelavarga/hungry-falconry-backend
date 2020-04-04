FROM python:3.8-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Creating working directory
RUN mkdir /code
WORKDIR /code

# Copying requirements
COPY . /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Run the service as a non-root user
USER 1001
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "2", "hungryFalconryRest.wsgi"]