#!/bin/sh

python3 download_model.py

if [ -z "$MODEL_LOCAL_PATH" ]; then
  echo "download_model.py execution failed. exiting..."
  exit 1
fi

echo "starting Jupyter Lab on port $JUPYTER_PORT..."
jupyter lab --port=$JUPYTER_PORT --ip=0.0.0.0
