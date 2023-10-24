import os
import huggingface_hub

llm_repo: str = os.environ.get("HF_REPO")
llm_file: str = os.environ.get("HF_MODEL_FILE")
llm_local_path: str = huggingface_hub.hf_hub_download(repo_id=llm_repo, filename=llm_file)

os.environ.set("MODEL_LOCAL_PATH", llm_local_path)
