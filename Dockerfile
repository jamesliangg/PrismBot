FROM python:3.9-slim

WORKDIR /src/app

COPY . ./

RUN pip3 install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["streamlit", "run", "lit.py", "--server.port=8080", "--server.address=0.0.0.0"]