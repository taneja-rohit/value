import streamlit as st

# Function to calculate TCO for managed service
def calculate_managed_service_tco(compute_cost, storage_cost, networking_cost, data_center_cost):
    return compute_cost + storage_cost + networking_cost + data_center_cost

# Function to calculate TCO for customer-built environment
def calculate_customer_built_tco(compute_cost, storage_cost, networking_cost, data_center_cost, kubernetes_cost):
    return compute_cost + storage_cost + networking_cost + data_center_cost + kubernetes_cost

# Function to convert token pricing to GPU per hour pricing
def convert_token_to_gpu_pricing(cost_per_1000_tokens, tokens_per_request, processing_time_per_request, requests_per_hour):
    # Calculate cost per request
    cost_per_request = (cost_per_1000_tokens / 1000) * tokens_per_request
    # Calculate total cost per hour
    total_cost_per_hour = cost_per_request * requests_per_hour
    return total_cost_per_hour

# Streamlit UI for TCO comparison
st.title('LLM Inference TCO Comparison Tool')

# Managed Service Costs
st.header('Managed Service Costs')
ms_compute_cost = st.number_input('Compute Cost ($)', value=1000.0, key='ms_compute')
ms_storage_cost = st.number_input('Storage Cost ($)', value=500.0, key='ms_storage')
ms_networking_cost = st.number_input('Networking Cost ($)', value=300.0, key='ms_networking')
ms_data_center_cost = st.number_input('Data Center Cost ($)', value=200.0, key='ms_data_center')

# Customer-Built Environment Costs
st.header('Customer-Built Environment Costs')
cb_compute_cost = st.number_input('Compute Cost ($)', value=1000.0, key='cb_compute')
cb_storage_cost = st.number_input('Storage Cost ($)', value=500.0, key='cb_storage')
cb_networking_cost = st.number_input('Networking Cost ($)', value=300.0, key='cb_networking')
cb_data_center_cost = st.number_input('Data Center Cost ($)', value=200.0, key='cb_data_center')
cb_kubernetes_cost = st.number_input('Kubernetes/Autoscaling Cost ($)', value=400.0, key='cb_kubernetes')

# Token to GPU Pricing Conversion
st.header('Token to GPU Pricing Conversion')
cost_per_1000_tokens = st.number_input('Cost per 1,000 Tokens ($)', value=3.0)
tokens_per_request = st.number_input('Tokens per Request', value=4000.0)
processing_time_per_request = st.number_input('Processing Time per Request (seconds)', value=1.3)  # Based on [1]
requests_per_hour = st.number_input('Requests per Hour', value=3600 / processing_time_per_request)

if st.button('Calculate TCO'):
    ms_tco = calculate_managed_service_tco(ms_compute_cost, ms_storage_cost, ms_networking_cost, ms_data_center_cost)
    cb_tco = calculate_customer_built_tco(cb_compute_cost, cb_storage_cost, cb_networking_cost, cb_data_center_cost, cb_kubernetes_cost)
    gpu_cost_per_hour = convert_token_to_gpu_pricing(cost_per_1000_tokens, tokens_per_request, processing_time_per_request, requests_per_hour)
    
    st.subheader('Results')
    st.write(f'Managed Service TCO: ${ms_tco}')
    st.write(f'Customer-Built Environment TCO: ${cb_tco}')
    st.write(f'Equivalent GPU Cost per Hour: ${gpu_cost_per_hour:.2f}')
    
    if ms_tco < cb_tco:
        st.success('Managed Service is more cost-effective.')
    else:
        st.error('Customer-Built Environment is more cost-effective.')
