docker build -t cicd_pipeline_products
docker images
docker run -p 5000:5000 cicd_pipeline_products
http://localhost:5000

