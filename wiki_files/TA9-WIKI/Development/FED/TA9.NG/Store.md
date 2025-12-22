# [This](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fadmin&version=GBdev&_a=contents) directory contains application-wise store NGRX store files.
If one module needs to listen to an action that are invoked as a result of something that happened in other module  it shall be done in an effect/ a reducer file inside this directory.
Generally the main app.module "knows" all its sub modules but no module knows the other sub module.


For example:
In [search.component.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fanalyst%2Fmodules%2Ffederated-search%2Fmodules%2Fsearch%2Fcomponents%2Fsearch%2Fsearch.component.ts&version=GBdev) inside the federated-search module we dispatch getCurrentUserAction.
This action has effect inside [federated-search.app.effects.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fstore%2Ffederated-search.app.effects.ts&version=GBdev):
```
  languageChanged$ = createEffect( () =>
      this.actions$.pipe(
        ofType(SearchActions.getCurrentUserAction),
        map(() => {
          const userContext: UserContext = JSON.parse(localStorage.getItem('currentUser'));
          return AuthorizationActions.setCurrentUserAction({user: userContext});
        })
      )
  );
```

When this action is dispatched, the effect takes the current user data from localStorage and dispatch setCurrentUserAction that then is cached inside the 
[app.reducer.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fstore%2Fapp.reducer.ts&version=GBdev) and updates the store with the user data:
```    
AuthorizationActions.setCurrentUserAction,
    (state, {user}) => ({
      ...state,
      user: {...user}
    })),
```