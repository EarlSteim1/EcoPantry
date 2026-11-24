"""
EcoPantry AI - Telemetry, Tracing & Prompt Management Module
Provides prompt version management, latency/token telemetry,
and Langfuse trace integration with an interactive local trace inspector.
"""
import time
import uuid
from typing import Dict, Any, List

# Versioned System Prompts
PROMPT_REGISTRY = {
    "v1.0-baseline": {
        "version": "1.0.0",
        "name": "Chef Eco - Baseline Persona",
        "description": "Standard zero-waste chef persona with basic recipe formatting rules.",
        "template": "You are Chef Eco, a helpful culinary assistant. Suggest recipes using leftover ingredients."
    },
    "v2.0-rag-grounded": {
        "version": "2.0.0",
        "name": "Chef Eco - RAG Grounded",
        "description": "Retrieval-augmented prompt incorporating USDA food safety, shelf-life, and scrap cooking citations.",
        "template": (
            "You are Chef Eco, a zero-waste culinary coach. Ground your advice strictly on the provided "
            "authoritative USDA and culinary guidelines. Cite source IDs when referencing food safety."
        )
    },
    "v2.1-agentic-production": {
        "version": "2.1.0",
        "name": "Chef Eco - Enterprise Production (RAG + Agentic + Defenses)",
        "description": "Full production prompt featuring ReAct tool execution, XML delimiter framing, and canary defense directives.",
        "template": (
            "You are Chef Eco, a warm, authoritative culinary coach and zero-waste consultant.\n"
            "Synthesize tool observations (nutrition macros, shelf-life limits, carbon offset) "
            "and retrieved USDA knowledge into an actionable, uniform recipe card."
        )
    }
}

class TelemetryManager:
    def __init__(self):
        self.traces: List[Dict[str, Any]] = []
        self.active_prompt_version = "v2.1-agentic-production"
        self.langfuse_connected = False

    def get_prompt(self, version_key: str = None) -> Dict[str, Any]:
        """Fetches prompt definition and metadata from the registry."""
        key = version_key or self.active_prompt_version
        return PROMPT_REGISTRY.get(key, PROMPT_REGISTRY["v2.1-agentic-production"])

    def start_trace(self, user_query: str, session_id: str = None) -> Dict[str, Any]:
        """Initiates a telemetry trace session."""
        trace_id = f"trace_{uuid.uuid4().hex[:8]}"
        trace_record = {
            "trace_id": trace_id,
            "session_id": session_id or "default_session",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "start_time": time.time(),
            "query": user_query,
            "prompt_version": self.active_prompt_version,
            "security_status": "PENDING",
            "rag_retrievals": [],
            "agent_tools": [],
            "latency_ms": 0,
            "input_tokens_est": len(user_query.split()) * 2,
            "output_tokens_est": 0,
            "status": "RUNNING"
        }
        return trace_record

    def end_trace(self, trace_record: Dict[str, Any], response_text: str, security_status: str, rag_docs: list = None, agent_tools: list = None):
        """Finalizes trace with metrics, token estimations, and tool metadata."""
        duration_ms = round((time.time() - trace_record["start_time"]) * 1000, 2)
        trace_record["latency_ms"] = duration_ms
        trace_record["security_status"] = security_status
        trace_record["output_tokens_est"] = len(response_text.split()) * 2
        trace_record["rag_retrievals"] = [
            {"id": d.get("id"), "title": d.get("title"), "score": d.get("relevance_score")} 
            for d in (rag_docs or [])
        ]
        trace_record["agent_tools"] = [
            {"tool": t.get("tool"), "step": t.get("step")} 
            for t in (agent_tools or [])
        ]
        trace_record["status"] = "COMPLETED"
        
        # Store in rolling trace buffer (up to 50 traces)
        self.traces.insert(0, trace_record)
        if len(self.traces) > 50:
            self.traces.pop()

    def get_recent_traces(self) -> List[Dict[str, Any]]:
        return self.traces

# Global Singleton Telemetry Manager
telemetry_service = TelemetryManager()
