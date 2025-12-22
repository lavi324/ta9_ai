HAZHAROT Data Model contains number of files attached to every hazhara
when the data model loaded only the names of the files appears (without the extension)

To add the extension of the file, need to run a script   **'DeclarationNoFileExtensionFixed'**
The script searches the files in the folder and enrich the files extensions.
Need to run every time new files are added to the folder.
the script will be scheduled to run evert night, for manual run of the script:
enter the cmd and run:
​**DeclarationNoFileExtensionFixed.exe \\SERVER_IP\e$\Declaration**


yofi liza.