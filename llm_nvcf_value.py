import streamlit as st

# Function to calculate TCO for managed service and partner DIY
def calculate_tco(gpu_hourly_rate, dl_services_yearly, private_addon_yearly, data_connectivity_yearly, nvidia_nim_yearly, other_software_yearly,
                  storage_yearly, networking_yearly, data_center_yearly, kubernetes_yearly, sre_yearly, data_yearly, security_yearly, update_yearly):
    compute_yearly = gpu_hourly_rate * 24 * 365  # Convert hourly rate to yearly
    managed_service_tco = compute_yearly + dl_services_yearly + private_addon_yearly + data_connectivity_yearly + nvidia_nim_yearly + other_software_yearly
    partner_diy_tco = compute_yearly + storage_yearly + networking_yearly + data_center_yearly + kubernetes_yearly + sre_yearly + data_yearly + security_yearly + update_yearly
    return managed_service_tco, partner_diy_tco

# Function to calculate cost per 1M tokens based on GPU type, processing time, and model size
def calculate_cost_per_million_tokens(gpu_hourly_rate, processing_time_seconds, model_size_billion_parameters):
    processing_time_hours = (processing_time_seconds / 3600.0) * (model_size_billion_parameters / 1)  # Adjusted for model size
    cost_per_million_tokens = gpu_hourly_rate * processing_time_hours
    return cost_per_million_tokens

# Main app
def main():
    st.sidebar.title('Navigation')
    section = st.sidebar.radio('Go to', ['TCO Comparison', 'GPU-Hour to Token Pricing'])

    if section == 'TCO Comparison':
        st.title('LLM Inference TCO Comparison Tool')

        st.header('Managed Service Costs')
        gpu_type_managed = st.selectbox('Select GPU type for Managed Service:', ['A100', 'H100', 'L40S'], key='gpu_type_managed')
        gpu_hourly_rate_managed = st.number_input(f'{gpu_type_managed} Hourly Rate ($):', key='gpu_hourly_rate_managed')

        st.subheader('Upsell Opportunity')
        dl_services_yearly = st.number_input('DL Professional Services Cost (Yearly $):', value=0.0)
        #private_addon_yearly = st.number_input('Private offering add-on (Yearly $):', value=300.0)
        #data_connectivity_yearly = st.number_input('Data connectivity cost (Yearly $):', value=200.0)
        nvidia_nim_yearly = st.number_input('NVIDIA NVIDIA/NIM Cost (Yearly $):', value=4500.0)
        #other_software_yearly = st.number_input('Other Software Cost (Yearly $):', value=100.0)

        st.header('Partner DIY Costs')
        gpu_type_diy = st.selectbox('Select GPU type for Partner DIY:', ['A100', 'H100', 'L40S'], key='gpu_type_diy')
        gpu_hourly_rate_diy = st.number_input(f'{gpu_type_diy} Hourly Rate ($):', key='gpu_hourly_rate_diy')

        storage_yearly = st.number_input('Storage Cost (Yearly $):', value=5000.0)
        networking_yearly = st.number_input('Networking Cost (Yearly $):', value=3000.0)
        data_center_yearly = st.number_input('Data Center Cost (Yearly $):', value=20000.0)
        kubernetes_yearly = st.number_input('Kubernetes/Autoscaling Cost (Yearly $):', value=10000.0)
        sre_yearly = st.number_input('SRE / Human-in-loop Cost (Yearly $):', value=500000.0)
        data_yearly = st.number_input('Data connectivity Cost (Yearly $):', value=400.0)
        security_yearly = st.number_input('Security Cost (Yearly $):', value=400000.0)
        update_yearly = st.number_input('Software Update - versioning and variance cost (Yearly $):', value=100000.0)

        if st.button('Calculate Yearly TCO'):
            managed_service_tco, partner_diy_tco = calculate_tco(
                gpu_hourly_rate_managed, dl_services_yearly, private_addon_yearly, data_connectivity_yearly, nvidia_nim_yearly, other_software_yearly,
                storage_yearly, networking_yearly, data_center_yearly, kubernetes_yearly, sre_yearly, data_yearly, security_yearly, update_yearly)
            st.subheader('Results (Yearly Costs)')
            st.write(f'Managed Service TCO for {gpu_type_managed}: ${managed_service_tco:,.2f}')
            st.write(f'Partner DIY TCO for {gpu_type_diy}: ${partner_diy_tco:,.2f}')
            if managed_service_tco < partner_diy_tco:
                st.success('Managed Service is more cost-effective.')
            else:
                st.error('Partner DIY is more cost-effective.')

    elif section == 'GPU-Hour to Token Pricing':
        st.title('GPU-Hour to Token Pricing Converter')
        gpu_type = st.selectbox('Select GPU type:', ['A100', 'H100', 'L40S'])
        gpu_hourly_rate = st.number_input(f'{gpu_type} Hourly Rate ($):', value=4.0)
        processing_time_seconds = st.number_input('Processing time for 1B*1M tokens (in seconds):', value=60.0)

        # Allow user to add a custom model
        custom_model_name = st.text_input("Custom model name (e.g., Custom-1B):", "")
        custom_model_size = st.number_input("Custom model size in billion parameters:", value=0.0, format="%.2f")

        st.write('### Cost per 1M Tokens for Different Models')
        model_sizes = {'LLaMA-7B': 7, 'LLaMA-13B': 13, 'LLaMA-70B': 70, 'Mistral-7B': 7, 'Mistral-8*7B': 56}
        if custom_model_name and custom_model_size > 0:
            model_sizes[custom_model_name] = custom_model_size  # Add custom model to the dictionary

        for model, size in model_sizes.items():
            cost_per_million_tokens = calculate_cost_per_million_tokens(gpu_hourly_rate, processing_time_seconds, size)
            st.write(f'{model} on {gpu_type}: ${cost_per_million_tokens:.4f} per 1M tokens')

        st.write("""
        **Formula Explanation**:
        The cost to process 1M tokens for a model is calculated based on the GPU's hourly rate and the processing time for the model.
        The processing time is adjusted based on the model size (in billion parameters), assuming linear scaling.
        Formula: Cost per 1M Tokens = GPU Hourly Rate * (Adjusted Processing Time per 1M Tokens / 3600) * Model Size (in billion parameters)
        """)

if __name__ == "__main__":
    main()

