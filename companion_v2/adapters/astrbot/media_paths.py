"""Trusted attachment origin and directory for bridging adapters.

The WeChat bridge (``agent_wechat``) serves chat attachments from its own
loopback HTTP origin and downloads inbound media into AstrBot's temp
directory.  Both facts are read from the authenticated event, never from the
message payload, so a network message cannot grant itself local read access.
"""

import os
import tempfile


def trusted_media_origin(event):
    """The bridge serves chat attachments from its own loopback HTTP origin."""
    meta = getattr(event, "platform_meta", None)
    if getattr(meta, "name", None) != "agent_wechat":
        return None
    base = getattr(getattr(event, "client", None), "base_url", None)
    return base if type(base) is str and base else None


def trusted_media_root(event):
    """The bridge downloads inbound media into AstrBot's temp directory."""
    meta = getattr(event, "platform_meta", None)
    if getattr(meta, "name", None) != "agent_wechat":
        return None
    try:
        from astrbot.core.utils.astrbot_path import get_astrbot_temp_path
        base = get_astrbot_temp_path()
    except Exception:
        base = tempfile.gettempdir()
    root = os.path.join(base, "agent_wechat_bridge")
    if os.path.isdir(root):
        return root
    fallback = os.path.join(tempfile.gettempdir(), "agent_wechat_bridge")
    return fallback if os.path.isdir(fallback) else root
