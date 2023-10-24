# quick installation

1. build docker image `docker build -t llama2 .`
2. run the container `docker run -p 8888:8888 -e HUGGINGFACEHUB_API_TOKEN=<YOUR_API_TOKEN> llama2`
3. access via `http://localhost:8888/lab`
