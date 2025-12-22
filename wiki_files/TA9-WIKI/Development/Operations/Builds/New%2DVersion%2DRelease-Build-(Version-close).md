[[_TOC_]]


## Intro
This build closes a version on a specified branch.
Generally, it organizing scripts and mark the SCM with a tag.

**This build has to run whenever we'd like to close a version.**

## Inputs
1. `Branch` - the **branch** that we would like to perform the version closing on. If we're closing from dev, than we use `dev`, but if we have proceeded with `dev` and want to close a version on different branch (version branch, like `2.9` for example) - we choose that one instead of `dev`
2. Variables:
2.1. `_GitTagComment` - the git comment to specify for the newly created tag
2.2. `_GitTag_Name` - the name of the tag to create. Convention: `2_9_0`
2.3. `CurrentVersion` - latest released version (for example, `2_8_0`)
2.4. `NewVersion` - the name of the new version. Same convention as above

### Sample parameters
![image.png](/.attachments/image-4199d96d-e8cb-4d08-98ba-d173e1e310be.png)
![image.png](/.attachments/image-0c308c62-1f0b-42d3-92c7-68bdf440646c.png)


## Outputs
1. BaseScript for version (`DBScripts/MySql/BaseScripts/BaseScript_2_9_0.sql`)
1. BaseScript with Data (`DBScripts/MySql/BaseScriptsWithData/BASE_2_9_0_Dev_Machine.sql`)
1. Resetting DBChangeSyncer.json (`{"queries":[]}`)
1. Upgrade script (`DBScripts/MySql/UpdateScripts/DBChangeSyncer-2_8_0_to_2_9_0.json`)
1. New tag (New tag `2_9_0` )

## After successful run
1. All these changes were pushed to the branch defined on step 1 ('Branch').
1. Now, if that wasn't dev branch, we should merge these changes into dev as well (PR: 2.9->dev)
1. Also create PR from version branch (eg 2.9, same as step 1) to other version specific branches (aka: 'client branches')