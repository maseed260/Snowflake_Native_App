-- ===============================================================
-- This script runs when the app is installed 
-- ===============================================================

-- Create Application Role and Schema
create application role if not exists data_quality_control_app_role;
create or alter versioned schema app_instance_schema;

-- Create Streamlit app
create or replace streamlit app_instance_schema.DQC_STREAMLIT from '/libraries' main_file='app.py';

CREATE or replace PROCEDURE app_instance_schema.register_reference(ref_name STRING, operation STRING, ref_or_alias STRING)
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
	CASE (operation)
	WHEN 'ADD' THEN
		SELECT SYSTEM$SET_REFERENCE(:ref_name, :ref_or_alias);
	WHEN 'REMOVE' THEN
		SELECT SYSTEM$REMOVE_REFERENCE(:ref_name);
	WHEN 'CLEAR' THEN
		SELECT SYSTEM$REMOVE_REFERENCE(:ref_name);
	ELSE
	RETURN 'unknown operation: ' || operation;
	END CASE;
	RETURN NULL;
END;
$$;

-- Grant usage and permissions on objects
grant usage on schema app_instance_schema to application role data_quality_control_app_role;
grant usage on streamlit app_instance_schema.DQC_STREAMLIT to application role data_quality_control_app_role;
GRANT USAGE ON PROCEDURE app_instance_schema.register_reference(STRING, STRING, STRING) TO APPLICATION ROLE data_quality_control_app_role;
