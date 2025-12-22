# In the Authorization module we have the following files in store directory:
![image.png](/.attachments/image-13fcdb83-69db-4aac-8a88-50f83a9620ed.png)

## [authorization.actions.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fauthorization%2Fstore%2Fauthorization.actions.ts&version=GBdev&_a=contents)
Contains NGRX actions for authorization module like:
- login2FaAction
- verify2FaAction
- loginAction
- loginSuccessAction
- changePasswordAction
- loadUserPermissionsAction
- logoutAction
- clearUserAction

## [authorization.effects.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fauthorization%2Fstore%2Fauthorization.effects.ts&version=GBdev&_a=contents)

Contains NGRX effects that listens to invoked actions and react by invoking new actions (depends on logic).

## [authorization.reducer.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fauthorization%2Fstore%2Fauthorization.reducer.ts&version=GBdev&_a=contents)

Contains NGRX reducer that listens to invoked actions and changes and change store state accordingly.

## [authorization.selector.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fauthorization%2Fstore%2Fauthorization.selector.ts&version=GBdev&_a=contents)
A helper file that contains all the store selectors of the Authorization module. A selector is an object that reveals a relevant part of the store.
i.e. : selectLoginErrorMessage - This selector reveals the current error message in the store state (if any). 

## [authorization.state.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fauthorization%2Fstore%2Fauthorization.state.ts&version=GBdev&_a=contents)

Store state file.
In the Authorization module we save to store the following data in order to enable it in all the relevant components:
- loginErrorMessage
- isServerUp



