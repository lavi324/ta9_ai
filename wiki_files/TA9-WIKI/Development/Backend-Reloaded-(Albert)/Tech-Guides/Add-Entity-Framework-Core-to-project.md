Intro 
Entity framework is a ORM provided by Microsoft. We're using EF Core as part of our .net core backend (Albert.Services) to CRUD our repositories.

First time installation
If that's the first time on a DEV machine, run the following command to install EF tool (Developer PowerShell from within VS2019):
`dotnet tool install --global dotnet-ef`

Define for a project:
1. Install NuGet packages
MySql.EntityFrameworkCore (Might be different than old microservices as MySql.EntityFrameworkCore has been deprecated)
Microsoft.EntityFrameworkCore.Design
1. Create a DB-context
On project level path (ie - where csproj is) run the following command (Developer PowerShell from within VS2019):
`dotnet ef dbcontext scaffold "server=localhost;user id=root; password=mysql!@#$; database=sqlite_metadata;Port=3306;CharSet=utf8" MySql.Data.EntityFrameworkCore  -o Model -c "SampleEfContext" -t sensors`
2.1 Attention to connection string
2.2 `Model` - the name of the folder to put all generated classes (ie - DbContext & Entities). **Those classes should be re-located to fit the project structure convention**
2.3 `sensors` - table name to connect to (ie - create entities for them). to specify multiple tables, repeat -t
1. Open the Inventory Context class file. You will see the database credentials are hard coded in the OnConfiguring method.
It’s not good practice to have db credentials in C# class. So, remove this OnConfiguring method from context file.
1. Put the connection string in appsettings.json (can be overwritten for different environments)
![image.png](/.attachments/image-16e6e8ad-4d8d-49dc-b2ab-eb317169585b.png)
1. Finally, on service's bootstrap (ie - `Startup.cs / ConfigureServices`) configure the ef with the connection string (it also injects DbContext)

`services.AddDbContextPool<SampleEfContext>(options => options.UseMySQL(Configuration.GetConnectionString("SampleApiDb")));`


https://docs.microsoft.com/en-us/ef/core/miscellaneous/cli/dotnet

nice tutorial: https://www.youtube.com/watch?v=-sftSA9_X-k

Clean Code with Entity Framework Core: https://www.youtube.com/watch?v=LDRxo6wDIE0