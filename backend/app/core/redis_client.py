import redis
import json
from typing import Optional, Any
from app.core.config import settings

redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5
)


def get_cache(key: str) -> Optional[Any]:
    """Get value from Redis cache"""
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"Redis get error: {e}")
        return None


def set_cache(key: str, value: Any, ttl: int = settings.CACHE_TTL) -> bool:
    """Set value in Redis cache with TTL"""
    try:
        redis_client.setex(
            key,
            ttl,
            json.dumps(value, default=str)
        )
        return True
    except Exception as e:
        print(f"Redis set error: {e}")
        return False


def delete_cache(key: str) -> bool:
    """Delete key from Redis cache"""
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        print(f"Redis delete error: {e}")
        return False


def clear_user_cache(user_id: int) -> bool:
    """Clear all cache entries for a user"""
    try:
        pattern = f"recommendations:user:{user_id}:*"
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
        return True
    except Exception as e:
        print(f"Redis clear cache error: {e}")
        return False

