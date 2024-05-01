# Import python packages
import streamlit as st
import snowflake.permissions as perms
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

# Setting page config to wide
st.set_page_config(layout="wide")

# Initializing session state
if "submitted" not in st.session_state:
    st.session_state.submitted = False

def main(session):
    st.title(f"**:blue[Data Quality App]**")
    st.write("---")
    snow_df = session.sql("select * from reference('consumer_table')")

    st.write(f"**➥ Preview of :blue[selected table] table**")
    st.dataframe(snow_df.limit(5), height=220)

    st.write(f"**➥ Select data quality checks using the below input form**")
    with st.form('Data quality check selection form', clear_on_submit=False):
        null_check = st.selectbox('Null check', snow_df.columns)
        unique_check = st.selectbox('Unique check', snow_df.columns)
        st.session_state.submitted = st.form_submit_button(label="**:green[Submit]**")

    if st.session_state.submitted:
        st.write("---")
        st.write(f"**➥ Below is the test report**")
        unique_check_result = snow_df.groupBy(col(f'"{unique_check}"')).count().filter(col("count") > 1)
        if unique_check_result.count() > 0:
                st.error(f"**Unique Check failed on column : {unique_check}. The below are column values with duplicates**")
                st.dataframe(unique_check_result, use_container_width=True)
        if unique_check_result.count() == 0:
            st.success(f"**The column :blue[{null_check}] has passed UNIQUE check in the selected table**")
            
        null_check_result = snow_df.where(col(f'"{null_check}"').isNull())
        if null_check_result.count() > 0:
                st.error(f"**Unique Check failed on column : {null_check}. The below are column values with Nulls**")
                st.dataframe(null_check_result, use_container_width=True)
        if null_check_result.count() == 0:
            st.success(f"**The column :blue[{null_check}] has passed NULL check in the selected table**")
        st.session_state.submitted = False


# Check if the app has select privs on a table
if not perms.get_reference_associations("consumer_table"):
    perms.request_reference("consumer_table")

else:
    # Get the current credentials
    session = get_active_session()
    main(session)
