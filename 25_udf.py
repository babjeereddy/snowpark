from snowflake.snowpark import Session
from snowflake.snowpark.functions import udf, col
from snowflake.snowpark.types import StringType
session = Session.builder.config("connection_name", "default").create()

def to_lower_py(text: str) -> str:
    if text is None:
        return None
    return text.lower()

session.udf.register(
    func=to_lower_py,
    name="to_lower_udf",
    return_type=StringType(),
    input_types=[StringType()],
    is_permanent=True,
    stage_location="@udf_stage",
    replace=True
)

df = session.table("orders1")
session.sql("""
    select ORDER_ID,
              TO_LOWER_UDF(STATUS) as status_lower
    from orders1 
""").show()
