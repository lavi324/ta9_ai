# In the Federated Search module we have the following files in store directory:
![image.png](/.attachments/image-2ca68f67-e429-43ab-a47f-752d87fab1da.png)

## [search.actions.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fanalyst%2Fmodules%2Ffederated-search%2Fcore%2Fstore%2Fsearch.actions.ts&version=GBdev)
Contains NGRX actions for authorization module like:
- addHistorySearchAction
- deleteHistorySearchAction
- updateSearchTextInputAction
- getCurrentUserAction
- getHistorySearchAction
- clearHistorySearchAction
- generateSearchAction
- generateSearchSuccessAction
- populateFacetsInStoreAction

## [search.effects.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fanalyst%2Fmodules%2Ffederated-search%2Fcore%2Fstore%2Fsearch.effects.ts&version=GBdev)

Contains NGRX effects that listens to invoked actions and react by invoking new actions (depends on logic).

## [search.reducer.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fanalyst%2Fmodules%2Ffederated-search%2Fcore%2Fstore%2Fsearch.reducer.ts&version=GBdev)

Contains NGRX reducer that listens to invoked actions and changes and change store state accordingly.

## [search.selector.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fanalyst%2Fmodules%2Ffederated-search%2Fcore%2Fstore%2Fsearch.selector.ts&version=GBdev)
A helper file that contains all the store selectors of the search module. A selector is an object that reveals a relevant part of the store.
i.e. : selectLoginErrorMessage - This selector reveals the current error message in the store state (if any). 

## [search.state.ts](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fanalyst%2Fmodules%2Ffederated-search%2Fcore%2Fstore%2Fsearch.state.ts&version=GBdev)

Store state file.
In the federated search module we save to store the following data in order to enable it in all the relevant components:
![image.png](/.attachments/image-456214a4-3b13-439a-8774-bff5bd0456ee.png)



