Index Endpoint – Usage Guide
============================

The PLA process is designed to ensure the OrientDB database reflects the detected event entities, particularly when the incoming incident data is inserted into the system. Recognizing that such streams can sometimes experience gaps or "holes," this functionality provides an option to specifically execute the update process for a defined time window. This allows for targeted backfilling or reconciliation of data within a specified period, addressing any inconsistencies that might arise from interruptions in the real-time notification stream and ensuring data integrity within OrientDB.

Endpoint
--------

    GET /Index?start={START}&end={END}&batchSize={BATCH_SIZE}
    

Parameters
----------

*   `start`: `string` (format: `yyyy-MM-ddTHH:mm:ssZ`) – Start date/time in UTC.
*   `end`: `string` (format: `yyyy-MM-ddTHH:mm:ssZ`) – End date/time in UTC.
*   `batchSize`: `integer` (optional, default: 1000) – Number of records per batch.

Example curl Command
--------------------

    curl -X 'GET' \
      'http://pla_host/Index?start=2025-04-29T06:00:00Z&end=2025-04-29T09:00:00Z&batchSize=1000' \
      -H 'accept: text/plain'
    

Successful Response (HTTP 200)
------------------------------

    {
      "version": "1.0.0.0",
      "code": 200,
      "message": null,
      "isError": false,
      "responseException": null,
      "data": {
        "count": 1000,
        "time": "2025-04-29T06:41:56Z"
      }
    }
    

Failure Response (HTTP 500)
---------------------------

If something goes wrong on the server, the endpoint will return:
*   **HTTP Status**: 500 Internal Server Error
*   The response body may vary depending on the exception.

Validation Checklist
--------------------

*   Ensure `start` and `end` dates are in correct UTC format.
*   Ensure `end` is after `start`.
*   Ensure `batchSize` is a positive integer.

> **Note:** Since the PLA service does not have access to the external network (its ports are blocked),  
> you must run this curl command from a container that is on the `plugins` Docker network.

One option is to use the **Data Model Search Service** container.