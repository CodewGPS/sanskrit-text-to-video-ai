# Text-To-Video AI 🎬

An AI-powered application that transforms text input (specifically Sanskrit text) into engaging video stories with moral lessons. The system uses advanced AI models to generate scripts, create narration audio, produce timed captions, find relevant background videos, and render everything into a polished final video.

## 🌟 Features

- **Sanskrit Text Processing**: Accepts Sanskrit text input and translates it to create meaningful stories
- **AI Story Generation**: Uses OpenAI GPT-4o-mini to generate short, impactful moral stories (<140 words)
- **Text-to-Speech**: Converts generated scripts into high-quality audio narration using OpenAI TTS
- **Timed Captions**: Automatically generates synchronized captions using Whisper timestamped transcription
- **Intelligent Video Search**: Uses AI to generate relevant search queries and finds matching background videos from Pexels
- **Video Rendering**: Combines audio, captions, and background videos into a professional final video
- **Dual Interface**: Available as both a command-line tool and an interactive web application (Chainlit)

## 📋 Prerequisites

- Python 3.11 or higher
- FFmpeg (required for video processing)
- ImageMagick (optional, for enhanced text rendering in captions)
- OpenAI API key
- Pexels API key

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Text-To-Video-AI
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install FFmpeg:**
   - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

6. **Install ImageMagick (Optional but recommended):**
   - **Windows**: Download from [ImageMagick website](https://imagemagick.org/script/download.php)
   - **macOS**: `brew install imagemagick`
   - **Linux**: `sudo apt-get install imagemagick`

7. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_KEY=your_openai_api_key_here
   PEXELS_KEY=your_pexels_api_key_here
   ```

   You can get your API keys from:
   - OpenAI: https://platform.openai.com/api-keys
   - Pexels: https://www.pexels.com/api/ (the API key is in `apis.txt` - move it to `.env`)

## 📖 Usage

### Command-Line Interface

Run the application from the command line with a topic:

```bash
python app.py "सत्यं वद"
```

Replace `"सत्यं वद"` with your Sanskrit text or topic. The application will:
1. Generate a story script
2. Create audio narration
3. Generate timed captions
4. Find background videos
5. Render the final video

The output video will be saved as `rendered_video.mp4`.

### Web Interface (Chainlit)

Launch the interactive web interface:

```bash
chainlit run main.py
```

Then open your browser to the URL shown (typically `http://localhost:8000`). You can:
- Enter Sanskrit text in the chat interface
- Watch the progress as each step completes
- View the generated video directly in the browser

## 🏗️ Project Structure

```
Text-To-Video-AI/
├── main.py                          # Chainlit web interface
├── app.py                           # Command-line interface
├── requirements.txt                 # Python dependencies
├── chainlit.md                      # Chainlit welcome screen
├── apis.txt                         # API keys (move to .env)
├── utility/
│   ├── script/
│   │   └── script_generator.py      # Story generation using OpenAI
│   ├── audio/
│   │   └── audio_generator.py       # Text-to-speech using OpenAI TTS
│   ├── captions/
│   │   └── timed_captions_generator.py  # Whisper-based caption generation
│   ├── video/
│   │   ├── video_search_query_generator.py  # AI-powered search query generation
│   │   └── background_video_generator.py    # Pexels video search and retrieval
│   ├── render/
│   │   └── render_engine.py         # Video composition and rendering
│   └── utils.py                     # Utility functions (logging)
├── .logs/                           # API response logs (gitignored)
├── rendered_video.mp4               # Output video (gitignored)
└── audio_tts.wav                    # Generated audio (gitignored)
```

## 🔧 How It Works

The application follows a multi-stage pipeline:

1. **Script Generation** (`utility/script/script_generator.py`)
   - Takes Sanskrit text input
   - Uses OpenAI GPT-4o-mini to translate and generate a moral story
   - Returns a JSON-formatted script (<140 words)

2. **Audio Generation** (`utility/audio/audio_generator.py`)
   - Converts the generated script to speech
   - Uses OpenAI TTS API with streaming response
   - Saves audio as WAV file

3. **Caption Generation** (`utility/captions/timed_captions_generator.py`)
   - Uses Whisper timestamped model to transcribe audio
   - Generates word-level timestamps
   - Creates timed caption segments (max 15 words per segment)

4. **Video Search Query Generation** (`utility/video/video_search_query_generator.py`)
   - Analyzes script and timed captions
   - Uses OpenAI to generate visually concrete search keywords
   - Creates time-synchronized search queries

5. **Background Video Retrieval** (`utility/video/background_video_generator.py`)
   - Searches Pexels API for relevant videos
   - Filters for 1920x1080 landscape videos
   - Selects best matching videos for each time segment

6. **Video Rendering** (`utility/render/render_engine.py`)
   - Downloads background videos
   - Composites videos, audio, and captions
   - Uses MoviePy for final video assembly
   - Outputs MP4 file with H.264 encoding

## 📦 Dependencies

Key dependencies include:

- **OpenAI** (`openai==1.31.1`) - For script generation and TTS
- **Whisper Timestamped** (`whisper-timestamped==1.15.4`) - For caption generation
- **MoviePy** (`moviepy==1.0.3`) - For video editing and rendering
- **Chainlit** - For web interface
- **Edge TTS** (`edge-tts==6.1.12`) - Alternative TTS option
- **Requests** - For API calls
- **Python-dotenv** - For environment variable management

See `requirements.txt` for the complete list.

## ⚙️ Configuration

### API Keys

Ensure your `.env` file contains:
```env
OPENAI_KEY=sk-...
PEXELS_KEY=...
```

### Video Server

Currently supports:
- `pexel` - Uses Pexels API for background videos
- `stable_diffusion` - Placeholder for future image generation support

### Audio Settings

Default TTS settings in `utility/audio/audio_generator.py`:
- Model: `tts-1`
- Voice: `echo` (options: alloy, echo, fable, onyx, nova, shimmer)
- Format: Auto-detected from filename extension

### Caption Settings

Default caption settings in `utility/captions/timed_captions_generator.py`:
- Model: `base` (Whisper model size)
- Max caption size: 15 words

## 🐛 Troubleshooting

### FFmpeg Not Found
- Ensure FFmpeg is installed and added to your system PATH
- Verify installation: `ffmpeg -version`

### ImageMagick Not Found
- Captions will still work but may have reduced quality
- Install ImageMagick and ensure `magick` command is available

### API Errors
- Verify your API keys are correct in `.env`
- Check your OpenAI and Pexels API quotas
- Review logs in `.logs/` directory for detailed error messages

### Video Rendering Issues
- Ensure sufficient disk space for temporary video files
- Check that background videos are downloading correctly
- Verify audio file is generated successfully

## 📝 Logging

The application logs API responses to:
- `.logs/gpt_logs/` - OpenAI API responses
- `.logs/pexel_logs/` - Pexels API responses

These logs help debug issues and track API usage.

---

**Note**: This project is designed for educational and creative purposes. Ensure you comply with API usage terms and video licensing when using generated content.

