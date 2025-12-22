[[_TOC_]]
# Intro
IntSight can send emails on some events, such as file loading completion, mentioning a user and so on

# Guide
In order to make it work, just the following configuration items need to be set (system config table `sqlite_metadata.system_config`):

|Key|Sample  |
|--|--|
| MailSettings_user	 | services@t-a9.com |
|  MailSettings_password	| ********** |
|  MailSettings_from	| services@t-a9.com |
| MailSettings_fromDisplay	 |  IntSight Mailer|
| MailSettings_host	 | smtp.office365.com |
| MailSettings_port	 | 587 |
|  MailSettings_ssl	| true |

These are just an example, every environment need to be configured according to its mailing service.