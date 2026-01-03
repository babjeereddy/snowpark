create database trainiing;


-- Snowflake Cortex Search is an AI-powered s search feature in Snowflake.
-- It lets you search text by meaning, not just exact words.
-- You ask a natural-language question, and Cortex finds the most relevant text from your data.
-- Think of it as Google-style search inside Snowflake tables.

CREATE OR REPLACE TABLE faq_docs (
  id INT,
  content STRING
);

INSERT INTO faq_docs VALUES
(1, 'You can reset your password using the Forgot Password link'),
(2, 'Refunds are processed within 7 business days'),
(3, 'Contact support by emailing support@company.com');



CREATE OR REPLACE CORTEX SEARCH SERVICE faq_search
ON content
WAREHOUSE = compute_wh
TARGET_LAG = '1 hour'
AS
SELECT id, content FROM faq_docs;

SHOW CORTEX SEARCH SERVICES;

GRANT USAGE ON CORTEX SEARCH SERVICE  faq_search to  ACCOUNTADMIN;

DESCRIBE CORTEX SEARCH SERVICE faq_search;

SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'faq_search',
    '{
        "query": "How do I get my money back?",
        "columns": ["id", "content"],
        "limit": 2
    }'
) AS OUTPUT;


SELECT 
    value:id::string AS id,
    value:content::string AS content,
    value:"@scores".cosine_similarity::float AS semantic_score
FROM TABLE(FLATTEN(INPUT => PARSE_JSON(
    SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
        'faq_search',
        '{"query": "How do I get my money back?", "columns": ["id", "content"], "limit": 2}'
    )
):results));


SELECT 
    value:id::string AS id,
    value:content::string AS content,
    value:"@scores".cosine_similarity::float AS score
FROM TABLE(
    FLATTEN(
        INPUT => PARSE_JSON(
            SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                'faq_search',
                '{
                    "query": "I forgot my password",
                    "columns": ["id", "content"],
                    "limit": 3
                }'
            )
        ):results
    )
);



SELECT 
    value:id::string AS id,
    value:content::string AS content,
    value:"@scores".cosine_similarity::float AS semantic_score
FROM TABLE(FLATTEN(INPUT => PARSE_JSON(
    SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
        'faq_search',
        '{"query": "how do i reset my password", "columns": ["id", "content"], "limit": 2}'
    )
):results));
