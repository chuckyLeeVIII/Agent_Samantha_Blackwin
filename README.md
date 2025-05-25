# Agent_Samantha_Blackwin

This project provides an experimental framework for building fully local AI agents. It now includes a small retrieval-augmented generation (RAG) example using the open-source **Qwen** model. The agent can respond using a local text-to-speech engine configured with a British accent.

## Features

- Works completely offline. Models are expected to be available locally.
- Simple FAISS index for document retrieval.
- Text-to-speech output using `pyttsx3` (British accent configuration).
- Example script `rag_assistant.py` that demonstrates question answering over a small set of documents.

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

## Notes

- The text-to-speech voice is selected based on voices installed on the host operating system. You may need to install an English (UK) voice for best results.
- This repository is provided as a minimal reference implementation. It does not include any video generation or real-time voice modulation components, which would require additional tooling.

## React Native interface (Evolve 2 prototype)

A minimal React Native app is included in `rn_app/`. It provides a simple text-based interface to the assistant and is intended as a starting point for integrating the **Evolve 2** workflow engine.

To run the React Native demo (dependencies must be installed beforehand):

```bash
cd rn_app
npm start
```

The demo uses placeholders for backend calls. Connect it to your local Python assistant or Evolve 2 service as needed.
