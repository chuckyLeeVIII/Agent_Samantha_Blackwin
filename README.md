# Agent_Samantha_Blackwin

This project provides an experimental framework for building fully local AI agents. It now includes a small retrieval-augmented generation (RAG) example using the open-source **Qwen** model. The agent can respond using a local text-to-speech engine configured with a British accent.

## Features

- Works completely offline. Models are expected to be available locally.
- Simple FAISS index for document retrieval.
 - Text-to-speech output using `pyttsx3`. A British voice is selected by default,
   but you can specify any installed voice.
- Example script `rag_assistant.py` that demonstrates question answering over a small set of documents. Conversation logs can optionally be stored in SurrealDB.

## Usage

1. Download the desired Qwen model (for example `Qwen/Qwen-7B-Chat`) and place it in a local directory.
2. Install dependencies:
   ```bash
   pip install faiss-cpu sentence-transformers transformers pyttsx3
   ```
3. Prepare a set of text documents you want the assistant to search through.
4. Run the example:
   ```bash
   python rag_assistant.py
   ```
   Ask a question and the assistant will respond aloud with a British accent.
   To use a specific installed voice, pass the `voice_name` argument when
   creating `LocalRAGAssistant`, e.g. `LocalRAGAssistant(model_path="Qwen/Qwen-7B-Chat", voice_name="lottie")`.

## Notes

- The text-to-speech voice is selected from voices installed on the host operating system. Use the `voice_name` argument to choose a specific voice. You may need to install an English (UK) voice for best results.
- This repository is provided as a minimal reference implementation. It does not include any video generation or real-time voice modulation components, which would require additional tooling.

## SurrealDB logging

You can store conversation history using a local [SurrealDB](https://surrealdb.com/) instance. Run `surreal start` to launch the database, then execute the assistant with logging enabled:

```bash
python rag_assistant.py
```

The default configuration assumes the database is available at `http://localhost:8000` with the default root credentials. Results will be stored in a `conversation` table and can be inspected using the [Surrealist](https://surrealdb.com/surrealist) UI.

## React Native interface (Evolve 2 prototype)

A minimal React Native app is included in `rn_app/`. It provides a simple text-based interface to the assistant and is intended as a starting point for integrating the **Evolve 2** workflow engine.

To run the React Native demo (dependencies must be installed beforehand):

```bash
cd rn_app
npm start
```

The demo uses placeholders for backend calls. Connect it to your local Python assistant or Evolve 2 service as needed.

The app starts with a dark color scheme. You can enable a simple theme editor by
setting `allowThemeEditing` to `true` in `rn_app/config.json`. When enabled, an
"Edit Theme" button lets you change the background and text colors at runtime.

## Building executables

You can create standalone binaries of `rag_assistant.py` using [PyInstaller](https://pyinstaller.org/).

### Linux

```bash
pip install pyinstaller
./build_exe.sh
```

### Windows

Run the commands inside a Windows environment:

```cmd
pip install pyinstaller
build_exe.bat
```

The resulting executable will appear in the `dist/` folder. Because PyInstaller
does not cross-compile, you must run the build command on each platform you want
to target.
