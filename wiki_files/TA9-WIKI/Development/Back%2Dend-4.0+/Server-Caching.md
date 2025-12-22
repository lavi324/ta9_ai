[[_TOC_]]
In this section we will explain about cache architecture in the system and about Redis cache ( installation and helpful info)
Cache service code in the TA9 system is in the following projects : CacheService, infra.caching.redis and CacheAttribute(in middleware Nuget).

![image.png](/.attachments/image-ed939231-272d-48a0-a629-e5c013b5a15b.png)

## **CacheService:**
responsible on the following api :
![image.png](/.attachments/image-c93bc9b9-0130-4ab1-b2a4-b693292ad938.png)
`HttpDelete()-DeleteCacheByRegex(string regex)`-
`HttpDelete("global")-CleanGlobal()`-
`HttpDelete("ClearAll")-ClearAllCache()`- 

# **Cache Settings**
---
CachConfig, is a class object that represents Vault cache setting and appsetting.json configurations.

![image.png](/.attachments/image-3576e67d-d22e-423b-81ef-955a0c17652e.png)

# **Cache Nuget**
---
## **TA9.Intsight.Infra.Caching.Redis** 
Nuget that holds the following code sections:
1. *RedisCacheExtension*
Extension that organizes all services and configurations for connecting to Redis, used in service startup, need to inject the service config for Redis(CacheConfig).
2. *RedisStringLocalizer*
use to implements translation in services (uses HttpContextAccessor to extract user language from header and send the translation back to client. translation table is saved in cache).
3. *StackRedisCache*
class that implements commends to Redis like get and delete. implements ICache interface.

## **TA9.Intsight.Infra.Middleware** 
Nuget that implements **CacheAttribute**, Usually this attribute appears on GET API's to reduce client response time.
**Cache types** - saves the data in cache accordingly:
1. *Local*
if the data is relevant only for the local service we will save it in a folder with the service name ( the details are saved in service cache config- each service has the service name under CacheConfig.InstanseName in appsettings)
2. *Global*
If the data is needed between several services it will go to global cache (like translation table) under TA9.Application

# **Redis Installation**
---
## **Install Redis Container**
`docker run -d -e REDIS_PASSWORD="redis!@#$" -p 6379:6379 --name redis redis /bin/sh -c 'redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}'`

## **Installation of Redis Client [click here](https://redis.com/redis-enterprise/redis-insight)**

## **Add Redis Database**
![image.png](/.attachments/image-d1242a77-3ea4-458a-b926-4b0cc584531c.png)

## **Redis Key Example**
![image.png](/.attachments/image-6e78e6be-8823-4c80-af4f-8f1c5b1b8b6f.png)


# **Documentation for Redis Commands**
---
## **Useful Redis Commands: [redis.io/commands](https://redis.io/commands)**

![cache1.png](/.attachments/cache1-6c335389-1000-4b86-bc69-fdc4eb98ac72.png)

![cache3.png](/.attachments/cache3-c5a5fb8c-2549-45e7-aafc-3073960adf3a.png)![cache4.png](/.attachments/cache4-45d9c13f-cc6d-4011-8e27-c5c9ce8b1777.png)![cache5.png](/.attachments/cache5-1cf65c79-5abc-4f0d-9652-3dd7dcb7de21.png)![cache6.png](/.attachments/cache6-7fe315aa-c14f-4085-83f7-6f676bffe485.png)![cache7.png](/.attachments/cache7-388f2b56-1293-48f3-88c5-162acc771e65.png)![cache8.png](/.attachments/cache8-7af97018-d7ae-4838-9400-79adc75e1054.png)![cache9.png](/.attachments/cache9-f27740d0-7938-4601-a066-cf5de920eae3.png)





