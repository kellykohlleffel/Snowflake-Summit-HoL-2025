# LogLynx – AI-driven Field Technician Task Summarization

![LogLynx](images/LogLynx.png)

A Fivetran and Cortex-powered Streamlit in Snowflake data application for Oil & Gas.

## Overview

LogLynx is an AI-driven field technician task summarization system that helps oil and gas operations automate the manual and time-consuming process of analyzing daily logs from field technicians. This Streamlit in Snowflake data application helps field technicians, maintenance managers, and operations managers reduce failed treatments, decrease maintenance costs, minimize equipment downtime, and save manual summarization time through real-time analysis of field operations data.

The application utilizes a synthetic oil and gas dataset that simulates data from field technician logs, computerized maintenance management systems (CMMS), and enterprise resource planning (ERP) systems. This synthetic data is moved into Snowflake using a custom connector built with the Fivetran Connector SDK, enabling reliable and efficient data pipelines for oil and gas operations analytics.

## Data Sources

The application is designed to work with data from major oil and gas operational systems:

### Oil & Gas Data Sources (Simulated)
- **Field Technician Logs**: 
  - SAP
  - Oracle
  - Microsoft Dynamics
- **Computerized Maintenance Management Systems (CMMS)**: 
  - IBM Maximo
  - Infor EAM
  - SAP EAM
- **Enterprise Resource Planning (ERP) Systems**: 
  - SAP
  - Oracle
  - Microsoft Dynamics

For demonstration and development purposes, we've created a synthetic dataset that approximates these data sources and combined them into a single table exposed through an API server. This approach allows for realistic oil and gas operations analytics without using proprietary field operations data.

## Key Features

- **AI-driven field technician log summarization**: Leverages generative AI to analyze field technician logs and automatically generate summaries with key insights
- **Integration with synthetic oil & gas data**: Simulates data from major field operations systems, CMMS platforms, and ERP systems
- **Comprehensive data application**: Visual representation of key metrics including failure rates, maintenance costs, downtime hours, and time savings
- **AI-powered insights**: Generate in-depth analysis of overall performance, optimization opportunities, financial impact, and strategic recommendations
- **Custom Fivetran connector**: Utilizes a custom connector built with the Fivetran Connector SDK to reliably move data from the API server to Snowflake

## Streamlit Data App Sections

### 📊 Metrics
- **Key Performance Indicators**: Track failure rates, maintenance costs, downtime hours, and time saved
- **Operational Analytics**: Monitor maintenance types, equipment performance, and technician efficiency
- **Cost Distribution**: Visualize the distribution of maintenance costs across operations
- **Failure Rate Analysis**: Analyze failure rates by maintenance type with boxplot visualizations
- **Downtime Trends**: Track downtime hours over time to identify patterns
- **Status Distribution**: Review maintenance status distribution across operations
- **Cost vs Time Correlation**: Map relationships between time saved and maintenance costs
- **Equipment Performance**: Monitor equipment failure rates to identify high-risk assets

### ✨ AI Insights
Generate AI-powered insights with different focus areas:
- **Overall Performance**: Comprehensive analysis of the field technician log summarization system
- **Optimization Opportunities**: Areas where field operations and maintenance efficiency can be improved
- **Financial Impact**: Cost-benefit analysis and ROI in oil and gas operations terms
- **Strategic Recommendations**: Long-term strategic implications for digital transformation

### 📁 Insights History
Access previously generated insights for reference and comparison.

### 🔍 Data Explorer
Explore the underlying data with pagination controls.

## Setup Instructions

1. Within Snowflake, click on **Projects**
2. Click on **Streamlit**
3. Click the blue box in the upper right to create a new Streamlit application
4. On the next page:
   - Name your application
   - **IMPORTANT:** Set the database context
   - **IMPORTANT:** Set the schema context

### Fivetran Data Movement Setup

1. Ensure the API server hosting the synthetic oil and gas data is operational
2. Configure the custom Fivetran connector (built with Fivetran Connector SDK) to connect to the API server - debug and deploy
3. Start the Fivetran sync in the Fivetran UI to move data into a `FTS_RECORDS` table in your Snowflake instance
4. Verify data is being loaded correctly by checking the table in Snowflake

## Data Flow

1. **Synthetic Data Creation**: A synthetic dataset approximating real oil and gas operational data sources has been created and exposed via an API server:
   - Field Technician Logs: SAP, Oracle, Microsoft Dynamics
   - Computerized Maintenance Management Systems: IBM Maximo, Infor EAM, SAP EAM
   - Enterprise Resource Planning Systems: SAP, Oracle, Microsoft Dynamics

2. **Custom Data Integration**: A custom connector built with the Fivetran Connector SDK communicates with the API server to extract the synthetic oil and gas operations data

3. **Automated Data Movement**: Fivetran manages the orchestration and scheduling of data movement from the API server into Snowflake

4. **Data Loading**: The synthetic oil and gas data is loaded into Snowflake as a `FTS_RECORDS` table in a structured format ready for analysis

5. **Data Analysis**: Snowpark for Python and Snowflake Cortex analyze the data to generate insights

6. **Data Visualization**: Streamlit in Snowflake presents the analyzed data in an interactive data application

## Data Requirements

The application expects a table named `FTS_RECORDS` which contains synthetic data simulating various oil and gas operational systems. This data is retrieved from an API server using a custom Fivetran connector built with the Fivetran Connector SDK:

### Field Operations Data
- `record_id`
- `log_date`
- `technician_id`
- `log_description`
- `equipment_id`
- `maintenance_type`
- `maintenance_status`
- `erp_order_id`
- `customer_id`
- `summarized_log`

### Performance Metrics
- `failure_rate`
- `maintenance_cost`
- `downtime_hours`
- `summarization_time_saved`

## Benefits

- **300 fewer failed treatments per year**: 10,000 field technician logs × 3% baseline failure rate × 15% reduction = 300 fewer failed treatments/year
- **$1,200,000 in maintenance cost savings annually**: $4,000,000 annual maintenance costs × 30% reduction = $1,200,000 savings/year
- **25% reduction in maintenance downtime**: 100 hours of downtime/month × 12 months/year × 25% reduction = 300 hours saved/year
- **90% reduction in manual summarization time**: 100 hours/month × 12 months/year × 90% reduction = 1,200 hours saved/year

## Technical Details

This application uses:
- Streamlit in Snowflake for the user interface
- Snowflake Cortex for AI-powered insights generation
- Multiple AI models including Claude 4 Sonnet, Claude 3.5 Sonnet, Llama 3.1/3.3, Mistral, DeepSeek, and more
- Snowpark for Python for data processing
- **Fivetran Connector SDK** for building a custom connector to retrieve synthetic oil and gas operations data from an API server
- **Custom Fivetran connector** for automated, reliable data movement into Snowflake

## Success Metrics

- Reduction in failed treatments
- Maintenance cost savings
- Maintenance downtime reduction
- Time saved in manual summarization

## Key Stakeholders

- Field Technicians
- Maintenance Managers
- Operations Managers
- C-level Executive: Chief Operating Officer (COO)

## Competitive Advantage

LogLynx differentiates itself by leveraging generative AI to automate the summarization process, reducing manual labor and increasing the speed of insights. This allows for faster decision-making and improved operational efficiency in oil and gas field operations.

## Long-term Evolution

Over the next 3-5 years, LogLynx will continue to evolve by incorporating more advanced NLP techniques, integrating with emerging technologies like IoT sensors, and expanding its capabilities to include predictive maintenance and real-time monitoring.