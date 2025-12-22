# Preface
**PermissionAuthorizeAttribute** is an **AuthorizeAttribute** that checks if specified **Claim**, or **Claim** and one of provided values (**for specified Claim**) are present in **User Claims**.
_More about ClaimsPrincipal, ClaimsIdentity and Claims_
::: video
<iframe width="640" height="480" src="https://www.youtube.com/embed/3i0RcKrVyTo" title="ClaimsPrincipal, ClaimsIdentity and Claim | ASP.NET CORE Identity & Security Series | Episode #3" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
:::


# Usage
_Besides default values in **ClaimTypes** we have Ta9 claim types: **TaClaimTypes**_

1. To check if **Claim** is present in User **Claims** add line below, above your controller method with **ClaimType** that you want to check.

```
[PermissionAuthorizeAttribute(ClaimTypes.Role)]
```

2. To check if **Claims** and one of provided values are present in **User Claims** add line below, above your controller method with **ClaimType** and values.

```
[PermissionAuthorizeAttribute(ClaimTypes.Role, Permissions.Admin, Permissions.User)]
```
### Explanation for use-case above:
_If **Claim** with claim type **ClaimTypes.Role** will be present in **User Claims** but it's value will be something other then **"Admin" or "User"** error **403** will be returned_