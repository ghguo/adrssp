Clone the code (Dockerfile and app folder) to a directory. In the directory, run
docker build -t ssp .

Then, run
docker run --name adrssp -d -v $PWD/app:/app -p 80:80 ssp app.py
  
