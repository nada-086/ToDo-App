FROM alpine:3.21.3

# Setting Working Directory
WORKDIR /opt

# Get Repo Code
RUN apk add --no-cache git2.48.1 /
&& git clone https://github.com/nada-086/ToDo-App

# Changing Working Directory
WORKDIR /opt/ToDo-App

# Installing Python Requirements
RUN apk add --no-cache python3.13.2 python3-pip python3-venv /
&& apk add --no-cache sqlite3

# Instantiating the Virtual Environment
RUN python3 -m venv venv /
&& source venv/bin/activate /
&& pip install -r requirements.txt

# Setting Environment Variable for Flask App Start
ENV FLASK_APP=main.py

# Initializing Flask Migrate
RUN flask db init /
&& flask db migrate -m "Initial migration" /
&& flask db upgrade

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port:5000"]

EXPOSE 5000