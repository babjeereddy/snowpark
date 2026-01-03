-- RAG (Retrieval-Augmented Generation)

-- RAG is a method where an AI first retrieves relevant information from your data and then generates an answer using that information.

-- RAG = Search your data + Use AI to answer from that data

-- In Snowflake, RAG means: Cortex Search retrieves relevant rows from your tables, and Cortex Complete generates an answer using those rows.


CREATE OR REPLACE TABLE company_docs (
    id INT,
    category STRING,
    search_text STRING
);

ALTER TABLE company_docs SET CHANGE_TRACKING = TRUE;

-- Insert sample data
INSERT INTO company_docs (id, category, search_text) VALUES
(1, 'Security', 'To enable Multi-Factor Authentication (MFA), go to settings and select Security.'),
(2, 'Payroll', 'Direct deposit changes take one full pay cycle to update in the system.'),
(3, 'IT', 'VPN access requires the GlobalProtect client installed on your company laptop.');


CREATE OR REPLACE CORTEX SEARCH SERVICE doc_search_service
  ON search_text               
  ATTRIBUTES id, category      
  WAREHOUSE = compute_wh
  TARGET_LAG = '1 minute'
  AS 
  SELECT id, category, search_text FROM company_docs;


SET user_query = 'How do I set up MFA?';

SET retrieved_context = (
    SELECT LISTAGG(value:search_text::string, '\n\n') 
    FROM TABLE(FLATTEN(INPUT => PARSE_JSON(
        SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
            'doc_search_service', 
            '{"query": "' || $user_query || '", "columns": ["search_text"], "limit": 2}'
        )
    ):results))
);


SELECT $retrieved_context;

--  Generate the final Answer
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'llama3-70b', 
    CONCAT(
        'Answer the question using ONLY the following facts: ',
        '\n\nFacts: ', $retrieved_context, 
        '\n\nQuestion: ', $user_query
    )
) AS ai_response;

