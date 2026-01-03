--AI function that pulls specific structured information from unstructured text.


SELECT SNOWFLAKE.CORTEX.EXTRACT_ANSWER(
  'The order was shipped on 12th June and delivered on 15th June.',
  'When was the order delivered?'
) AS answer;


CREATE OR REPLACE TABLE support_ticket (
    ticket_id        NUMBER,
    customer_name    VARCHAR,
    ticket_date      DATE,
    issue_type       VARCHAR,
    priority         VARCHAR,
    ticket_text      VARCHAR
);

INSERT INTO support_ticket VALUES
(1001, 'Ramesh Kumar', '2025-01-05', 'Delivery', 'High',
 'The order was placed on 1st January 2025. It was shipped on 3rd January and delivered on 6th January 2025. The delivery was delayed by one day.'),

(1002, 'Anita Sharma', '2025-01-06', 'Refund', 'Medium',
 'I cancelled my order on 2nd January 2025. The refund amount of ₹2,500 was promised within 7 working days but has not yet been credited.'),

(1003, 'Vikram Rao', '2025-01-07', 'Product', 'Low',
 'The product quality is good and I am satisfied with the purchase. No further issues.'),

(1004, 'Sneha Iyer', '2025-01-08', 'Support', 'High',
 'I contacted customer support on 5th January 2025 regarding a login issue. The issue was resolved on 6th January 2025.'),

(1005, 'Arjun Mehta', '2025-01-09', 'Delivery', 'High',
 'The order was supposed to be delivered on 8th January 2025 but is still pending. Please confirm the expected delivery date.'),

(1006, 'Pooja Nair', '2025-01-10', 'Billing', 'Medium',
 'I was charged twice for the same order on 7th January 2025. The extra amount needs to be refunded.'),

(1007, 'Suresh Patel', '2025-01-11', 'Refund', 'High',
 'The refund of ₹1,200 was initiated on 4th January 2025 and credited on 10th January 2025.'),

(1008, 'Neha Verma', '2025-01-12', 'Delivery', 'Low',
 'The order was delivered on time on 11th January 2025. Very happy with the service.');


 SELECT
  ticket_id,
  SNOWFLAKE.CORTEX.EXTRACT_ANSWER(
    ticket_text,
    'When was the order delivered?'
  ) AS delivery_date
FROM support_ticket;

-- Combined Cortex Query

SELECT
  ticket_id,
  priority,
  SNOWFLAKE.CORTEX.SENTIMENT(ticket_text) AS sentiment,
  SNOWFLAKE.CORTEX.EXTRACT_ANSWER(
    ticket_text,
    'What is the refund amount?'
  ) AS refund_amount
FROM support_ticket;






