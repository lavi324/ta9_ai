This [module](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fapp%2Fmodules%2Fadmin&version=GBdev&_a=contents) shall contain:
1. Functionalities that exist in the current TA9.App/Admin tool that have been migrated to new Angular.
2. New Administrator functionalities that have been implemented using new Angular.

**_Remark:_**
Generally - this module needs to be refactored a bit. 
The "components" directory in it shall be removed.
Today the existing one functionality that have been added to this section (Lookup manager) was implemented as a component.
We should consider moving it to an inner directory called "Modules" where each functionality will have its own module + store.