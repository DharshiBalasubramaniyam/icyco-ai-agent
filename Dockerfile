FROM python:3.11-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN ls

# Create a new user with UID 10016
RUN addgroup --gid 10016 choreo && \
    adduser  --disabled-password  --no-create-home --uid 10016 --ingroup choreo choreouser

USER 10016
EXPOSE 5000
CMD [ "flask", "run", "--host=0.0.0.0"]