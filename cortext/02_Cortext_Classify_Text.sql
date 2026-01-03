-- CLASSIFY_TEXT() is a Snowflake Cortex AI function used to automatically categorize (classify) text into predefined labels based on its meaning.

-- It answers the question:

-- “Which category does this text belong to?”


--simple classification

SELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
  'Booked flight to Delhi for client meeting',
  ['Travel','Meals','Office']
) ['label']::string AS simple_classification;

-- Classify accounting expense'
SELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
  'Lunch with vendor',
  ['Travel','Meals','Professional Fees']  
)['label']::string AS accounting_expenses;

--Classify HR request type

SELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
  'I want to apply for earned leave next Friday',
  ['Leave','Payroll','Recruitment','Policy']
) ['label']::string AS hr_request;


--Email Intent Classification

SELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
  'Please cancel my subscription and refund the amount',
  ['Cancellation','Refund','Enquiry','Complaint']
)['label']::string AS cancalation;

--Customer Feedback Sentiment Type
SELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
  'Delivery was late but customer support handled it well',
  ['Positive','Neutral','Negative']
)['label']::string AS feedback_type;

--HR Query Categorization

SELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
  'I want to apply for earned leave next Friday',
  ['Leave','Payroll','Recruitment','Policy']
)['label']::string AS hr_category;

--Compliance / Audit Observation Tagging
SELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
  'Vendor invoice does not have GST registration number',
  ['GST Non-Compliance','Documentation Issue','Pricing Issue']
)['label']::string AS audit_finding;



