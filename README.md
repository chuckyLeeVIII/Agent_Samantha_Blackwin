# Agent_Samantha_Blackwin

This project provides an experimental framework for building fully local AI agents. It now includes a small retrieval-augmented generation (RAG) example using the open-source **Qwen** model. The agent can respond using a local text-to-speech engine configured with a British accent.

## Features

- Works completely offline. Models are expected to be available locally.
- Simple FAISS index for document retrieval.
- Text-to-speech output using `pyttsx3`. A British voice is selected by default,
  but you can specify any installed voice with the `voice_name` argument. Call
  `list_available_voices()` to see voices detected on your system.
- Example script `rag_assistant.py` that demonstrates question answering over a
  small set of documents. Conversation logs can optionally be stored in
  SurrealDB.

## One-click installation

Run `one_click_setup.sh` on Linux/macOS or `one_click_setup.bat` on Windows to
create a virtual environment, install dependencies, and register the assistant
to start automatically whenever you log in. After running the script, the
assistant launches immediately and will auto-start on reboot.

## Usage

1. Download the desired Qwen model (for example `Qwen/Qwen-7B-Chat`) and place it in a local directory.
2. Install dependencies (or just run the one-click script):
   ```bash
   pip install -r requirements.txt
   ```
   Alternatively, execute `./one_click_setup.sh` or `one_click_setup.bat` which
   will install everything automatically.
3. Prepare a set of text documents you want the assistant to search through.
4. Run the example:
   ```bash
   python rag_assistant.py
   ```
   Ask a question and the assistant will respond aloud with a British accent.
   To use a specific installed voice, pass the `voice_name` argument when
   creating `LocalRAGAssistant`, e.g. `LocalRAGAssistant(model_path="Qwen/Qwen-7B-Chat", voice_name="lottie")`.
   You can also enable the BMAD Method and Evolve 2 workflow with
   `use_bmad=True` and by passing a custom `Evolve2Workflow` instance.

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

## BMAD Method and Evolve 2 integration

`workflow_engine.py` includes minimal stubs for the **BMAD Method** and the
**Evolve 2** workflow engine. Enable these components when creating
`LocalRAGAssistant` to preprocess input or orchestrate multi-step agent
behaviors.


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
