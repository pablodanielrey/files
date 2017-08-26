sudo docker run -ti -d --name files -v $(pwd)/src:/src -p 5010:5000 -p 5011:5001 -p 5012:5002 -p 5013:5003 --env-file /home/pablo/gitlab/fce/produccion/files files
