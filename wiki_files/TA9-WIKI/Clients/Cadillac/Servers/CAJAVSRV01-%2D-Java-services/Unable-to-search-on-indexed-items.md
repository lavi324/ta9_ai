# Unable to search indexed items such as: Document + Emails

Issue:
when trying to search on a DM that is indexed to federated, getting the error "Bad Request"

Solution:
Make sure all fields in dataschemafields1 exists in Solar manage schema.

In order to fix this in Cadillac ENV we needed to change 2 files in Solr managed schema.(observe attachments)

One line added to datamodel managed schema and Freetextindex managed schema:

<field name="system_comment" type="text_general" multiValued="false" indexed="true" stored="false"/>
