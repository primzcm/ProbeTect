from __future__ import annotations

import mimetypes
import os
import urllib.error
import urllib.request
import uuid

from django.conf import settings


class SupabaseStorageError(RuntimeError):
    pass


def _get_config() -> tuple[str, str, str]:
    url = getattr(settings, "SUPABASE_URL", None) or os.getenv("SUPABASE_URL")
    key = getattr(settings, "SUPABASE_SERVICE_ROLE_KEY", None) or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    bucket = getattr(settings, "SUPABASE_STORAGE_BUCKET", None) or os.getenv("SUPABASE_STORAGE_BUCKET", "materials")
    if not url or not key or not bucket:
        raise SupabaseStorageError("Supabase storage environment variables are not configured.")
    return url.rstrip("/"), key, bucket


def _perform_request(method: str, url: str, *, headers: dict[str, str] | None = None, data: bytes | None = None) -> bytes:
    request = urllib.request.Request(url, data=data, method=method)
    for key, value in (headers or {}).items():
        request.add_header(key, value)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="ignore")[:200]
        raise SupabaseStorageError(f"Supabase request failed ({exc.code}): {detail}") from exc
    except urllib.error.URLError as exc:
        raise SupabaseStorageError(f"Supabase request error: {exc.reason}") from exc


def upload_file(file_obj, *, owner_id: int, folder: str = "materials") -> tuple[str, str]:
    url, service_key, bucket = _get_config()
    filename = file_obj.name
    file_ext = os.path.splitext(filename)[1]
    unique_name = f"{folder}/{owner_id}/{uuid.uuid4().hex}{file_ext}"
    storage_endpoint = f"{url}/storage/v1/object/{bucket}/{unique_name}"

    content_type = getattr(file_obj, "content_type", None) or mimetypes.guess_type(filename)[0] or "application/octet-stream"
    file_obj.seek(0)
    file_bytes = file_obj.read()

    _perform_request(
        "POST",
        storage_endpoint,
        headers={
            "Authorization": f"Bearer {service_key}",
            "Content-Type": content_type,
            "x-upsert": "true",
        },
        data=file_bytes,
    )

    public_url = f"{url}/storage/v1/object/public/{bucket}/{unique_name}"
    return unique_name, public_url


def delete_file(storage_path: str) -> None:
    url, service_key, bucket = _get_config()
    endpoint = f"{url}/storage/v1/object/{bucket}/{storage_path}"
    try:
        _perform_request("DELETE", endpoint, headers={"Authorization": f"Bearer {service_key}"})
    except SupabaseStorageError:
        # Ignore missing files for now; future work can log these attempts.
        pass
