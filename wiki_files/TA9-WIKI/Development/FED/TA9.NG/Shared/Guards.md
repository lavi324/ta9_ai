# Guards Goal
The Angular way to give clients access only to their own application modules are guards.
For now, in our project there are [2 guards implemented](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fshared%2Fguards&version=GBdev&_a=contents):
1. AdminGuard
1. LoggedInGuard

# Implementation example for using guards

```
const coreRoutes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  {
    path: 'login',
    loadChildren: () => import('../modules/authorization/authorization.module').then(m => m.AuthorizationModule),
    canLoad: [ LoggedInGuard ], data: { preload: true, positiveGuard: false, redirect: '/' }
  },
  {
    path: 'analyst',
    loadChildren: () => import('../modules/analyst/analyst.module').then(m => m.AnalystModule),
    canLoad: [ LoggedInGuard ], data: { preload: true, positiveGuard: true, redirect: '/login' }
  },
  {
    path: 'admin',
    loadChildren: () => import('../modules/admin/admin.module').then(m => m.AdminModule),
    canLoad: [ LoggedInGuard ], data: { preload: true, positiveGuard: true, redirect: '/login' }
  },
  { path: 'server-down', component: ServerDownComponent }
];
```

As you can see - the "login", "analyst" and "admin" modules are lazy loaded. The LoggedInGuard checks if the user is logged in. only if he/she is logged in - the module will be loaded.
