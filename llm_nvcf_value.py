import streamlit as st

# Function to calculate TCO for managed service
def calculate_managed_service_tco(nvcf_pricing, dl_services_cost, private_addon_cost, data_connectivity_cost, nvidia_nim_cost, other_software_cost):
    return nvcf_pricing + dl_services_cost + private_addon_cost + data_connectivity_cost + nvidia_nim_cost + other_software_cost

# Function to calculate TCO for customer-built environment
def calculate_customer_built_tco(compute_cost, storage_cost, networking_cost, data_center_cost, kubernetes_cost, sre_cost, data_cost, security_cost, update_cost):
    return compute_cost + storage_cost + networking_cost + data_center_cost + kubernetes_cost + sre_cost + data_cost + security_cost + update_cost

# Function to convert token pricing to GPU per hour pricing
def convert_token_to_gpu_pricing(cost_per_1000_tokens, tokens_per_request, requests_per_hour):
    cost_per_request = (cost_per_1000_tokens / 1000) * tokens_per_request
    total_cost_per_hour = cost_per_request * requests_per_hour
    return total_cost_per_hour

# Sidebar for navigation
st.sidebar.title('Navigation')
section = st.sidebar.radio('Go to', ['TCO Comparison', 'Token to GPU-Hour Pricing'])

if section == 'TCO Comparison':
    st.title('LLM Inference TCO Comparison Tool')

    # Managed Service Costs
    st.header('Managed Service Costs')
    ms_compute_cost = st.number_input('NVCF pricing ($)', value=1000.0, key='ms_compute')
    ms_storage_cost = st.number_input('DL Professional Services Cost ($)', value=500.0, key='ms_storage')
    ms_networking_cost = st.number_input('Private offering add-on ($)', value=300.0, key='ms_networking')
    ms_data_center_cost = st.number_input('Data connectivity cost ($)', value=200.0, key='ms_data_center')
    ms_nvidia_nim_cost = st.number_input('NVIDIA NIM Cost ($)', value=100.0, key='ms_nvidia_nim')
    ms_other_software_cost = st.number_input('Other Software Cost ($)', value=100.0, key='ms_other_software')

    # Customer-Built Environment Costs
    st.header('Customer-Built Environment Costs')
    cb_compute_cost = st.number_input('Compute Cost ($)', value=1000.0, key='cb_compute')
    cb_storage_cost = st.number_input('Storage Cost ($)', value=500.0, key='cb_storage')
    cb_networking_cost = st.number_input('Networking Cost ($)', value=300.0, key='cb_networking')
    cb_data_center_cost = st.number_input('Data Center Cost ($)', value=200.0, key='cb_data_center')
    cb_kubernetes_cost = st.number_input('Kubernetes/Autoscaling Cost ($)', value=400.0, key='cb_kubernetes')
    cb_sre_cost = st.number_input('SRE / Human-in-loop Cost ($)', value=400.0, key='cb_sre')
    cb_data_cost = st.number_input('Data connectivity Cost ($)', value=400.0, key='cb_data')
    cb_security_cost = st.number_input('Security Cost ($)', value=400.0, key='cb_security')
    cb_update_cost = st.number_input('Software Update - versioning and variance cost ($)', value=400.0, key='cb_update')

    # Calculate TCO button
    if st.button('Calculate TCO'):
        ms_tco = calculate_managed_service_tco(ms_compute_cost, ms_storage_cost, ms_networking_cost, ms_data_center_cost, ms_nvidia_nim_cost, ms_other_software_cost)
        cb_tco = calculate_customer_built_tco(cb_compute_cost, cb_storage_cost, cb_networking_cost, cb_data_center_cost, cb_kubernetes_cost, cb_sre_cost, cb_data_cost, cb_security_cost, cb_update_cost)
        
        st.subheader('Results')
        st.write(f'Managed Service TCO: ${ms_tco}')
        st.write(f'Customer-Built Environment TCO: ${cb_tco}')
        
        if ms_tco < cb_tco:
            st.success('Managed Service is more cost-effective.')
        else:
            st.error('Customer-Built Environment is more cost-effective.')

elif section == 'Token to GPU-Hour Pricing':
    st.title('Token to GPU-Hour Pricing Converter')

    cost_per_1000_tokens = st.number_input('Cost per 1,000 Tokens ($)', value=3.0)
    tokens_per_request = st.number_input('Tokens per Request', value=4000.0)
    requests_per_hour = st.number_input('Requests per Hour', value=1000.0)

    if st.button('Convert Pricing'):
        gpu_cost_per_hour = convert_token_to_gpu_pricing(cost_per_1000_tokens, tokens_per_request, requests_per_hour)
        st.write(f'Equivalent GPU Cost per Hour: ${gpu_cost_per_hour:.2f}')
