FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y g++ python3 python3-pip git htop

RUN useradd -ms /bin/bash llamauser

WORKDIR /home/llamademo

ENV HUGGINGFACEHUB_API_TOKEN=
ENV HF_REPO=TheBloke/Llama-2-13B-chat-GGML
ENV HF_MODEL_FILE=llama-2-13b-chat.ggmlv3.q5_1.bin
ENV JUPYTER_PORT=8888
ENV DOWNLOAD_LATER=false

COPY download_model.py .
COPY entrypoint.sh .
COPY requirements.txt .
COPY llama-example.ipynb .

RUN chmod +x entrypoint.sh

RUN pip install -r requirements.txt

EXPOSE ${JUPYTER_PORT}

USER llamauser

CMD if [ -n "$HUGGINGFACEHUB_API_TOKEN" ]; then ./entrypoint.sh; else echo "HUGGINGFACEHUB_API_TOKEN is required"; exit 1; fi
