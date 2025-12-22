Deployment stages:

1. Json configuration file - must be placed in System32.
   We need to change URL value - according to IP in production environment. We have to update the content of the file ( DM numbers and field names)
   according to real values in prod.
2. Copy dll's to plugins folder.
3. Create DM's from dll's ( or copy definitions from dataschema1 and dataschemafields1 ).
4. Create Dashboard ( or copy definitions from dsb_dashboard_definitions and dsb_dashboard_widgets ).
5. User permissions (userdatamodels1).
6. Create passport id to numero piece views (attached[immigration_passports.txt](/.attachments/immigration_passports-1adf0c5a-24ca-4d88-9292-9745a21a4a64.txt)[unified_cni.txt](/.attachments/unified_cni-d5c5a62a-8fea-4dd0-9807-ebdef5062749.txt))

Possible Problems:
null value - make sure json file is loaded correctly
if there is problem with specific widget - need to check the proper working of DM that this widget based on.
There are certain values hardcoded in plugins - check the names of the fields according to dataschemafields1.


 
