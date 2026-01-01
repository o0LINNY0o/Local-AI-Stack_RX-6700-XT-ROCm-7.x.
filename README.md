This is a comprehensive `README.md` template designed for your GitHub repository. It organizes your build instructions, configuration files, and the hardware-specific tweaks you discovered to make this stack work on the **RX 6700 XT**.

---

# AMD Local AI Stack: RX 6700 XT + ROCm 7.x

A high-performance, fully local AI ecosystem optimized for AMD Radeon GPUs (specifically the **RX 6700 XT / gfx1031**). This setup integrates LLMs, Vision models, Text-to-Speech (TTS), Speech-to-Text (STT), and Document Parsing into a single, unified interface via **Open WebUI**.

## 🚀 Performance Snapshot
*   **GPU:** AMD Radeon RX 6700 XT (12GB VRAM)
*   **CPU:** Ryzen 5 5600X / 16GB RAM
*   **Metric:** ~22-25 t/s on `Ministral-3-14B-Instruct-Q5_K_XL` (16k context)

---

## 🛠️ System Components

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Interface** | [Open WebUI](https://github.com/open-webui/open-webui) | Docker-based frontend for all services. |
| **Inference** | [llama.cpp](https://github.com/ggml-org/llama.cpp) | Custom built for ROCm 7.2 & gfx1031. |
| **Model Swap** | [llama-swap](https://github.com/mostlygeek/llama-swap) | Dynamic model loading/unloading for VRAM efficiency. |
| **TTS** | [Kokoro-ONNX](https://github.com/thewh1teagle/kokoro-onnx) | High-speed, high-quality local text-to-speech. |
| **STT** | [Whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Vulkan-accelerated transcription with VAD. |
| **Embedding** | Qwen3-Embedding | Local vector generation for RAG. |
| **Parsing** | [Docling](https://github.com/DS4SD/docling) | Advanced document-to-markdown conversion. |

---

## 🏗️ Installation & Build

### 1. ROCm Environment (Windows)
This setup uses a hybrid of ROCm 7.x and custom libraries for the gfx1031 architecture.
*   **ROCm Build:** [guinmoon/rocm7_builds](https://github.com/guinmoon/rocm7_builds)
*   **Required Libraries:** [ROCmLibs-for-gfx1103-AMD780M-APU](https://github.com/likelovewant/ROCmLibs-for-gfx1103-AMD780M-APU) (Provides compatible ROCBlas).

### 2. Building llama.cpp
To utilize the RX 6700 XT, you must compile `llama.cpp` manually using Ninja and LLVM.

```batch
:: Set Compiler Paths
set CC=C:\AMD\ROCm\7.2\lib\llvm\bin\clang.exe
set CXX=C:\AMD\ROCm\7.2\lib\llvm\bin\clang++.exe
set HIP_DEVICE_LIB_PATH=C:\AMD\ROCm\7.2\lib\llvm\amdgcn\bitcode

:: Configure with gfx1031 target
cmake -B build -G "Ninja" -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1031 ^
-DCMAKE_C_COMPILER="%CC%" -DCMAKE_CXX_COMPILER="%CXX%" ^
-DCMAKE_PREFIX_PATH="C:\AMD\ROCm\7.2" -DCMAKE_BUILD_TYPE=Release
```

### 3. Python Environment (3.12.x)
Install necessary wheels for ROCm-accelerated PyTorch:
```bash
pip install "rocm-7.2.0.tar.gz" "rocm_sdk_libraries_custom-7.2.0-py3-none-win_amd64.whl"
pip install "torch-2.9.1+rocmsdk20251203-cp312-cp312-win_amd64.whl"
```

---

## ⚙️ Configuration

### Llama-Swap (`config.yaml`)
We use `llama-swap` to handle multiple models (Vision, Instruct, Reasoning) on a single 12GB GPU without crashing.

```yaml
models:
  glm-4.6v:
    cmd: llama-server.exe --model GLM-4.6V-Flash-UD-Q6_K_XL.gguf --mmproj GLM_mmproj-F16.gguf --gpu-layers -1 -c 16384
  ministral-3b:
    cmd: llama-server.exe --model Ministral-3-3B-Instruct-2512-UD-Q6_K_XL.gguf --gpu-layers -1 -c 32768
  llama-3.3-8b:
    cmd: llama-server.exe --model Llama-3.3-8B-Instruct-Q6_K_L.gguf --gpu-layers -1 -c 16384
```

### Automation Scripts
The stack is managed via a master batch file (`START_LlamaROCMCPP.bat`) that launches:
1.  **Llama-Swap** (LLM Port 8000)
2.  **Qwen Embedding** (Port 8181)
3.  **Docling Service** (Document processing)
4.  **Whisper STT** (Vulkan backend)
5.  **Kokoro TTS** (Python ONNX backend)

---

## 🐳 Docker Deployment (Open WebUI)

To keep the UI updated while preserving your local data:
```bash
# Update and Restart
docker compose pull
docker compose up -d
# Cleanup
docker image prune -f
```

---

## 💡 Tips & Troubleshooting

*   **VRAM Management:** Using `q8_0` for K/V cache (as seen in `config.yaml`) is essential for maintaining 16k+ context windows on a 12GB card.
*   **Vision Models:** Ensure the `--mmproj` flag is correctly pointed to the project file in `llama-swap` configurations to enable image analysis.
*   **STT Modification:** To make Whisper.cpp compatible with OpenAI-style endpoints, modify `server.cpp` changing `/inference` to `/v1/audio/transcriptions` before compiling.
*   **Pathing:** This configuration assumes a root directory of `C:\llamaROCM`.

---

## 🔗 Credits
*   **ROCm Builds:** [guinmoon](https://github.com/guinmoon)
*   **llama.cpp:** [ggml-org](https://github.com/ggml-org/llama.cpp)
*   **llama-swap:** [mostlygeek](https://github.com/mostlygeek/llama-swap)
*   **Kokoro-ONNX:** [thewh1teagle](https://github.com/thewh1teagle/kokoro-onnx)
