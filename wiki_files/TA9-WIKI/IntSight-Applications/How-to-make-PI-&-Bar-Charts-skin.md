[[_TOC_]]
 
# 1. Prerequisits
The first To create Pi or Bar chart is to make sure that the data model (or Plugin) contains the following columns:

1. **Column holding the Argument** - E.g. call direction - incoming or outgoing, numbers - 1, 2, 3, 4... etc.
2. **Count column** - holding the count from each column (Must be a number)
3. **Percentage column** - holding the data of how much percent the count column takes from the total 100% amount. 
> _NOTE: Percentage Column Name must be named "%"_

---

# 2. Steps to Create the Configuration
To activate the "pi" or "Bar" chart skin - a configuration should be done on Admin Studio "Group" property.

Once configured, the data model should support that skin in the "skins" view:
![image.png](/.attachments/image-45207a53-afb9-4fe7-8070-b9985ddd0c84.png)


## 2.1 Admin Configuration
1. Add the group name "argument" to the column holding the Argument data. In this example, the "direction" column is the argument:
![image.png](/.attachments/image-4c80a488-0a4b-47bb-9290-bd8895da84e8.png)

2. Add the group name "count" to the column holding the count data. In this example, the "total" column is the count:

![image.png](/.attachments/image-8f4924d9-7e8a-4986-a51f-6e34d9948be4.png)

## 2.2 Sample Data
you can use this sample data as a CSV file, to load as a data model for test:

`direction,total,%`
`1,10,20`
`2,50,80`

direction = argument group name
total = count group name