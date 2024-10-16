import json
import os
import sys
import traceback
from threading import Lock


from ..operators.install_dependencies import load_dependencies
from ..utils import absolute_path


class Generator:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Generator, cls).__new__(cls)
                    cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if self.initialized:
            return
        self.required_models = ["Zhengyi/LLaMa-Mesh"]
        self.downloaded_models = []
        self.dependencies_installed = False
        self.dependencies_loaded = False
        self.device = "cpu"
        self.tokenizer = None
        self.pipeline = None
        self.terminators = []
        self.initialized = True

    def _process_model_dir(self, dir_name):
        from huggingface_hub.constants import HF_HUB_CACHE

        model_dir = os.path.join(HF_HUB_CACHE, dir_name)
        if not os.path.isdir(model_dir):
            return None
        model_name = os.path.basename(model_dir).replace("models--", "").replace("--", "/")
        return model_name

    def _list_downloaded_models(self):
        from huggingface_hub.constants import HF_HUB_CACHE

        models = []

        if not os.path.exists(HF_HUB_CACHE):
            self.downloaded_models = models
            return

        for dir_name in os.listdir(HF_HUB_CACHE):
            model_name = self._process_model_dir(dir_name)
            if model_name:
                models.append(model_name)

        self.downloaded_models = models
    
    def _ensure_dependencies(self):
        if not self.dependencies_installed:
            self.dependencies_installed = len(os.listdir(absolute_path(".python_dependencies"))) > 2

        if self.dependencies_installed and not self.dependencies_loaded:
            load_dependencies()
            self.dependencies_loaded = True

    def has_dependencies(self):
        self._ensure_dependencies()
        return self.dependencies_installed
    
    def has_required_models(self):
        self._list_downloaded_models()
        return all(model in self.downloaded_models for model in self.required_models)
    
    def is_generator_loaded(self):
        return self.pipeline is not None

    def load_generator(self):
        print("Loading generator...")

        self._ensure_dependencies()

        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer

            if torch.cuda.is_available():
                self.device = "cuda"
                print("Using CUDA")
            elif torch.backends.mps.is_available():
                self.device = "mps"
                print("Using MPS")
            else:
                print("Running on CPU")

            model_path = "Zhengyi/LLaMa-Mesh"
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.pipeline = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.bfloat16,
            ).to(self.device)
            self.terminators = [
                self.tokenizer.eos_token_id,
                self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]

            print("Finished loading generator.")

        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                print("Failed to load generator: Insufficient memory.", file=sys.stderr)
            else:
                print(f"Failed to load generator: {e}", file=sys.stderr)
            traceback.print_exc()

        except Exception as e:
            print(f"Failed to load generator: {e}", file=sys.stderr)
            traceback.print_exc()

    @classmethod
    def instance(cls):
        return cls()
