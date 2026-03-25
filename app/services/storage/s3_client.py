"""
S3 に音声 bytes をアップロードし、URL を返す.
bucket/region 未設定時は None を返す.
"""

import logging
from typing import Optional

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def upload_audio_bytes(
    data: bytes,
    object_key: str,
    content_type: str = "audio/wav",
) -> Optional[str]:
    """
    bytes を S3 にアップロードし、オブジェクトの URL を返す.
    設定未設定時は None を返す (呼び出し側でスキップ).
    """
    settings = get_settings()
    if not settings.s3_bucket or not settings.s3_region:
        logger.debug("S3 未設定 (S3_BUCKET / S3_REGION)")
        return None
    if not settings.aws_access_key_id or not settings.aws_secret_access_key:
        logger.debug("AWS 認証情報未設定")
        return None

    try:
        import boto3
        from botocore.exceptions import ClientError
    except ImportError:
        logger.warning("boto3 がインストールされていません")
        return None

    client = boto3.client(
        "s3",
        region_name=settings.s3_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )
    try:
        client.put_object(
            Bucket=settings.s3_bucket,
            Key=object_key,
            Body=data,
            ContentType=content_type,
        )
        url = f"https://{settings.s3_bucket}.s3.{settings.s3_region}.amazonaws.com/{object_key}"
        return url
    except ClientError as e:
        logger.error("S3 アップロード失敗: %s", e)
        return None
