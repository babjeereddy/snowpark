import streamlit as st
from snowflake.snowpark.context import get_active_session

st.title("AI Document Assistant")

session = get_active_session()

user_query = st.text_input("Enter your question:", placeholder="e.g., How do I set up MFA?")

if user_query:
    with st.spinner("Searching documents and generating answer..."):
        try:
            # 1. Retrieval: Get context from Cortex Search
            # We use a simple string for the JSON to keep it clean
            search_service_name = "doc_search_service"
            search_query_json = f"""
            {{
                "query": "{user_query}",
                "columns": ["search_text"],
                "limit": 3
            }}
            """
            
            search_res = session.sql(f"SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW('{search_service_name}', '{search_query_json}')").collect()
            
            import json
            results_json = json.loads(search_res[0][0])
            context_list = [row['search_text'] for row in results_json['results']]
            full_context = "\n\n".join(context_list)

            if not full_context:
                st.warning("No relevant documents found in the database.")
            else:
                # 2. Generation: Pass context to Cortex.COMPLETE
                prompt = f"Answer the question using ONLY the facts provided.\nFacts: {full_context}\nQuestion: {user_query}"
                
                # Use SQL to call the LLM
                response = session.sql("SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3-70b', ?)", params=[prompt]).collect()
                ai_answer = response[0][0]

                # --- Display Results ---
                st.subheader("Answer")
                st.write(ai_answer)

                # with st.expander("View Source Context"):
                #     st.info(full_context)
                    
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.divider()
st.caption("Powered by Snowflake Cortex AI & Streamlit")