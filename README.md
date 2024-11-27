This initial release contains a minimal integration of [LLaMa-Mesh](https://github.com/nv-tlabs/LLaMA-Mesh) in Blender.

# Installation

Go to the [Latest Release](https://github.com/huggingface/meshgen/releases/latest) page for a download link and installation instructions.

# Setup
- In `MeshGen` addon preferences, click `Download Required Models`
- If set up correctly, addon preferences should display the message `Ready to generate. Press 'N' -> MeshGen to get started.'

# Usage

- Press `N` -> `MeshGen`
- Click `Load Generator` (this will take a while)
- Enter a prompt, for example: `Create a 3D obj file using the following description: a desk`
- Click `Generate Mesh`

# Troubleshooting

- Find errors in the console:
  - Windows: In Blender, go to `Window` -> `Toggle System Console`
  - Mac/Linux: Launch Blender from the terminal
- Report errors in [Issues](https://github.com/huggingface/meshgen/issues)
