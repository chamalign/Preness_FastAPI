"""
full_parts の listening 各 item について script を音声合成し S3 にアップロードし、
url_map と block_starts_per_part を返す. 音声/S3 未設定時は空 dict を返す.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from app.services.speech import (
    _split_config,
    passage_signature,
    split_listening_script,
    synthesize_script_to_bytes,
)
from app.services.storage import upload_audio_bytes
from app.core.config import get_settings

logger = logging.getLogger(__name__)

# full_parts のキー -> part_type (API 用)
LISTENING_PART_KEYS = [
    ("listening_part_a", "part_a"),
    ("listening_part_b", "part_b"),
    ("listening_part_c", "part_c"),
]


def _get_listening_script(item: Dict[str, Any]) -> List[Dict[str, Any]]:
    """item から content.listening_script を取得. 無ければ空リスト."""
    content = item.get("content") or {}
    script = content.get("listening_script")
    if isinstance(script, list):
        return script
    return []


def build_audio_url_map(
    full_parts: Dict[str, Dict[str, Any]],
    job_id: str,
    s3_prefix_override: Optional[str] = None,
) -> Tuple[Dict[str, str], Dict[str, List[int]]]:
    """
    full_parts の listening 3 パートについて、各 item の listening_script を
    音声合成して S3 にアップロードし、(url_map, block_starts_per_part) を返す.
    分割時: キーは "part_a:1:passage", "part_a:1:question" など.
    非分割時: キーは "part_a:1" など. 音声/S3 未設定時は ({}, {}).
    s3_prefix_override: 指定時は S3 オブジェクトキー先頭にこれを使う (手動指定時など).
    """
    settings = get_settings()
    if not settings.azure_speech_key or not settings.s3_bucket:
        return ({}, {})

    prefix = (
        (s3_prefix_override or settings.s3_mock_audio_prefix or "mocks/audio").rstrip("/")
    )
    url_map: Dict[str, str] = {}
    block_starts_per_part: Dict[str, List[int]] = {}
    split_cfg = _split_config()
    split_on = split_cfg["split_passage_questions"]
    dedup = split_cfg["deduplicate_passage_blocks"]

    for part_key, part_type in LISTENING_PART_KEYS:
        part_data = full_parts.get(part_key) or {}
        items = part_data.get("items") or []
        block_starts: List[int] = []
        previous_sig: Optional[str] = None

        for idx, item in enumerate(items, start=1):
            script = _get_listening_script(item)
            if not script:
                continue

            if split_on:
                passage_script, question_script = split_listening_script(script)
                sig = passage_signature(script)
                is_new_block = idx == 1 or (dedup and sig != previous_sig)
                if is_new_block:
                    block_starts.append(idx)
                    if passage_script:
                        audio_bytes = synthesize_script_to_bytes(passage_script)
                        if audio_bytes:
                            object_key = f"{prefix}/{job_id}/{part_key}/{idx:03d}_passage.wav"
                            url = upload_audio_bytes(audio_bytes, object_key)
                            if url:
                                url_map[f"{part_type}:{idx}:passage"] = url
                if question_script:
                    audio_bytes = synthesize_script_to_bytes(question_script)
                    if audio_bytes:
                        object_key = f"{prefix}/{job_id}/{part_key}/{idx:03d}_question.wav"
                        url = upload_audio_bytes(audio_bytes, object_key)
                        if url:
                            url_map[f"{part_type}:{idx}:question"] = url
                previous_sig = sig
            else:
                audio_bytes = synthesize_script_to_bytes(script)
                if audio_bytes:
                    object_key = f"{prefix}/{job_id}/{part_key}/{idx:03d}.wav"
                    url = upload_audio_bytes(audio_bytes, object_key)
                    if url:
                        url_map[f"{part_type}:{idx}"] = url
                block_starts.append(idx)

        block_starts_per_part[part_type] = block_starts

    return (url_map, block_starts_per_part)
