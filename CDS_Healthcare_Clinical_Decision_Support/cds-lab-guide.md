# Fivetran Connector SDK Hands on Lab at Snowflake Summit 2025: Healthcare Clinical Decision Support

## Overview
In this 20-minute hands on lab, you'll build a **custom Fivetran connector** using the **Fivetran Connector SDK** and the **Anthropic Workbench** to integrate healthcare data from a custom REST API into Snowflake. You'll then create a **Streamlit in Snowflake** application powering healthcare metrics and **Snowflake Cortex AI-driven** clinical decision support applications.

The Healthcare CDS custom connector should fetch clinical decision support records from a REST API and load them into a single table called `cds_records` in your Snowflake database. The connector should deliver detailed information about patient records, medical histories, lab results, diagnoses, treatments, clinical trials, and various healthcare performance metrics. It should handle authentication, pagination, error handling, and maintain state between sync runs using a cursor-based approach.

## Lab Steps Quick Access

- [Step 1: Create a Custom Connector with the Fivetran Connector SDK (8 minutes)](#step-1-create-a-custom-connector-with-the-fivetran-connector-sdk-8-minutes)
- [Step 2: Start Data Sync in Fivetran (3 minutes)](#step-2-start-data-sync-in-fivetran-3-minutes)
- [Step 3: Create a Streamlit in Snowflake Gen AI Data App (5 minutes)](#step-3-create-a-streamlit-in-snowflake-gen-ai-data-app-5-minutes)

## Lab Environment
- MacBook Pro laptop with Chrome browser, VS Code, DBeaver and the Fivetran Connector SDK
- 6 Chrome tabs are pre-configured (leave them open throughout the lab):
  - Tab 1: GitHub Lab Repo: Lab Guide
  - Tab 2: Anthropic Workbench: AI Code Generation Assistant (Claude)
  - Tab 3: Fivetran: Automated Data Movement Platform
  - Tab 4: Snowflake: Data and AI Platform including Cortex (AI functions) and Streamlit (data apps)
  - Tab 5: Fivetran Connector SDK Examples Open Source Github Repository
  - Tab 6: Fivetran Connector SDK Docs

## Mac Keyboard Shortcuts Reference
- **Command+A**: Select all
- **Command+C**: Copy
- **Command+V**: Paste
- **Command+S**: Save
- **Command+Tab**: Switch between applications
- **Control+`**: Open terminal in VS Code

## Trackpad/MousePad Reference
- **Single finger tap**: Left click
- **Two finger tap**: Right click
- **Two finger slide**: Scroll up and down

## Step 1: Create a Custom Connector with the Fivetran Connector SDK (8 minutes)

### 1.1 Generate the Custom Connector Code Using AI Code Generation Assistance
1. Switch to **Chrome Tab 2 (Anthropic Workbench)**
2. Copy and paste the following **User prompt** into the workbench:

<details>
  <summary>Click to expand the User prompt and click the Copy icon in the right corner</summary>

```
- Provide a custom connector for Healthcare for the cds_data endpoint. 1 table called cds_records - all columns.  
- Make sure you copy the configuration.json file exactly - do not add any other variables to it.
- Here is the API spec: https://sdk-demo-api-dot-internal-sales.uc.r.appspot.com/cds_api_spec
```
</details>

3. Click the black **Run** button in the upper right
4. After Claude generates the connector.py code, you will see a response similar to the example connector, but updated for the healthcare dataset.
5. Click [cds_data](https://sdk-demo-api-dot-internal-sales.uc.r.appspot.com/cds_data) if you'd like to see the dataset.
 
### 1.2 Debug and Deploy the Custom Connector in VS Code
1. When you see the connector.py code generated in the Anthropic Workbench, click the **Copy** button in the upper right of the code connector.py code block
2. Go to **VS Code** with Command + Tab or open from the dock
3. Click on the `connector.py` file in your project
4. Press Command+V to paste the connector code into the `connector.py` file
5. Save the updated `connector.py` by pressing Command+S
6. To test your code locally with configuration values specified in `configuration.json`, you can run the default Fivetran Connector SDK debug command:  
   `fivetran debug --configuration configuration.json`  
   This command provides out-of-the-box debugging without any additional scripting. 
7. We have created a helper script to debug and validate your connector with enhanced logging, state clearing and data validation. To run the helper script please run it in the VS Code terminal (bottom right). You can copy the `debug_and_validate` command using the icon on the right:

```
./debug_and_validate.sh
```

8. When prompted with "Do you want to continue? (Y/N):", type `Y` and press Enter.

    - You'll see output displaying the results of the debug script including:

        - Resets the connector state by deleting the existing warehouse.db file and any saved sync checkpoints to start with a clean slate.

        - Runs the fivetran debug command using your configuration file to test the connector in real time.(debug emulates a regular Fivetran sync where the schema() and update() methods are called).

        - Excute the Custom `Connector.py` code you wrote fetching data and executing pagination and checkpoint saving for incremental sync as per your custom code and the current state variable. The helper script emulates an initial full sync.

        - Verifies data loading and schema creation by simulating a full sync (in this case, upserting 750 records into cds_records).

        - Queries and displays sample records from the resulting DuckDB table to confirm the connector outputs expected data.

9. Fivetran provides a built-in command to deploy your connector directly using the SDK:  
   `fivetran deploy --api-key <BASE64_API_KEY> --destination <DESTINATION_NAME> --connection <CONNECTION_NAME>`  
   This command deploys your code to Fivetran and creates or updates the connection. If the connection already exists, it prompts you before overwriting.  
   You can also provide additional optional parameters:  
   - `--configuration` to pass configuration values  
   - `--force` to bypass confirmation prompts, great for CI/CD uses  
   - `--python-version` to specify Python runtime  
   - `--hybrid-deployment-agent-id` for non-default hybrid agent selection  

10. To simplify the lab experience, we’ve created a helper script that wraps the deploy logic. Run the following command in the VS Code terminal (copy the command using the icon in the right corner):

```
./deploy.sh
```

11. Click enter twice to accept the default values for the Fivetran Account Name and the Fivetran Destination. When prompted for the **connection name**, type in:

```
cds_healthcare_connector
```

11. Press Enter to deploy your new custom connector to Fivetran.

## Step 2: Start Data Sync in Fivetran (3 minutes)

1. Switch to **Chrome Tab 3 (Fivetran Automated Data Movement)**
2. Refresh the page and find your newly created connection named "healthcare-cds-connector" in the connections list
3. Click on the connection to open the **Status** page
4. Click the **Start Initial Sync** button
5. You should see a status message indicating that the sync is **Active** and that it is the first time syncing data for this connection.
     * you may need to refresh the UI to see updated sync progress and logs in the UI. 
7. Once your sync completes, you will see a message "Next sync will run in x hours" and if you click on the **1 HOUR** selection on the right side, you will see some sync metrics.

## Step 3: Create a Streamlit in Snowflake Gen AI Data App (5 minutes)

### 3.1 Copy the Streamlit Data App Code
1. Copy the Streamlit code below (click the Copy icon in the right corner)

<details>
  <summary>Click to expand the Streamlit Data App Code and click the Copy icon in the right corner</summary>

```python
import streamlit as st
import pandas as pd
import altair as alt
import time
import json
import re
from datetime import datetime
from snowflake.snowpark.context import get_active_session

st.set_page_config(
    page_title="medmind_–_ai_driven_clinical_decision_support",
    page_icon="https://i.imgur.com/Og6gFnB.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

solution_name = '''Solution 1: MedMind – AI-driven Clinical Decision Support'''
solution_name_clean = '''medmind_–_ai_driven_clinical_decision_support'''
table_name = '''CDS_RECORDS'''
table_description = '''Consolidated patient data for MedMind AI-driven clinical decision support'''
solution_content = '''Solution 1: MedMind – AI-driven Clinical Decision Support**

* **Tagline:** "Transforming patient care with AI-driven insights"
* **Primary Business Challenge:** Reducing medical errors and improving patient outcomes
* **Key Features:**
	+ AI-driven clinical decision support system
	+ Integration with Electronic Health Records (EHRs)
	+ Real-time patient data analysis
	+ Personalized treatment recommendations
* **Data Sources:**
	+ Electronic Health Records (EHRs): Epic Systems Corporation, Cerner, Meditech
	+ Clinical Trials: ClinicalTrials.gov, National Institutes of Health (NIH)
	+ Medical Literature: PubMed, National Library of Medicine
* **Competitive Advantage:** MedMind differentiates itself from traditional clinical decision support systems by leveraging generative AI to analyze vast amounts of patient data and provide personalized treatment recommendations.
* **Key Stakeholders:** Chief Medical Officer, Chief Information Officer, Clinical Decision Support Teams
* **Technical Approach:** Generative AI using deep learning algorithms to analyze patient data and generate personalized treatment recommendations
* **Expected Business Results:**
	+ 10% reduction in medical errors
	+ 15% improvement in patient outcomes
	+ 20% reduction in hospital readmissions
	+ 5% reduction in healthcare costs
* **Calculations:**
	+ 10% reduction in medical errors: **100,000 patients/year × 10% baseline error rate × 10% reduction = 1,000 fewer medical errors/year**
	+ 15% improvement in patient outcomes: **10,000 patients/year × 20% baseline complication rate × 15% reduction = 300 fewer complications/year**
	+ 20% reduction in hospital readmissions: **5,000 patients/year × 20% baseline readmission rate × 20% reduction = 200 fewer readmissions/year**
	+ 5% reduction in healthcare costs: **$ 10,000,000 annual healthcare costs × 5% reduction = $ 500,000 savings/year**
* **Success Metrics:** Reduction in medical errors, improvement in patient outcomes, reduction in hospital readmissions, reduction in healthcare costs
* **Risk Assessment:** Integration with EHRs, data quality, regulatory compliance
* **Long-term Evolution:** Integration with wearable devices, telemedicine, and personalized medicine

**'''

# Display logo and title inline
st.markdown(f'''
<div style="display:flex; align-items:center; margin-bottom:15px">
    <img src="https://i.imgur.com/Og6gFnB.png" width="100" style="margin-right:15px">
    <div>
        <h1 style="font-size:2.2rem; margin:0; padding:0">{solution_name_clean.replace('_', ' ').title()}</h1>
        <p style="font-size:1.1rem; color:gray; margin:0; padding:0">Fivetran and Cortex-powered Streamlit in Snowflake data application for Healthcare</p>
    </div>
</div>
''', unsafe_allow_html=True)

# Define available models as strings
MODELS = [
    "claude-4-sonnet", "claude-3-7-sonnet", "claude-3-5-sonnet", "llama3.1-8b", "llama3.1-70b", "llama4-maverick", "llama4-scout", "llama3.2-1b", "snowflake-llama-3.1-405b", "snowflake-llama-3.3-70b", "mistral-large2", "mistral-7b", "deepseek-r1", "snowflake-arctic", "reka-flash", "jamba-instruct", "gemma-7b"
]

if 'insights_history' not in st.session_state:
    st.session_state.insights_history = []

if 'data_cache' not in st.session_state:
    st.session_state.data_cache = {}

try:
    session = get_active_session()
except Exception as e:
    st.error(f"❌ Error connecting to Snowflake: {str(e)}")
    st.stop()

def query_snowflake(query):
    try:
        return session.sql(query).to_pandas()
    except Exception as e:
        st.error(f"Query failed: {str(e)}")
        return pd.DataFrame()

def load_data():
    query = f"SELECT * FROM {table_name} LIMIT 1000"
    df = query_snowflake(query)
    df.columns = [col.lower() for col in df.columns]
    return df

def call_cortex_model(prompt, model_name):
    try:
        cortex_query = "SELECT SNOWFLAKE.CORTEX.COMPLETE(?, ?) AS response"
        response = session.sql(cortex_query, params=[model_name, prompt]).collect()[0][0]
        return response
    except Exception as e:
        st.error(f"❌ Cortex error: {str(e)}")
        return None

def generate_insights(data, focus_area, model_name):
    data_summary = f"Table: {table_name}\n"
    data_summary += f"Description: {table_description}\n"
    data_summary += f"Records analyzed: {len(data)}\n"

    # Calculate basic statistics for numeric columns
    numeric_stats = {}
    key_metrics = ["readmission_risk", "medical_error_rate", "patient_outcome_score", "cost_of_care", "length_of_stay", "medication_cost", "total_cost_savings"]
    for col in key_metrics:
        if col in data.columns:
            numeric_stats[col] = {
                "mean": data[col].mean(),
                "min": data[col].min(),
                "max": data[col].max(),
                "std": data[col].std()
            }
            data_summary += f"- {col} (avg: {data[col].mean():.2f}, min: {data[col].min():.2f}, max: {data[col].max():.2f})\n"

    # Get top values for categorical columns
    categorical_stats = {}
    categorical_options = ["patient_id", "medical_history", "current_medications", "lab_results", "vital_signs", "diagnosis", "treatment_plan", "clinical_trial_id", "trial_name", "trial_status", "medical_publication_id", "publication_title", "medication_side_effects", "allergies", "medical_conditions", "family_medical_history", "genetic_data", "treatment_outcome", "medication_adherence", "patient_satisfaction", "medication_recommendation", "treatment_recommendation"]
    for cat_col in categorical_options:
        if cat_col in data.columns:
            top = data[cat_col].value_counts().head(3)
            categorical_stats[cat_col] = top.to_dict()
            data_summary += f"\nTop {cat_col} values:\n" + "\n".join(f"- {k}: {v}" for k, v in top.items())

    # Calculate correlations if enough numeric columns available
    correlation_info = ""
    if len(key_metrics) >= 2:
        try:
            correlations = data[key_metrics].corr()
            # Get the top 3 strongest correlations (absolute value)
            corr_pairs = []
            for i in range(len(correlations.columns)):
                for j in range(i+1, len(correlations.columns)):
                    col1 = correlations.columns[i]
                    col2 = correlations.columns[j]
                    corr_value = correlations.iloc[i, j]
                    corr_pairs.append((col1, col2, abs(corr_value), corr_value))

            # Sort by absolute correlation value
            corr_pairs.sort(key=lambda x: x[2], reverse=True)

            # Add top correlations to the summary
            if corr_pairs:
                correlation_info = "Top correlations between metrics:\n"
                for col1, col2, _, corr_value in corr_pairs[:3]:
                    correlation_info += f"- {col1} and {col2}: r = {corr_value:.2f}\n"
        except:
            correlation_info = "Could not calculate correlations between metrics.\n"

    # Define specific instructions for each focus area
    focus_area_instructions = {
        "Overall Performance": """
        For the Overall Performance analysis of MedMind:
        1. Provide a comprehensive analysis of the clinical decision support system's performance using patient outcome scores, treatment outcomes, and medical error rates
        2. Identify significant patterns in medication recommendations, patient outcomes, and readmission risks
        3. Highlight 3-5 key healthcare metrics that best indicate clinical effectiveness (patient outcome scores, medical error rates, readmission risks)
        4. Discuss both clinical strengths and areas for improvement in treatment recommendations
        5. Include 3-5 actionable insights for improving patient care based on the data
        
        Structure your response with these healthcare-focused sections:
        - Clinical Insights (5 specific insights with supporting patient data)
        - Patient Outcome Trends (3-4 significant trends in treatment effectiveness)
        - Clinical Recommendations (3-5 data-backed recommendations for improving care)
        - Implementation Steps (3-5 concrete next steps for clinical teams)
        """,
        
        "Optimization Opportunities": """
        For the Optimization Opportunities analysis of MedMind:
        1. Focus specifically on areas where clinical decision support can be improved
        2. Identify inefficiencies in treatment plans, medication recommendations, and patient monitoring
        3. Analyze correlations between medication adherence, treatment outcomes, and patient satisfaction
        4. Prioritize optimization opportunities based on potential impact on medical error reduction and patient outcomes
        5. Suggest specific technical or process improvements for integration with existing EHR systems
        
        Structure your response with these healthcare-focused sections:
        - Clinical Optimization Priorities (3-5 areas with highest patient care improvement potential)
        - Patient Impact Analysis (quantified benefits of addressing each opportunity in terms of patient outcomes)
        - Clinical Implementation Strategy (specific steps for clinical staff to implement each optimization)
        - EHR Integration Recommendations (specific technical changes needed for seamless workflow)
        - Clinical Risk Assessment (potential challenges for medical staff and how to mitigate them)
        """,
        
        "Financial Impact": """
        For the Financial Impact analysis of MedMind:
        1. Focus on cost-benefit analysis and ROI in healthcare terms (cost of care vs. outcome improvement)
        2. Quantify financial impacts through total cost savings, medication costs, and length of stay reductions
        3. Identify cost savings opportunities in readmission prevention and medical error reduction
        4. Analyze resource allocation efficiency across different treatment plans
        5. Project future financial outcomes based on improved patient outcomes and reduced medical errors
        
        Structure your response with these healthcare-focused sections:
        - Healthcare Cost Analysis (breakdown of cost of care, medication costs, and potential savings)
        - Clinical Revenue Impact (how improved outcomes affect healthcare revenue)
        - Healthcare ROI Calculation (specific calculations showing return on investment in terms of patient outcomes and cost savings)
        - Hospital Cost Reduction Opportunities (specific areas to reduce length of stay and readmissions)
        - Value-Based Care Forecasting (projections based on improved clinical metrics)
        """,
        
        "Strategic Recommendations": """
        For the Strategic Recommendations analysis of MedMind:
        1. Focus on long-term strategic implications for clinical decision support improvement
        2. Identify competitive advantages against traditional clinical decision support systems
        3. Suggest new directions for AI integration with genetic data, vital signs monitoring, and clinical trials
        4. Connect recommendations to broader healthcare goals of reducing errors and improving outcomes
        5. Provide a clinical implementation roadmap with prioritized initiatives
        
        Structure your response with these healthcare-focused sections:
        - Clinical Context (how MedMind fits into broader healthcare quality improvement initiatives)
        - Healthcare Competitive Advantage Analysis (how to maximize clinical effectiveness compared to traditional systems)
        - Clinical Strategic Priorities (3-5 high-impact strategic initiatives for improving patient care)
        - Future Medical Technology Vision (how to evolve MedMind with wearable devices, telemedicine, and personalized medicine over 1-3 years)
        - Clinical Implementation Roadmap (sequenced steps for clinical integration and adoption)
        """
    }

    # Get the specific instructions for the selected focus area
    selected_focus_instructions = focus_area_instructions.get(focus_area, "")

    prompt = f'''
    You are an expert data analyst specializing in {focus_area.lower()} analysis.

    SOLUTION CONTEXT:
    {solution_name}

    {solution_content}

    DATA SUMMARY:
    {data_summary}

    {correlation_info}

    ANALYSIS INSTRUCTIONS:
    {selected_focus_instructions}

    IMPORTANT GUIDELINES:
    - Base all insights directly on the data provided
    - Use specific metrics and numbers from the data in your analysis
    - Maintain a professional, analytical tone
    - Be concise but thorough in your analysis
    - Focus specifically on {focus_area} as defined in the instructions
    - Ensure your response is unique and tailored to this specific focus area
    - Include a mix of observations, analysis, and actionable recommendations
    - Use bullet points and clear section headers for readability
    '''

    return call_cortex_model(prompt, model_name)

data = load_data()
if data.empty:
    st.error("No data found.")
    st.stop()

categorical_cols = [col for col in ["patient_id", "medical_history", "current_medications", "lab_results", "vital_signs", "diagnosis", "treatment_plan", "clinical_trial_id", "trial_name", "trial_status", "medical_publication_id", "publication_title", "medication_side_effects", "allergies", "medical_conditions", "family_medical_history", "genetic_data", "treatment_outcome", "medication_adherence", "patient_satisfaction", "medication_recommendation", "treatment_recommendation"] if col in data.columns]
numeric_cols = [col for col in ["readmission_risk", "medical_error_rate", "patient_outcome_score", "cost_of_care", "length_of_stay", "medication_cost", "total_cost_savings"] if col in data.columns]
date_cols = [col for col in ["publication_date"] if col in data.columns]

sample_cols = data.columns.tolist()
numeric_candidates = [col for col in sample_cols if data[col].dtype in ['float64', 'int64'] and 'id' not in col.lower()]
date_candidates = [col for col in sample_cols if 'date' in col.lower() or 'timestamp' in col.lower()]
cat_candidates = [col for col in sample_cols if data[col].dtype == 'object' and data[col].nunique() < 1000]

# Four tabs - with Metrics as the first tab (Tab 0)
tabs = st.tabs(["📊 Metrics", "✨ AI Insights", "📁 Insights History", "🔍 Data Explorer"])

# Metrics Tab (Tab 0)
with tabs[0]:
    st.header("Clinical Decision Support Metrics")
    
    # Overview metrics row - 4 KPIs
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics from the data
    avg_outcome_score = data['patient_outcome_score'].mean() if 'patient_outcome_score' in data.columns else 0
    avg_error_rate = data['medical_error_rate'].mean() if 'medical_error_rate' in data.columns else 0
    avg_readmission_risk = data['readmission_risk'].mean() if 'readmission_risk' in data.columns else 0
    total_cost_savings = data['total_cost_savings'].sum() if 'total_cost_savings' in data.columns else 0
    
    with col1:
        with st.container(border=True):
            st.metric(
                "Avg Patient Outcome Score", 
                f"{avg_outcome_score:.2f}",
                f"{(avg_outcome_score - 0.5) / 0.5 * 100:.1f}%" if avg_outcome_score > 0.5 else f"{(avg_outcome_score - 0.5) / 0.5 * 100:.1f}%",
                help="Average patient outcome score (0-1 scale). Higher is better."
            )
    
    with col2:
        with st.container(border=True):
            st.metric(
                "Avg Medical Error Rate", 
                f"{avg_error_rate:.2f}",
                f"{(0.5 - avg_error_rate) / 0.5 * 100:.1f}%" if avg_error_rate < 0.5 else f"{(0.5 - avg_error_rate) / 0.5 * 100:.1f}%",
                help="Average error rate (0-1 scale). Lower is better."
            )
    
    with col3:
        with st.container(border=True):
            st.metric(
                "Avg Readmission Risk", 
                f"{avg_readmission_risk:.2f}",
                f"{(0.5 - avg_readmission_risk) / 0.5 * 100:.1f}%" if avg_readmission_risk < 0.5 else f"{(0.5 - avg_readmission_risk) / 0.5 * 100:.1f}%",
                help="Average readmission risk (0-1 scale). Lower is better."
            )
    
    with col4:
        with st.container(border=True):
            st.metric(
                "Total Cost Savings", 
                f"${total_cost_savings:,.2f}",
                help="Total cost savings across all patients"
            )
    
    # Financial Metrics Section - 3 Financial Metrics
    st.subheader("Financial Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            avg_cost_of_care = data['cost_of_care'].mean() if 'cost_of_care' in data.columns else 0
            st.metric("Avg Cost of Care", f"${avg_cost_of_care:,.2f}")
        
    with col2:
        with st.container(border=True):
            avg_medication_cost = data['medication_cost'].mean() if 'medication_cost' in data.columns else 0
            st.metric("Avg Medication Cost", f"${avg_medication_cost:,.2f}")
        
    with col3:
        with st.container(border=True):
            avg_los = data['length_of_stay'].mean() if 'length_of_stay' in data.columns else 0
            st.metric("Avg Length of Stay", f"{avg_los:.1f} days")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    # Patient Outcome Distribution
    with col1:
        st.subheader("Patient Outcome Distribution")
        
        if 'patient_outcome_score' in data.columns:
            # Create bins for outcome scores
            bins = [0, 0.25, 0.5, 0.75, 1.0]
            labels = ['Poor (0-0.25)', 'Fair (0.25-0.5)', 'Good (0.5-0.75)', 'Excellent (0.75-1.0)']
            data['outcome_category'] = pd.cut(data['patient_outcome_score'], bins=bins, labels=labels, include_lowest=True)
            
            outcome_counts = data['outcome_category'].value_counts().reset_index()
            outcome_counts.columns = ['category', 'count']
            
            # Patient Outcome Distribution Chart
            chart = alt.Chart(outcome_counts).mark_bar().encode(
                x=alt.X('category:N', title='Outcome Category', sort=None, axis=alt.Axis(labelAngle=0)),
                y=alt.Y('count:Q', title='Number of Patients'),
                color=alt.Color('category:N', scale=alt.Scale(domain=labels, range=['#E74C3C', '#F4D03F', '#52BE80', '#5DADE2']))
            )
            
            text = chart.mark_text(
                align='center',
                baseline='bottom',
                dy=-15  # Increased space above bars
            ).encode(
                text='count:Q'
            )
            
            # Use the same approach for both charts
            st.altair_chart((chart + text).properties(height=300, width=500), use_container_width=True)
        else:
            st.write("Patient outcome score data not available")
    
    # Treatment Outcome Distribution
    with col2:
        st.subheader("Treatment Outcome Distribution")
        
        if 'treatment_outcome' in data.columns:
            treatment_counts = data['treatment_outcome'].value_counts().reset_index()
            treatment_counts.columns = ['outcome', 'count']
            
            colors = {
                'Successful': '#52BE80',
                'Partial Success': '#F4D03F',
                'Ongoing': '#5DADE2', 
                'Unsuccessful': '#E74C3C'
            }
            
            chart = alt.Chart(treatment_counts).mark_bar().encode(
                x=alt.X('outcome:N', title='Treatment Outcome', sort='-y', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('count:Q', title='Number of Patients'),
                color=alt.Color('outcome:N', scale=alt.Scale(domain=list(colors.keys()), range=list(colors.values())))
            )
            
            text = chart.mark_text(
                align='center',
                baseline='bottom',
                dy=-15  # Increased space above bars
            ).encode(
                text='count:Q'
            )
            
            st.altair_chart((chart + text).properties(height=300, width=500), use_container_width=True)
        else:
            st.write("Treatment outcome data not available")
    
    # Patient Satisfaction
    st.subheader("Patient Satisfaction")
    
    if 'patient_satisfaction' in data.columns:
        satisfaction_counts = data['patient_satisfaction'].value_counts().reset_index()
        satisfaction_counts.columns = ['satisfaction', 'count']
        
        colors = {
            'Satisfied': '#52BE80',
            'Neutral': '#F4D03F',
            'Unsatisfied': '#E74C3C'
        }
        
        # Patient Satisfaction Chart
        chart = alt.Chart(satisfaction_counts).mark_bar().encode(
            x=alt.X('satisfaction:N', title='Satisfaction Level', sort='-y', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('count:Q', title='Number of Patients'),
            color=alt.Color('satisfaction:N', scale=alt.Scale(domain=list(colors.keys()), range=list(colors.values())))
        )
        
        text = chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-15  # Increased space above bars
        ).encode(
            text='count:Q'
        )
        
        # Use the same approach for Patient Satisfaction chart
        st.altair_chart((chart + text).properties(height=300, width=500), use_container_width=True)
    else:
        st.write("Patient satisfaction data not available")
    
    # Clinical Metrics Section
    st.subheader("Clinical Metrics")
    
    # Create 2 columns for diagnosis/treatment metrics
    col1, col2 = st.columns(2)
    
    # Top Diagnoses
    with col1:
        st.subheader("Top Diagnoses")
        
        if 'diagnosis' in data.columns:
            diagnosis_counts = data['diagnosis'].value_counts().head(5).reset_index()
            diagnosis_counts.columns = ['diagnosis', 'count']
            
            # Top Diagnoses Chart
            chart = alt.Chart(diagnosis_counts).mark_bar().encode(
                y=alt.Y('diagnosis:N', title='Diagnosis', sort='-x'),
                x=alt.X('count:Q', title='Number of Patients'),
                color=alt.Color('diagnosis:N', legend=None)
            )
            
            text = chart.mark_text(
                align='left',
                baseline='middle',
                dx=3
            ).encode(
                text='count:Q'
            )
            
            st.altair_chart((chart + text).properties(height=300), use_container_width=True)
        else:
            st.write("Diagnosis data not available")
    
    # Treatment Plan Distribution
    with col2:
        st.subheader("Treatment Plan Distribution")
        
        if 'treatment_plan' in data.columns:
            treatment_counts = data['treatment_plan'].value_counts().reset_index()
            treatment_counts.columns = ['plan', 'count']
            
            # Treatment Plan Distribution Chart
            chart = alt.Chart(treatment_counts).mark_bar().encode(
                y=alt.Y('plan:N', title='Treatment Plan', sort='-x'),
                x=alt.X('count:Q', title='Number of Patients'),
                color=alt.Color('plan:N', legend=None)
            )
            
            text = chart.mark_text(
                align='left',
                baseline='middle',
                dx=3
            ).encode(
                text='count:Q'
            )
            
            st.altair_chart((chart + text).properties(height=300), use_container_width=True)
        else:
            st.write("Treatment plan data not available")
    
# AI Insights tab
with tabs[1]:
    st.subheader("✨ AI-Powered Insights")
    focus_area = st.radio("Focus Area", [
        "Overall Performance", 
        "Optimization Opportunities", 
        "Financial Impact", 
        "Strategic Recommendations"
    ])
    selected_model = st.selectbox("Cortex Model", MODELS, index=0)

    if st.button("Generate Insights"):
        with st.spinner("Generating with Snowflake Cortex..."):
            insights = generate_insights(data, focus_area, selected_model)
            if insights:
                st.markdown(insights)
                timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.insights_history.append({
                    "timestamp": timestamp,
                    "focus": focus_area,
                    "insights": insights,
                    "model": selected_model
                })
                st.download_button("Download Insights", insights, file_name=f"{solution_name.replace(' ', '_').lower()}_insights.md")
            else:
                st.error("No insights returned.")

# Insights History tab
with tabs[2]:
    st.subheader("📁 Insights History")
    if st.session_state.insights_history:
        for i, item in enumerate(reversed(st.session_state.insights_history)):
            with st.expander(f"{item['timestamp']} - {item['focus']} ({item['model']})", expanded=False):
                st.markdown(item["insights"])
    else:
        st.info("No insights generated yet. Go to the AI Insights tab to generate some insights.")

# Data Explorer tab
with tabs[3]:
    st.subheader("🔍 Data Explorer")
    rows_per_page = st.slider("Rows per page", 5, 50, 10)
    page = st.number_input("Page", min_value=1, value=1)
    start = (page - 1) * rows_per_page
    end = min(start + rows_per_page, len(data))
    st.dataframe(data.iloc[start:end], use_container_width=True)
    st.caption(f"Showing rows {start + 1}–{end} of {len(data)}")
```

</details>

### 3.2 Create and Deploy the Streamlit in Snowflake Gen AI Data App
1. Switch to **Chrome Tab 4 (Snowflake UI)**
2. Click on **Projects** in the left navigation panel
3. Click on **Streamlit**
4. Click the **+ Streamlit App** blue button in the upper right corner
5. Configure your app:
   - App title: `MedMind_CDS`
   - Database: Select `SF_LABUSER#_DB` (only option available for your user)
   - Schema: Select `healthcare_cds_connector` the schema created by your Fivetran connector (this should be the only schema available other than Public - do not select Public)
6. In the Streamlit Editor that appears (left side of the Streamlit UI), select all text (Command+A) and delete it
7. Paste the copied Streamlit application code into the empty editor (Command+V):
8. Click the blue **Run** button in the upper right corner
9. Close the editor by clicking the middle icon in the bottom left navigation

### 3.3 Explore the Streamlit in Snowflake Gen AI Data App
The MedMind data app should now be running with the following sections:
- **Metrics**: View patient outcomes, medical error rates, and financial metrics
- **AI Insights**: Generate AI-powered analysis of the clinical data across four focus areas
- **Insights History**: Access previously generated AI insights
- **Data Explorer**: Browse the underlying data

## Done!
You've successfully:
1. Created a custom Fivetran connector using the Fivetran Connector SDK
2. Deployed the connector to sync healthcare data into Snowflake
3. Built a Streamlit in Snowflake data app to visualize and analyze the data using Snowflake Cortex

## Next Steps
Consider how you might adapt this solution for your own use:
- Integration with EHR systems like Epic, Cerner, or Meditech
- Adding real-time vital signs monitoring from patient devices
- Implementing machine learning models for more sophisticated predictions
- Customizing the Streamlit app for specific clinical specialties

## Resources
- Fivetran Connector SDK Documentation: [https://fivetran.com/docs/connectors/connector-sdk](https://fivetran.com/docs/connectors/connector-sdk)  
- Fivetran Connector SDK Examples: [https://fivetran.com/docs/connector-sdk/examples](https://fivetran.com/docs/connector-sdk/examples)
- API Connector Reference: [https://sdk-demo-api-dot-internal-sales.uc.r.appspot.com/icp_api_spec](https://sdk-demo-api-dot-internal-sales.uc.r.appspot.com/icp_api_spec)
- Snowflake Cortex Documentation: [https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions)
- Snowflake Streamlit Documentation: [https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)