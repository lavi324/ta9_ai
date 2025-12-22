[[_TOC_]]

# Intro
IntSight supports mentioning a user on annotations.
The mentioned user will receive an email as an alert with a content.

# Guide
To configure the mentions module, the following steps have to be done:
1. [Configure Emails](/TA9-WIKI/IntSight-Applications/Configure-Emails)
1. All other configurations should be enough by BaseScript, but can be changed **if needed**:
1.1 `MentionMailSubjectFormat_User` format of the email subject
1.2 `MentionMailBodyFormat_User` format of the email body

## Disabling user mentioning
Mentionable items are configured in a table named `sqlite_metadata.text_mention_defs`
Currently, by version 2.9 only users mentioning is supported. In order to disable that, just clear the table

## Test configuration
1. Choose a user that has an email you have access to
1. Goto a case (no matter which)
1. Click on the 'Annotations' icon ![image.png](/.attachments/image-127fb3c1-250c-4e35-be9b-ff3017755ecf.png)
1. On the opened side-bar, add an annotation
1. Tag that user (from step # 1) by typing '@' followed by his name ![image.png](/.attachments/image-0c7361be-4ba4-4f1b-a4a9-efa33f8daf7c.png)
1. Save the annotation (click 'Post')
1. After the annotation is saved, wait max 1 min to receive an email with a notification about mentioning