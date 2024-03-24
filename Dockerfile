FROM python:3.11.4

WORKDIR /backend

COPY backend/ /backend/

RUN pip install --no-cache-dir -r requirements.txt

ENV OPENAI_API_KEY=

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]