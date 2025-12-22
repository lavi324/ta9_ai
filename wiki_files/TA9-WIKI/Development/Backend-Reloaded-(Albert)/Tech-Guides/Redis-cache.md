**Intro**
Redis, which stands for Remote Dictionary Server, is a fast, open source, in-memory, key-value data store (cache). 
we will user cache when we use repeated data and we wanted to improve the performance of our service.

**install Redis in your computer:**
To install Redis container, use [this manual](https://hub.docker.com/_/redis), or run this command inside powershell: 
`docker run -d -e REDIS_PASSWORD="redis!@#$" -p 6379:6379 --name redis redis /bin/sh -c 'redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}'`

**Configuration**
To configure Redis cache in your .net core service - do the following:
1. add the selected dependencies:
![image.png](/.attachments/image-e21c3b23-8067-4df8-b976-036e8a4bb75b.png)
2. add the following to your appsettings file:


```
 "Cache": {
    "defaultExpirationTime": "00:01:00",
    "RedisConnection": "localhost:6379,password=redis!@#$",
    "InstanceName":  "savedCriteria1_"
  }
```



**under redisConnection put the relevant Redis IP and port,
**under "defaultExpirationTime" put the default expiration time in which the keys will be expaired
**under instans name put special value for this service cache

3. add this to your Startup file, in ConfigureServices function:


```
// Configure Redis cache
var cacheConfig =  Configuration.GetSection("Cache").Get<CacheConfig>();
services.Configure<CacheConfig>(Configuration.GetSection("Cache"));
services.AddStackExchangeRedisCache(options =>
{
options.Configuration = cacheConfig.RedisConnection;
options.InstanceName = cacheConfig.InstanceName; // Uniqe for the service
});

services.UseRedisCache();
```


4. Add static class with your prefix keys, for example:
  
```
public static class CachePerfixKeys
    {
        public static string savedCriteriaKey = "SavedCriteriaID";
    }
}
```

5. Flush cache:
in order to support "clear server cache" in our system, you must impliment another API with the rout "/FlushCache"
after that, make sure your sevice is in the enum "SystemModule" (on Argus) and the name of your service in the enum is matching the endpoint name in the "endpoints" table
then, in the function "ClearServerCache" (Argus) - call flush cache for your service like this:
` ClearServiceCacheMyModule(SystemModule.SavedCriteriaService);`

**Use Redis**
inject the ICache intarface to your component and set / get / remove keys from the cache
use example:


 
```
string recordKey = CachePerfixKeys.savedCriteriaKey + request.SavedCriteriaID;
                SavedCriteria savedCriteria = await _cache.GetRecoredAsync<SavedCriteria>(recordKey);
                if (savedCriteria is null)
                {
                    savedCriteria = await _readRepository.GetByIdAsync(request.SavedCriteriaID);

                    if (savedCriteria != null)
                    {
                        await _cache.SetRecordAsync<SavedCriteria>(recordKey, savedCriteria);
                    }

                    return savedCriteria;
                }else
                {
                    return savedCriteria;
                }
```

