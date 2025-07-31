FROM python:3.11-slim

# set working directory
WORKDIR /app

# copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the application code
COPY . .

# expose the port on which the app will run
EXPOSE 8000

# command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0", "--port", "8000", "--reload"]