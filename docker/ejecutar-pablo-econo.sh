sudo docker run -ti --name files -v $(pwd)/src:/src -p 9000:5000 -p 9001:5001 -p 9002:5002 --env-file /home/pablo/gitlab/fce/pablo/econo/files files
