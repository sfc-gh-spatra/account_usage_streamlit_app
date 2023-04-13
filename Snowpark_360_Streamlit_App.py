"""
Created on : Wed Apr 17 12:30 2023
@author: Saurabh Patra
"""

# Import python packages
import time
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Account Usage App")

# Get the current credentials
session = get_active_session()
database= session.get_current_database()
#st.write('Your selected database is ', database)
schema= session.get_current_schema()
#st.write('Your selected schema is ', schema)


#Define Global Variable
#deployment_name=''
#customer_name=''

# Get Customer deployment information
#@st.cache()
def get_deployment_name():
    deployment_name=session.sql(f"select ' ' union all select deployment from finance.customer.deployment")
    return deployment_name


# Get Customer name
#@st.cache()
def get_customer_name(deployment_name):
    account_name=session.sql(f"""select ' ' union all select distinct c.SALESFORCE_ACCOUNT_NAME from finance.customer.contract c 
                                    join finance.customer.subscription s 
                                    on c.salesforce_contract_id = s.salesforce_contract_id where s.snowflake_deployment = '{deployment_name}'""").toPandas()
    return account_name 

deployment_name = st.selectbox('Choose Your Deployment',get_deployment_name())    
st.write('Your selected deployment is ', deployment_name)
    
#if deployment_name != ' ':
    #st.spinner('Wait for the deployment to be selected...')
customer_name = st.selectbox('Choose Your Customer',(get_customer_name(deployment_name)))
st.write('You selected:', customer_name)

# Get replication group details
@st.cache()
def get_replication_group(customer_name):
    replication_group=session.sql(f"""select distinct ORGANIZATION_ETL_V.replication_group from finance.customer.contract 
                                        join snowhouse_import.prod.ORGANIZATION_ETL_V on contract.salesforce_account_id = ORGANIZATION_ETL_V.SALESFORCE_ID 
                                        join  snowhouse_import.prod.account_etl_v on ORGANIZATION_ETL_V.replication_group = account_etl_v.replication_group 
                                        where contract.salesforce_account_name in ('{customer_name}') and AGREEMENT_TYPE = 'Capacity' 
                                        and CONTRACT_STATUS = 'Activated'""").toPandas()
    st.spinner('Your data is being retreived...')
    return replication_group    

#Get schema details
#@st.cache()
def get_schema_details():
    schema_name=session.sql(f"select schema_name from information_schema.schemata").toPandas()
    return schema_name

# Get Replication group value
distinct_replication_group=get_replication_group(customer_name).values.tolist()
lenght_of_replication_group=len(get_replication_group(customer_name).values.tolist())
if (lenght_of_replication_group>0):
    drg=distinct_replication_group[0][0]
    #st.write(drg)
    schema_name = st.selectbox('Choose Your Schema where the views will be created',get_schema_details())    
    st.write('You selected:',schema_name)
    if st.button('Do you want to proceed with view creation'):
        with st.spinner('Wait for it...'):
            time.sleep(5)
            session.sql(f"""call temp.util.account_usage_view_deploy('{deployment_name}','{drg}','{schema_name}')""").collect()
        st.snow()
        st.success('Done! Have a look into the Schema for the newly created Views')
    else:
        st.error('Check The Query History to track the error', icon="🚨")
else:
     st.write('Your Replication Group is not found')

