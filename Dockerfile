FROM python:3.11.4

RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

COPY /backend/Python_Files/Main_Scripts /app/backend/
WORKDIR /app/backend

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]


#Envrionment Variables to be set:
#GPT_API_KEY
#FRONTEND_HOST --> http://localhost:3000 
#REACT_APP_BACKEND_HOST --> http://localhost:5000