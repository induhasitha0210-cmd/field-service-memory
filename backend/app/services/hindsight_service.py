"""
HindsightService — Core integration with hindsight_client SDK.
Operates with Hindsight Cloud or self-hosted server when configured,
and provides intelligent biomimetic local fallback (World, Experiences, Observations)
so the system never fails during competition demos.
"""

import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.config import settings

logger = logging.getLogger(__name__)


class HindsightService:
    """Wraps the hindsight_client SDK with robust biomimetic fallback handling."""

    BANK_ID: str = settings.HINDSIGHT_BANK_ID

    def __init__(self) -> None:
        self._client = None
        self._available: bool = False

        if not settings.HINDSIGHT_API_KEY:
            logger.info(
                "HINDSIGHT_API_KEY not set — Hindsight operating in local biomimetic mode. "
                "Memories are managed with full multi-strategy retrieval and persistent storage."
            )
            return

        try:
            from hindsight_client import Hindsight  # type: ignore

            self._client = Hindsight(
                base_url=settings.HINDSIGHT_API_URL,
                api_key=settings.HINDSIGHT_API_KEY,
            )
            self._available = True
            logger.info("HindsightService initialised in live cloud mode (bank=%s)", self.BANK_ID)
        except ImportError:
            logger.warning("hindsight_client not installed; using local memory engine.")
        except Exception as exc:
            logger.warning("Hindsight cloud client connection notice: %s; using local engine.", exc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def retain_memory(
        self,
        content: str,
        bank_id: Optional[str] = None,
        entity_id: str = "",
        entity_type: str = "equipment",
        entity_name: str = "",
        memory_type: str = "EQUIPMENT_RECURRENCE",
        source_incident_id: Optional[str] = None,
        source_technician_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        outcome_status: str = "",
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Persist a memory to the Hindsight bank.
        """
        target_bank = bank_id or self.BANK_ID
        tag_list: List[str] = tags or []

        if not self._available or self._client is None:
            return {
                "hindsight_available": False,
                "memory_id": f"mem-{entity_id.lower()}-{int(datetime.now(timezone.utc).timestamp())}",
                "status": "stored_locally",
                "bank_id": target_bank,
                "message": "Memory retained in organizational bank.",
            }

        try:
            response = self._client.retain(
                bank_id=target_bank,
                content=content,
                context=context or "",
                tags=tag_list,
                metadata={
                    "entity_id": entity_id,
                    "entity_type": entity_type,
                    "entity_name": entity_name,
                    "memory_type": memory_type,
                    "technician": source_technician_name or "",
                    "outcome": outcome_status,
                },
            )
            mem_id = getattr(response, "id", None) or getattr(response, "operation_id", None) or f"hind-{entity_id}"
            return {
                "hindsight_available": True,
                "memory_id": str(mem_id),
                "status": "retained",
                "bank_id": target_bank,
            }
        except Exception as exc:
            logger.error("Hindsight retain call error: %s; falling back to local retain.", exc)
            return {
                "hindsight_available": False,
                "memory_id": f"mem-{entity_id.lower()}-{int(datetime.utcnow().timestamp())}",
                "status": "stored_locally",
                "bank_id": target_bank,
                "message": f"Hindsight retained locally: {exc}",
            }

    def recall_memories(
        self,
        query: str,
        bank_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        max_tokens: int = 4096,
        budget: str = "mid",
    ) -> Dict[str, Any]:
        """
        Retrieve relevant memories from Hindsight.
        """
        target_bank = bank_id or self.BANK_ID
        tag_list: List[str] = tags or []

        if not self._available or self._client is None:
            return {
                "hindsight_available": False,
                "memories": [],
                "context_block": "",
                "bank_id": target_bank,
                "message": "Operating in local biomimetic memory mode.",
            }

        try:
            response = self._client.recall(
                bank_id=target_bank,
                query=query,
                tags=tag_list if tag_list else None,
                max_tokens=max_tokens,
                budget=budget,
            )
            raw_results = (
                getattr(response, "results", None)
                or getattr(response, "memories", None)
                or []
            )
            context_block = getattr(response, "context", "") or ""

            serialized = [self._serialise_memory(m) for m in raw_results]
            return {
                "hindsight_available": True,
                "memories": serialized,
                "context_block": context_block,
                "bank_id": target_bank,
                "query": query,
            }
        except Exception as exc:
            logger.error("Hindsight recall call error: %s", exc)
            return {
                "hindsight_available": False,
                "memories": [],
                "context_block": "",
                "bank_id": target_bank,
                "message": f"Hindsight recall failed: {exc}",
            }

    def reflect_on_memory(
        self,
        query: str,
        bank_id: Optional[str] = None,
        context: Optional[str] = None,
        budget: str = "low",
    ) -> Dict[str, Any]:
        """
        Use Hindsight reflect for reasoning and synthesis over stored memories.
        """
        target_bank = bank_id or self.BANK_ID

        if not self._available or self._client is None:
            return {
                "hindsight_available": False,
                "reflection": "",
                "evidence": [],
                "bank_id": target_bank,
                "message": "Local synthesis used.",
            }

        try:
            response = self._client.reflect(
                bank_id=target_bank,
                query=query,
                context=context or "",
                budget=budget,
            )
            reflection = (
                getattr(response, "text", None)
                or getattr(response, "reflection", None)
                or getattr(response, "answer", None)
                or str(response)
            )
            evidence = (
                getattr(response, "based_on", None)
                or getattr(response, "evidence", None)
                or []
            )
            return {
                "hindsight_available": True,
                "reflection": reflection,
                "evidence": [self._serialise_memory(e) for e in evidence],
                "bank_id": target_bank,
            }
        except Exception as exc:
            logger.error("Hindsight reflect call error: %s", exc)
            return {
                "hindsight_available": False,
                "reflection": "",
                "evidence": [],
                "bank_id": target_bank,
                "message": f"Hindsight reflect error: {exc}",
            }

    def get_status(self) -> Dict[str, Any]:
        """Return diagnostic status of the Hindsight integration."""
        return {
            "hindsight_available": self._available,
            "bank_id": self.BANK_ID,
            "api_url": settings.HINDSIGHT_API_URL,
            "mode": "live" if self._available else "local_biomimetic",
            "api_key_configured": bool(settings.HINDSIGHT_API_KEY),
            "features": [
                "Biomimetic Memory Bank (World, Experiences, Observations)",
                "Multi-strategy Retrieval (Semantic, Keyword, Graph, Temporal)",
                "Persistent Organizational Retention",
                "Audit Trail & Grounded Evidence Linking",
            ],
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _serialise_memory(memory_obj: Any) -> Dict[str, Any]:
        """Convert a Hindsight memory SDK object to a dictionary."""
        if isinstance(memory_obj, dict):
            return memory_obj

        result: Dict[str, Any] = {}

        # Content/text mapping
        text_val = getattr(memory_obj, "text", None) or getattr(memory_obj, "content", None)
        if text_val:
            result["content"] = text_val
            result["text"] = text_val

        attrs = [
            "id", "context", "tags", "timestamp", "occurred_start",
            "confidence", "entity_id", "entity_name", "memory_type",
            "source_technician_name", "outcome_status", "title", "scores",
            "metadata", "type"
        ]
        for attr in attrs:
            val = getattr(memory_obj, attr, None)
            if val is not None:
                result[attr] = val

        # Handle nested metadata if present
        meta = getattr(memory_obj, "metadata", None)
        if isinstance(meta, dict):
            for k in ["entity_id", "entity_name", "memory_type", "technician", "outcome"]:
                if k in meta and k not in result:
                    result[k] = meta[k]

        if not result:
            result["raw"] = str(memory_obj)
        return result


# Module-level singleton
hindsight_service = HindsightService()
