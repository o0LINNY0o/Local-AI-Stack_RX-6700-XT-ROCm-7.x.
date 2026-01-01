import io
import soundfile as sf
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from kokoro_onnx import Kokoro

# Initialize App and Model
app = FastAPI(title="Kokoro TTS OpenAI API")

# Load the model once on startup
# Ensure 'kokoro-v1.0.onnx' and 'voices-v1.0.bin' are in the same folder
print("Loading Kokoro model...")
kokoro = Kokoro("kokoro-v1.0.int8.onnx", "voices-v1.0.bin")
#kokoro = Kokoro("kokoro-v1.0.fp16.onnx", "voices-v1.0.bin")
#kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
print("Model loaded!")

# Define the request format expected by OpenWebUI (OpenAI compatible)
class OpenAISpeechRequest(BaseModel):
    model: str = "kokoro"
    input: str
    voice: str = "af_sarah" # Default voice
    speed: float = 1.0
    response_format: str = "mp3" # OpenWebUI sends this, but we will return WAV

@app.post("/v1/audio/speech")
async def generate_speech(request: OpenAISpeechRequest):
    try:
        # 1. Handle Voice Mapping
        # If OpenWebUI sends a default OpenAI voice name, map it to a Kokoro voice
        voice_map = {
            "alloy": "am_adam",
            "echo": "af_bella",
            "fable": "af_sarah",
            "onyx": "bm_lewis",
            "nova": "bf_emma",
            "shimmer": "af_nicole",
        }
        selected_voice = voice_map.get(request.voice, request.voice)

        # 2. Generate Audio
        # Note: 'lang' defaults to en-us in kokoro-onnx if not specified
        samples, sample_rate = kokoro.create(
            request.input, 
            voice=selected_voice, 
            speed=request.speed, 
            lang="en-us"
        )

        # 3. Convert to WAV in-memory
        # We return WAV because it is faster than encoding MP3 in Python without ffmpeg
        buffer = io.BytesIO()
        sf.write(buffer, samples, sample_rate, format='WAV')
        buffer.seek(0)

        # 4. Return Audio
        return Response(content=buffer.read(), media_type="audio/wav")

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run on port 8880 (you can change this)
    uvicorn.run(app, host="0.0.0.0", port=8880)