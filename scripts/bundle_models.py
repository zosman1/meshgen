import json
import os
import site
import sys


def load_dependencies():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    dependencies_dir = os.path.abspath(os.path.join(script_dir, "..", ".python_dependencies"))
    if dependencies_dir not in sys.path:
        sys.path.append(dependencies_dir)
    site.addsitedir(dependencies_dir)


def bundle_models():
    load_dependencies()

    from huggingface_hub import hf_hub_download

    script_dir = os.path.dirname(os.path.realpath(__file__))
    models_path = os.path.abspath(os.path.join(script_dir, "..", ".models"))
    manifest_path = os.path.join(models_path, "manifest.json")
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    required_models = manifest["required_models"]
    for model in required_models:
        hf_hub_download(model["repo_id"], filename=model["filename"], local_dir=models_path)


if __name__ == "__main__":
    bundle_models()
