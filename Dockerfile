FROM python:3.9-slim

WORKDIR /src/app

COPY . ./

RUN pip3 install -r requirements.txt

EXPOSE 8502

ENTRYPOINT ["streamlit", "run", "lit.py", "--server.port=8502", "--server.address=0.0.0.0"]