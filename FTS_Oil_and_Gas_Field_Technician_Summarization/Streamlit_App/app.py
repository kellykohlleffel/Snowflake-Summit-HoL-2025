import streamlit as st
import pandas as pd
import altair as alt
import time
import json
import re
from datetime import datetime
from snowflake.snowpark.context import get_active_session

st.set_page_config(
    page_title="loglynx_–_ai_driven_field_technician_task_summarization",
    page_icon="https://i.imgur.com/Og6gFnB.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

solution_name = '''Solution 1: LogLynx – AI-driven Field Technician Task Summarization'''
solution_name_clean = '''loglynx_–_ai_driven_field_technician_task_summarization'''
table_name = '''FTS_RECORDS'''
table_description = '''Consolidated data from field technician logs, CMMS, and ERP systems for LogLynx solution'''
solution_content = '''Solution 1: LogLynx – AI-driven Field Technician Task Summarization**

### Business Challenge
The primary business challenge addressed by LogLynx is the manual and time-consuming process of summarizing daily logs from field technicians in the Oil and Gas industry. This process hinders the ability to quickly identify trends, patterns, and potential issues, leading to delayed maintenance, increased costs, and reduced operational efficiency.

### Key Features
- Automated summarization of daily logs from field technicians
- Real-time data analysis and insights
- Customizable dashboards for easy monitoring and decision-making
- Integration with existing CMMS (Computerized Maintenance Management System) and ERP (Enterprise Resource Planning) systems

### Data Sources
- Field Technician Logs: SAP, Oracle, Microsoft Dynamics
- CMMS: IBM Maximo, Infor EAM, SAP EAM
- ERP: SAP, Oracle, Microsoft Dynamics

### Competitive Advantage
LogLynx differentiates itself by leveraging generative AI to automate the summarization process, reducing manual labor and increasing the speed of insights. This allows for faster decision-making and improved operational efficiency.

### Key Stakeholders
- Field Technicians
- Maintenance Managers
- Operations Managers
- C-level Executive: Chief Operating Officer (COO)

### Technical Approach
LogLynx utilizes a combination of natural language processing (NLP) and machine learning algorithms to analyze and summarize field technician logs. This approach enables the system to identify key information, trends, and patterns, providing actionable insights for maintenance and operations teams.

### Expected Business Results
- **300 fewer failed treatments per year**
  **10,000 field technician logs × 3% baseline failure rate × 15% reduction = 300 fewer failed treatments/year**
- **$ 1,200,000 in maintenance cost savings annually**
  **$ 4,000,000 annual maintenance costs × 30% reduction = $ 1,200,000 savings/year**
- **25% reduction in maintenance downtime**
  **100 hours of downtime/month × 12 months/year × 25% reduction = 300 hours saved/year**
- **90% reduction in manual summarization time**
  **100 hours/month × 12 months/year × 90% reduction = 1,200 hours saved/year**

### Success Metrics
- Reduction in failed treatments
- Maintenance cost savings
- Maintenance downtime reduction
- Time saved in manual summarization

### Risk Assessment
Potential challenges include:
- Data quality and consistency
- Integration with existing systems
- Training and adoption by field technicians

Mitigation strategies:
- Implement data quality checks and data cleansing processes
- Conduct thorough system integration testing
- Provide comprehensive training and support for field technicians

### Long-term Evolution
Over the next 3-5 years, LogLynx will continue to evolve by incorporating more advanced NLP techniques, integrating with emerging technologies like IoT sensors, and expanding its capabilities to include predictive maintenance and real-time monitoring.'''

# Display logo and title inline
st.markdown(f'''
<div style="display:flex; align-items:center; margin-bottom:15px">
    <img src="https://i.imgur.com/Og6gFnB.png" width="100" style="margin-right:15px">
    <div>
        <h1 style="font-size:2.2rem; margin:0; padding:0">{solution_name_clean.replace('_', ' ').title()}</h1>
        <p style="font-size:1.1rem; color:gray; margin:0; padding:0">Fivetran and Cortex-powered Streamlit in Snowflake data application for Oil & Gas</p>
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

    # Calculate basic statistics for numeric columns only - exclude ID columns
    numeric_stats = {}
    # Only include actual numeric metrics, not ID columns
    key_metrics = ["failure_rate", "maintenance_cost", "downtime_hours", "summarization_time_saved"]
    
    # Filter to only columns that exist and are actually numeric
    available_metrics = []
    for col in key_metrics:
        if col in data.columns:
            try:
                # Test if the column is actually numeric by trying to calculate mean
                test_mean = pd.to_numeric(data[col], errors='coerce').mean()
                if not pd.isna(test_mean):
                    available_metrics.append(col)
            except:
                # Skip columns that can't be converted to numeric
                continue
    
    for col in available_metrics:
        try:
            numeric_data = pd.to_numeric(data[col], errors='coerce')
            numeric_stats[col] = {
                "mean": numeric_data.mean(),
                "min": numeric_data.min(),
                "max": numeric_data.max(),
                "std": numeric_data.std()
            }
            data_summary += f"- {col} (avg: {numeric_data.mean():.2f}, min: {numeric_data.min():.2f}, max: {numeric_data.max():.2f})\n"
        except Exception as e:
            # Skip columns that cause errors
            continue

    # Get top values for categorical columns
    categorical_stats = {}
    categorical_options = ["log_description", "maintenance_type", "maintenance_status", "summarized_log"]
    for cat_col in categorical_options:
        if cat_col in data.columns:
            try:
                top = data[cat_col].value_counts().head(3)
                categorical_stats[cat_col] = top.to_dict()
                data_summary += f"\nTop {cat_col} values:\n" + "\n".join(f"- {k}: {v}" for k, v in top.items())
            except:
                # Skip columns that cause errors
                continue

    # Calculate correlations if enough numeric columns available
    correlation_info = ""
    if len(available_metrics) >= 2:
        try:
            # Create a dataframe with only the numeric columns
            numeric_df = data[available_metrics].apply(pd.to_numeric, errors='coerce')
            correlations = numeric_df.corr()
            
            # Get the top 3 strongest correlations (absolute value)
            corr_pairs = []
            for i in range(len(correlations.columns)):
                for j in range(i+1, len(correlations.columns)):
                    col1 = correlations.columns[i]
                    col2 = correlations.columns[j]
                    corr_value = correlations.iloc[i, j]
                    if not pd.isna(corr_value):
                        corr_pairs.append((col1, col2, abs(corr_value), corr_value))

            # Sort by absolute correlation value
            corr_pairs.sort(key=lambda x: x[2], reverse=True)

            # Add top correlations to the summary
            if corr_pairs:
                correlation_info = "Top correlations between metrics:\n"
                for col1, col2, _, corr_value in corr_pairs[:3]:
                    correlation_info += f"- {col1} and {col2}: r = {corr_value:.2f}\n"
        except Exception as e:
            correlation_info = "Could not calculate correlations between metrics.\n"

    # Define specific instructions for each focus area
    focus_area_instructions = {
        "Overall Performance": """
        For the Overall Performance analysis of LogLynx:
        1. Provide a comprehensive analysis of the field technician log summarization system using failure rate, maintenance cost, downtime hours, and time saved metrics
        2. Identify significant patterns in maintenance types, equipment performance, and technician efficiency across oil and gas operations
        3. Highlight 3-5 key operational metrics that best indicate log summarization effectiveness (failure rate reduction, cost savings, downtime reduction)
        4. Discuss both strengths and areas for improvement in the AI-powered log analysis process
        5. Include 3-5 actionable insights for improving field operations based on the technician log data
        
        Structure your response with these oil & gas focused sections:
        - Field Operations Insights (5 specific insights with supporting technician and equipment data)
        - Maintenance Performance Trends (3-4 significant trends in failure rates and downtime reduction)
        - Operational Efficiency Recommendations (3-5 data-backed recommendations for improving field operations)
        - Implementation Steps (3-5 concrete next steps for field technicians and maintenance managers)
        """,
        
        "Optimization Opportunities": """
        For the Optimization Opportunities analysis of LogLynx:
        1. Focus specifically on areas where field technician log analysis and maintenance efficiency can be improved
        2. Identify inefficiencies in maintenance scheduling, equipment downtime, and technician productivity across oil and gas operations
        3. Analyze correlations between maintenance types, failure rates, and summarization time savings
        4. Prioritize optimization opportunities based on potential impact on operational costs and equipment reliability
        5. Suggest specific technical or process improvements for integration with existing CMMS and ERP systems
        
        Structure your response with these oil & gas focused sections:
        - Field Operations Optimization Priorities (3-5 areas with highest cost and downtime reduction potential)
        - Operational Impact Analysis (quantified benefits of addressing each opportunity in terms of maintenance metrics)
        - CMMS Integration Strategy (specific steps for maintenance teams to implement each optimization)
        - System Integration Recommendations (specific technical changes needed for seamless integration with SAP, Oracle, and IBM Maximo)
        - Field Operations Risk Assessment (potential challenges for technicians and maintenance teams and how to mitigate them)
        """,
        
        "Financial Impact": """
        For the Financial Impact analysis of LogLynx:
        1. Focus on cost-benefit analysis and ROI in oil and gas operations terms (maintenance cost vs. operational efficiency gains)
        2. Quantify financial impacts through maintenance cost savings, downtime reduction, and productivity improvements
        3. Identify cost savings opportunities across different maintenance types and equipment categories
        4. Analyze resource allocation efficiency across different technicians and operational areas
        5. Project future financial outcomes based on improved log summarization accuracy and expanding to predictive maintenance
        
        Structure your response with these oil & gas focused sections:
        - Maintenance Cost Analysis (breakdown of maintenance costs and potential savings by equipment and maintenance type)
        - Operational Efficiency Impact (how improved log summarization affects operational costs and throughput)
        - Oil & Gas ROI Calculation (specific calculations showing return on investment in terms of maintenance cost reduction)
        - Downtime Reduction Opportunities (specific areas to reduce equipment downtime and associated costs)
        - Operations Cost Forecasting (projections based on improved maintenance efficiency metrics)
        """,
        
        "Strategic Recommendations": """
        For the Strategic Recommendations analysis of LogLynx:
        1. Focus on long-term strategic implications for digital transformation in oil and gas operations
        2. Identify competitive advantages against traditional manual log summarization approaches
        3. Suggest new directions for AI integration with emerging oil and gas technologies (e.g., IoT sensors, predictive maintenance)
        4. Connect recommendations to broader operational goals of reducing costs and improving equipment reliability
        5. Provide a digital operations roadmap with prioritized initiatives
        
        Structure your response with these oil & gas focused sections:
        - Digital Operations Context (how LogLynx fits into broader digital transformation in oil and gas)
        - Operational Competitive Advantage Analysis (how to maximize efficiency advantages compared to traditional manual processes)
        - Field Technology Strategic Priorities (3-5 high-impact strategic initiatives for improving field operations)
        - Advanced Technology Integration Vision (how to evolve LogLynx with IoT sensors and predictive maintenance over 1-3 years)
        - Operations Transformation Roadmap (sequenced steps for expanding to real-time monitoring and predictive maintenance)
        """
    }

    # Get the specific instructions for the selected focus area
    selected_focus_instructions = focus_area_instructions.get(focus_area, "")

    prompt = f'''
    You are an expert data analyst specializing in {focus_area.lower()} analysis for oil and gas operations.

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
    - Frame all insights in the context of oil and gas field operations and maintenance
    '''

    return call_cortex_model(prompt, model_name)

def create_metrics_charts(data):
    """Create metric visualizations for the oil and gas data"""
    charts = []
    
    # Maintenance Cost Distribution
    if 'maintenance_cost' in data.columns:
        cost_chart = alt.Chart(data).mark_bar().encode(
            alt.X('maintenance_cost:Q', bin=alt.Bin(maxbins=20), title='Maintenance Cost ($)'),
            alt.Y('count()', title='Number of Records'),
            color=alt.value('#1f77b4')
        ).properties(
            title='Cost Distribution',
            width=380,
            height=280
        )
        charts.append(('Cost Distribution', cost_chart))
    
    # Failure Rate by Maintenance Type
    if 'failure_rate' in data.columns and 'maintenance_type' in data.columns:
        failure_chart = alt.Chart(data).mark_boxplot().encode(
            alt.X('maintenance_type:N', title='Maintenance Type'),
            alt.Y('failure_rate:Q', title='Failure Rate'),
            color=alt.Color('maintenance_type:N', legend=None)
        ).properties(
            title='Failure Rate by Type',
            width=380,
            height=280
        )
        charts.append(('Failure Rate by Type', failure_chart))
    
    # Downtime Hours Trend
    if 'downtime_hours' in data.columns and 'log_date' in data.columns:
        downtime_chart = alt.Chart(data).mark_line(point=True).encode(
            alt.X('log_date:T', title='Date'),
            alt.Y('mean(downtime_hours):Q', title='Average Downtime Hours'),
            color=alt.value('#ff7f0e')
        ).properties(
            title='Downtime Trends',
            width=380,
            height=280
        )
        charts.append(('Downtime Trends', downtime_chart))
    
    # Maintenance Status Distribution
    if 'maintenance_status' in data.columns:
        status_chart = alt.Chart(data).mark_arc().encode(
            theta=alt.Theta('count():Q'),
            color=alt.Color('maintenance_status:N', title='Status'),
            tooltip=['maintenance_status:N', 'count():Q']
        ).properties(
            title='Status Distribution',
            width=380,
            height=280
        )
        charts.append(('Status Distribution', status_chart))
    
    # Time Saved vs Maintenance Cost Correlation
    if 'summarization_time_saved' in data.columns and 'maintenance_cost' in data.columns:
        correlation_chart = alt.Chart(data).mark_circle(size=80).encode(
            alt.X('summarization_time_saved:Q', title='Time Saved (hours)'),
            alt.Y('maintenance_cost:Q', title='Maintenance Cost ($)'),
            color=alt.Color('failure_rate:Q', title='Failure Rate', scale=alt.Scale(scheme='viridis')),
            tooltip=['summarization_time_saved:Q', 'maintenance_cost:Q', 'failure_rate:Q']
        ).properties(
            title='Time Saved vs Cost',
            width=380,
            height=280
        )
        charts.append(('Time Saved vs Cost', correlation_chart))
    
    # Equipment Performance Bar Chart
    if 'equipment_id' in data.columns and 'failure_rate' in data.columns:
        # Group by equipment and calculate average failure rate
        equipment_data = data.groupby('equipment_id')['failure_rate'].mean().reset_index()
        equipment_data = equipment_data.head(12).sort_values('failure_rate', ascending=False)  # Top 12 highest failure rates
        
        equipment_chart = alt.Chart(equipment_data).mark_bar().encode(
            alt.X('equipment_id:O', title='Equipment ID', sort='-y'),
            alt.Y('failure_rate:Q', title='Average Failure Rate'),
            color=alt.Color('failure_rate:Q', title='Failure Rate', scale=alt.Scale(scheme='reds')),
            tooltip=['equipment_id:O', alt.Tooltip('failure_rate:Q', format='.3f')]
        ).properties(
            title='Equipment Performance',
            width=380,
            height=280
        )
        charts.append(('Equipment Performance', equipment_chart))
    
    return charts

data = load_data()
if data.empty:
    st.error("No data found.")
    st.stop()

categorical_cols = [col for col in ["log_description", "maintenance_type", "maintenance_status", "summarized_log"] if col in data.columns]
numeric_cols = [col for col in ["technician_id", "equipment_id", "erp_order_id", "customer_id", "failure_rate", "maintenance_cost", "downtime_hours", "summarization_time_saved"] if col in data.columns]
date_cols = [col for col in ["log_date", "created_at", "updated_at"] if col in data.columns]

sample_cols = data.columns.tolist()
numeric_candidates = [col for col in sample_cols if data[col].dtype in ['float64', 'int64'] and 'id' not in col.lower()]
date_candidates = [col for col in sample_cols if 'date' in col.lower() or 'timestamp' in col.lower()]
cat_candidates = [col for col in sample_cols if data[col].dtype == 'object' and data[col].nunique() < 1000]

# Four tabs - Metrics tab first, then AI Insights
tabs = st.tabs(["📊 Metrics", "✨ AI Insights", "📁 Insights History", "🔍 Data Explorer"])

# Metrics tab (now first)
with tabs[0]:
    st.subheader("📊 Key Performance Metrics")
    
    # Display key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'failure_rate' in data.columns:
            avg_failure_rate = data['failure_rate'].mean()
            st.metric("Avg Failure Rate", f"{avg_failure_rate:.3f}", delta=f"{(avg_failure_rate - 0.03)*100:.1f}% vs baseline")
    
    with col2:
        if 'maintenance_cost' in data.columns:
            avg_cost = data['maintenance_cost'].mean()
            st.metric("Avg Maintenance Cost", f"${avg_cost:,.0f}", delta=f"-${(4000000/12 - avg_cost):,.0f} vs target")
    
    with col3:
        if 'downtime_hours' in data.columns:
            avg_downtime = data['downtime_hours'].mean()
            st.metric("Avg Downtime Hours", f"{avg_downtime:.1f}h", delta=f"{(avg_downtime - 8.33):.1f}h vs target")
    
    with col4:
        if 'summarization_time_saved' in data.columns:
            avg_time_saved = data['summarization_time_saved'].mean()
            st.metric("Avg Time Saved", f"{avg_time_saved:.1f}h", delta=f"{(avg_time_saved - 2.5):.1f}h vs baseline")
    
    st.markdown("---")
    
    # Create and display charts
    charts = create_metrics_charts(data)
    
    if charts:
        st.subheader("📈 Performance Visualizations")
        
        # Display charts in a 2-column grid, ensuring all 6 charts are shown
        num_charts = len(charts)
        for i in range(0, num_charts, 2):
            cols = st.columns(2)
            
            # Left column chart
            if i < num_charts:
                chart_title, chart = charts[i]
                with cols[0]:
                    st.altair_chart(chart, use_container_width=True)
            
            # Right column chart
            if i + 1 < num_charts:
                chart_title, chart = charts[i + 1]
                with cols[1]:
                    st.altair_chart(chart, use_container_width=True)
        
        # Display chart count for debugging
        st.caption(f"Displaying {num_charts} performance charts")
    else:
        st.info("No suitable data found for creating visualizations.")
    
    # Enhanced Summary statistics table
    st.subheader("📈 Summary Statistics")
    if numeric_candidates:
        # Create enhanced summary statistics
        summary_stats = data[numeric_candidates].describe()
        
        # Transpose for better readability and add formatting
        summary_df = summary_stats.T.round(3)
        
        # Add meaningful column names and formatting
        summary_df.columns = ['Count', 'Mean', 'Std Dev', 'Min', '25%', '50% (Median)', '75%', 'Max']
        
        # Format specific columns for better readability
        format_dict = {}
        for col in summary_df.index:
            if 'cost' in col.lower():
                format_dict[col] = "${:,.2f}"
            elif 'rate' in col.lower():
                format_dict[col] = "{:.3f}"
            elif 'hours' in col.lower() or 'time' in col.lower():
                format_dict[col] = "{:.1f}h"
            else:
                format_dict[col] = "{:.2f}"
        
        # Create three columns for better organization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Key Performance Metrics**")
            key_metrics = ['failure_rate', 'maintenance_cost', 'downtime_hours', 'summarization_time_saved']
            key_metrics_present = [m for m in key_metrics if m in summary_df.index]
            
            if key_metrics_present:
                key_stats_df = summary_df.loc[key_metrics_present]
                
                # Create a more readable format
                for metric in key_stats_df.index:
                    mean_val = key_stats_df.loc[metric, 'Mean']
                    min_val = key_stats_df.loc[metric, 'Min']
                    max_val = key_stats_df.loc[metric, 'Max']
                    
                    # Format based on metric type
                    if 'cost' in metric.lower():
                        st.metric(
                            label=metric.replace('_', ' ').title(),
                            value=f"${mean_val:,.0f}",
                            help=f"Range: ${min_val:,.0f} - ${max_val:,.0f}"
                        )
                    elif 'rate' in metric.lower():
                        st.metric(
                            label=metric.replace('_', ' ').title(),
                            value=f"{mean_val:.3f}",
                            help=f"Range: {min_val:.3f} - {max_val:.3f}"
                        )
                    elif 'hours' in metric.lower() or 'time' in metric.lower():
                        st.metric(
                            label=metric.replace('_', ' ').title(),
                            value=f"{mean_val:.1f}h",
                            help=f"Range: {min_val:.1f}h - {max_val:.1f}h"
                        )
                    else:
                        st.metric(
                            label=metric.replace('_', ' ').title(),
                            value=f"{mean_val:.2f}",
                            help=f"Range: {min_val:.2f} - {max_val:.2f}"
                        )
        
        with col2:
            st.markdown("**📊 Distribution Insights**")
            
            # Calculate and display key insights
            insights = []
            
            if 'failure_rate' in summary_df.index:
                fr_mean = summary_df.loc['failure_rate', 'Mean']
                fr_std = summary_df.loc['failure_rate', 'Std Dev']
                insights.append(f"• **Failure Rate Variability**: {fr_std:.3f} (σ)")
                
                if fr_mean > 0.5:
                    insights.append(f"• **High failure rate detected** (>{fr_mean:.1%})")
                else:
                    insights.append(f"• **Acceptable failure rate** ({fr_mean:.1%})")
            
            if 'maintenance_cost' in summary_df.index:
                mc_q75 = summary_df.loc['maintenance_cost', '75%']
                mc_q25 = summary_df.loc['maintenance_cost', '25%']
                iqr = mc_q75 - mc_q25
                insights.append(f"• **Cost IQR**: ${iqr:,.0f}")
            
            if 'downtime_hours' in summary_df.index:
                dt_median = summary_df.loc['downtime_hours', '50% (Median)']
                dt_max = summary_df.loc['downtime_hours', 'Max']
                insights.append(f"• **Median Downtime**: {dt_median:.1f}h")
                if dt_max > 10:
                    insights.append(f"• **⚠️ High downtime events**: up to {dt_max:.1f}h")
            
            if 'summarization_time_saved' in summary_df.index:
                ts_mean = summary_df.loc['summarization_time_saved', 'Mean']
                insights.append(f"• **Avg Time Saved**: {ts_mean:.1f}h per log")
            
            for insight in insights:
                st.markdown(insight)
        
        # Full detailed table (collapsible)
        with st.expander("📋 Detailed Statistics Table", expanded=False):
            st.dataframe(
                summary_df.style.format({
                    'Count': '{:.0f}',
                    'Mean': '{:.3f}',
                    'Std Dev': '{:.3f}',
                    'Min': '{:.3f}',
                    '25%': '{:.3f}',
                    '50% (Median)': '{:.3f}',
                    '75%': '{:.3f}',
                    'Max': '{:.3f}'
                }),
                use_container_width=True
            )

# AI Insights tab (now second)
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
                    "model": selected_model,
                    "insights": insights
                })
                st.download_button("Download Insights", insights, file_name=f"{solution_name.replace(' ', '_').lower()}_insights.md")
            else:
                st.error("No insights returned.")

# Insights History tab (now third)
with tabs[2]:
    st.subheader("📁 Insights History")
    if st.session_state.insights_history:
        for i, item in enumerate(reversed(st.session_state.insights_history)):
            with st.expander(f"{item['timestamp']} - {item['focus']} ({item['model']})", expanded=False):
                st.markdown(item["insights"])
    else:
        st.info("No insights generated yet. Go to the AI Insights tab to generate some insights.")

# Data Explorer tab (now fourth)
with tabs[3]:
    st.subheader("🔍 Data Explorer")
    rows_per_page = st.slider("Rows per page", 5, 50, 10)
    page = st.number_input("Page", min_value=1, value=1)
    start = (page - 1) * rows_per_page
    end = min(start + rows_per_page, len(data))
    st.dataframe(data.iloc[start:end], use_container_width=True)
    st.caption(f"Showing rows {start + 1}–{end} of {len(data)}")