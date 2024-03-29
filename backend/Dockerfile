FROM python:3.11.4

RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

COPY Python_Files/Main_Scripts /app/backend/
WORKDIR /app/backend

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]


#Envrionment Variables to be set:
#GPT_API_KEY
#FRONTEND_HOST --> http://localhost:3000 
#REACT_APP_BACKEND_HOST --> http://localhost:5000

#Docker Commands:
#docker build -t kit-backend .
#docker run -p 5000:5000 -e GPT_API_KEY=your-api-key -e FRONTEND_HOST=http://localhost:3000 kit-backend
#docker kill $(docker ps -q) --> kills all containers