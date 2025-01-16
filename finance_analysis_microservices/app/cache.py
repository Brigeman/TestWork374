import redis
import json

# Настройка Redis клиента
redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)

# Получение кэшированных данных
def get_cached_statistics():
    cached_data = redis_client.get("statistics")
    return json.loads(cached_data) if cached_data else None

# Сохранение статистики в кэш
def cache_statistics(stats):
    redis_client.set("statistics", json.dumps(stats), ex=3600)  # Данные кэшируются на 1 час