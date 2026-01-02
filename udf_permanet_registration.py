from snowflake.snowpark.types import IntegerType, StringType
from snowflake.snowpark.functions import col
from snowflake.snowpark import Session
session = Session.builder \
    .config("connection_name", "default").create()

    

def word_count(s: str) -> int:
    if s is None:
        return 0
    return len(s.split())

session.udf.register(
    func=word_count,
    name="WORD_COUNT_UDF",
    return_type=IntegerType(),
    input_types=[StringType()],
    is_permanent=True,
    stage_location="@udf_stage",
    replace=True
)
print("UDF registered successfully.")   

session.sql("""
    select WORD_COUNT_UDF('Snowflake Snowpark UDF permanent registration example') 
            as word_count""").show()