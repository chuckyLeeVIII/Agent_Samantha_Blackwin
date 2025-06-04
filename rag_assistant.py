import os
from typing import List, Optional

import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer
import pyttsx3
from workflow_engine import BMADMethod, Evolve2Workflow

from surrealdb_client import SurrealDBClient
from video_generator import RealTimeVideoGenerator


class LocalRAGAssistant:
    """Simple retrieval augmented generation assistant using Qwen."""

    def __init__(
        self,
        model_path: str,
        embeddings_model: str = "all-MiniLM-L6-v2",
        db_client: Optional[SurrealDBClient] = None,
        voice_name: Optional[str] = None,
        use_bmad: bool = False,
        workflow: Optional[Evolve2Workflow] = None,
        video_generator: Optional[RealTimeVideoGenerator] = None,
    ):
        """Create a local RAG assistant.

        Parameters
        ----------
        model_path : str
            Path to a locally available Qwen model.
        embeddings_model : str, optional
            SentenceTransformer model used for embeddings.
        db_client : SurrealDBClient, optional
            Database client for logging conversation history.
        voice_name : str, optional
            Name of a ``pyttsx3`` voice to use. Falls back to a British
            English voice if the name is not found.
        use_bmad : bool, optional
            Whether to enable the BMAD Method pipeline.
        workflow : Evolve2Workflow, optional
            Custom workflow to run on each input before querying.
        video_generator : RealTimeVideoGenerator, optional
            Optional video generator used to render answers.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True)
        self.embedder = SentenceTransformer(embeddings_model)
        self.index = None
        self.documents: List[str] = []
        self.db_client = db_client
        self.workflow = workflow if workflow else Evolve2Workflow()
        self.bmad = BMADMethod() if use_bmad else None
        self.video_generator = video_generator

        # Text to speech engine with optional voice selection
        self.tts_engine = pyttsx3.init()
        self.voice_id = None
        voices = self.tts_engine.getProperty("voices")
        if voice_name:
            for voice in voices:
                if voice_name.lower() in voice.id.lower() or voice_name.lower() in getattr(voice, "name", "").lower():
                    self.tts_engine.setProperty("voice", voice.id)
                    self.voice_id = voice.id
                    break
            if self.voice_id is None:
                print(f"Voice '{voice_name}' not found. Using default British voice.")
        if self.voice_id is None:
            for voice in voices:
                if "en-gb" in voice.id.lower():
                    self.tts_engine.setProperty("voice", voice.id)
                    self.voice_id = voice.id
                    break


    def build_index(self, docs: List[str]):
        """Create a simple FAISS index from a list of documents."""
        self.documents = docs
        embeddings = self.embedder.encode(docs)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def query(self, question: str) -> str:
        """Return the model answer given retrieved context."""
        if self.index is None:
            raise ValueError("Index not built")

        if self.bmad:
            question = self.bmad.apply(question)
        if self.workflow:
            question = self.workflow.run(question)

        question_embedding = self.embedder.encode([question])
        _, indices = self.index.search(question_embedding, k=3)
        retrieved_context = "\n".join(self.documents[i] for i in indices[0])

        prompt = f"Context:\n{retrieved_context}\n\nQuestion: {question}\nAnswer:"
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=128)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        if self.db_client:
            self.db_client.log_conversation(question, answer)
        if self.video_generator:
            self.video_generator.generate(answer)
        return answer

    def speak(self, text: str):
        """Speak text using local TTS engine."""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def list_available_voices(self) -> List[str]:
        """Return a list of available voice names."""
        return [voice.id for voice in self.tts_engine.getProperty("voices")]


if __name__ == "__main__":
    # Example usage with SurrealDB logging
    db = SurrealDBClient()
    voice = input("Voice name (blank for default): ")
    workflow = Evolve2Workflow()
    assistant = LocalRAGAssistant(
        model_path="Qwen/Qwen-7B-Chat",
        db_client=db,
        voice_name=voice or None,
        use_bmad=True,
        workflow=workflow,
        video_generator=RealTimeVideoGenerator(),
    )
    docs = [
        "Qwen is an open-source large language model.",
        "Retrieval augmented generation can improve response accuracy.",
        "This assistant uses a local voice with a British accent.",
    ]
    assistant.build_index(docs)
    question = input("Ask a question: ")
    answer = assistant.query(question)
    print("Answer:", answer)
    assistant.speak(answer)
