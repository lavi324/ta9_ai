**In Order to run ConsoleHoster locally, there is a need to:**
1. Encrypt the data connection string that is written in the database under "dataconnectiomanager" table (Any Connection string from sqlite_metadata.
The encryption is performed from Utils.TESTS.
2. Paste the encrypted connection string in the Metadata line of the ConnectionsManager.config file. inside ServiceManager\Contracts\Contracts.Common\Configuration\
3. Build All and run the ConsoleHoster.