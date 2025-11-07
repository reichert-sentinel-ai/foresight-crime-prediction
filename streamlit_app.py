"""
Streamlit Dashboard for Foresight Crime Prediction

Interactive dashboard with:
- Crime forecasting visualizations
- Hotspot maps
- Patrol route optimization
- Statistics and analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging

from src.models.prophet_forecaster import CrimeForecaster
from src.models.dbscan_hotspots import CrimeHotspotDetector
from src.models.route_optimizer import PatrolRouteOptimizer, Hotspot
from src.data.etl import CrimeDataETL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="Foresight Crime Prediction",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark theme styling
st.markdown("""
<style>
    /* Dark theme customizations */
    .stApp {
        background-color: #0f172a;
        color: #f1f5f9;
    }
    
    /* Sidebar dark theme */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
    }
    
    /* Text colors */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #3b82f6 !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: #f1f5f9;
    }
    
    /* Selectbox */
    .stSelectbox > div > div > select {
        background-color: #1e293b;
        color: #f1f5f9;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #3b82f6;
        color: white;
    }
    
    .stButton > button:hover {
        background-color: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🗺️ Foresight Crime Prediction Platform")
st.markdown("**Predictive crime intelligence with geospatial analytics**")

# Sidebar
st.sidebar.title("Configuration")

# Initialize ETL
@st.cache_data
def load_data():
    """Load and process crime data"""
    etl = CrimeDataETL()
    df = etl.load_chicago_data()
    return df

# Load data
with st.spinner("Loading crime data..."):
    df = load_data()

if df is None or len(df) == 0:
    st.error("No data loaded. Please ensure data files are available.")
    st.stop()

# Sidebar filters
st.sidebar.subheader("Data Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    value=(
        df['incident_date'].min().date() if 'incident_date' in df.columns else datetime(2020, 1, 1).date(),
        df['incident_date'].max().date() if 'incident_date' in df.columns else datetime(2024, 1, 1).date()
    ),
    min_value=df['incident_date'].min().date() if 'incident_date' in df.columns else datetime(2020, 1, 1).date(),
    max_value=df['incident_date'].max().date() if 'incident_date' in df.columns else datetime(2024, 1, 1).date()
)

if isinstance(date_range, tuple) and 'incident_date' in df.columns:
    start_date, end_date = date_range
    df = df[(df['incident_date'] >= pd.Timestamp(start_date)) & 
            (df['incident_date'] <= pd.Timestamp(end_date))]

crime_types = st.sidebar.multiselect(
    "Crime Types",
    options=sorted(df['crime_type'].unique().tolist()) if 'crime_type' in df.columns else [],
    default=[]
)

if crime_types and 'crime_type' in df.columns:
    df = df[df['crime_type'].isin(crime_types)]

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📊 Forecast", "🗺️ Hotspots", "🚗 Routes", "📈 Statistics"])

# Tab 1: Forecasting
with tab1:
    st.header("Crime Forecasting")
    st.markdown("7-day crime predictions using Prophet time-series model")
    
    col1, col2 = st.columns(2)
    
    with col1:
        forecast_periods = st.slider("Forecast Period (days)", 1, 30, 7)
        target_column = st.selectbox(
            "Target Metric",
            options=['total_crimes'] + (df['crime_type'].unique().tolist() if 'crime_type' in df.columns else []),
            index=0
        )
    
    with col2:
        show_history = st.checkbox("Show Historical Data", value=True)
        confidence_level = st.slider("Confidence Interval", 0.50, 0.95, 0.95, 0.05)
    
    if st.button("Generate Forecast"):
        with st.spinner("Training model and generating forecast..."):
            try:
                # Process data
                etl = CrimeDataETL()
                processed_df = etl.process()
                
                # Train forecaster
                forecaster = CrimeForecaster()
                forecaster.fit(processed_df, target_column=target_column)
                
                # Generate forecast
                forecast = forecaster.forecast(periods=forecast_periods, include_history=show_history)
                
                # Evaluation
                metrics = forecaster.evaluate(processed_df, forecast, target_column=target_column)
                
                # Display metrics
                if metrics:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Accuracy", f"{metrics.get('accuracy', 0):.1f}%")
                    with col2:
                        st.metric("MAPE", f"{metrics.get('mape', 0):.1f}%")
                    with col3:
                        st.metric("MAE", f"{metrics.get('mae', 0):.1f}")
                    with col4:
                        st.metric("RMSE", f"{metrics.get('rmse', 0):.1f}")
                
                # Plot forecast
                fig = go.Figure()
                
                # Historical data
                if show_history:
                    historical = processed_df.merge(
                        forecast[['ds', 'yhat']],
                        left_on='incident_date',
                        right_on='ds',
                        how='left'
                    )
                    
                    fig.add_trace(go.Scatter(
                        x=historical['incident_date'],
                        y=historical['total_crimes'],
                        mode='lines',
                        name='Historical',
                        line=dict(color='blue', width=1)
                    ))
                
                # Forecast
                fig.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat'],
                    mode='lines',
                    name='Forecast',
                    line=dict(color='red', width=2)
                ))
                
                # Confidence intervals
                fig.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat_upper'],
                    mode='lines',
                    name='Upper Bound',
                    line=dict(width=0),
                    showlegend=False
                ))
                
                fig.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat_lower'],
                    mode='lines',
                    name='Lower Bound',
                    fill='tonexty',
                    fillcolor='rgba(255,0,0,0.2)',
                    line=dict(width=0),
                    showlegend=False
                ))
                
                fig.update_layout(
                    title="Crime Forecast",
                    xaxis_title="Date",
                    yaxis_title="Crime Count",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Forecast table
                st.subheader("Forecast Details")
                forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
                forecast_display.columns = ['Date', 'Predicted', 'Lower Bound', 'Upper Bound']
                forecast_display['Predicted'] = forecast_display['Predicted'].round(0).astype(int)
                forecast_display['Lower Bound'] = forecast_display['Lower Bound'].round(0).astype(int)
                forecast_display['Upper Bound'] = forecast_display['Upper Bound'].round(0).astype(int)
                
                st.dataframe(forecast_display.tail(forecast_periods), use_container_width=True)
                
            except Exception as e:
                st.error(f"Forecast error: {e}")
                logger.error(f"Forecast error: {e}", exc_info=True)

# Tab 2: Hotspots
with tab2:
    st.header("Crime Hotspots")
    st.markdown("DBSCAN spatial clustering for hotspot detection")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        eps_value = st.slider("EPS (cluster radius)", 0.001, 0.1, 0.01, 0.001)
    
    with col2:
        min_samples = st.slider("Min Samples", 5, 50, 10)
    
    with col3:
        min_days = st.number_input("Min Days (stability)", 0, 365, 30)
    
    if st.button("Detect Hotspots"):
        with st.spinner("Detecting crime hotspots..."):
            try:
                # Detect hotspots
                detector = CrimeHotspotDetector(eps=eps_value, min_samples=min_samples)
                hotspots_df = detector.detect_hotspots(df)
                
                # Filter stable hotspots
                if min_days > 0 and 'incident_date' in hotspots_df.columns:
                    hotspots_df = detector.filter_stable_hotspots(hotspots_df, min_days=min_days)
                    hotspots_df = hotspots_df[hotspots_df['is_stable_hotspot']]
                
                # Calculate density
                density_df = detector.calculate_hotspot_density(hotspots_df)
                
                # Display statistics
                st.subheader("Hotspot Statistics")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Hotspots", len(density_df))
                with col2:
                    st.metric("Total Incidents", hotspots_df[hotspots_df['is_hotspot']].shape[0])
                with col3:
                    avg_density = density_df['density_per_km2'].mean() if len(density_df) > 0 else 0
                    st.metric("Avg Density", f"{avg_density:.1f}/km²")
                with col4:
                    total_area = density_df['area_km2'].sum() if len(density_df) > 0 else 0
                    st.metric("Total Area", f"{total_area:.2f} km²")
                
                # Map visualization
                if len(density_df) > 0:
                    st.subheader("Hotspot Map")
                    
                    # Create map
                    fig = px.scatter_mapbox(
                        density_df,
                        lat="center_latitude",
                        lon="center_longitude",
                        size="n_incidents",
                        color="density_per_km2",
                        hover_data=["cluster_id", "n_incidents", "area_km2"],
                        zoom=10,
                        height=600,
                        mapbox_style="open-street-map",
                        title="Crime Hotspots"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Hotspot table
                    st.subheader("Hotspot Details")
                    st.dataframe(density_df, use_container_width=True)
                else:
                    st.info("No hotspots detected with current parameters.")
                    
            except Exception as e:
                st.error(f"Hotspot detection error: {e}")
                logger.error(f"Hotspot detection error: {e}", exc_info=True)

# Tab 3: Routes
with tab3:
    st.header("Patrol Route Optimization")
    st.markdown("Optimize officer patrol routes to maximize hotspot coverage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_officers = st.number_input("Number of Officers", 1, 20, 3)
        depot_lat = st.number_input("Depot Latitude", 41.0, 42.0, 41.8781, 0.0001)
    
    with col2:
        max_distance = st.number_input("Max Route Distance (km)", 10.0, 200.0, 50.0, 5.0)
        depot_lon = st.number_input("Depot Longitude", -88.0, -87.0, -87.6298, 0.0001)
    
    if st.button("Optimize Routes"):
        with st.spinner("Optimizing patrol routes..."):
            try:
                # First detect hotspots
                detector = CrimeHotspotDetector()
                hotspots_df = detector.detect_hotspots(df)
                density_df = detector.calculate_hotspot_density(hotspots_df)
                
                if len(density_df) == 0:
                    st.warning("No hotspots detected. Please run hotspot detection first.")
                else:
                    # Convert to Hotspot objects
                    hotspots = []
                    for _, row in density_df.iterrows():
                        hotspot = Hotspot(
                            cluster_id=int(row['cluster_id']),
                            center_lat=row['center_latitude'],
                            center_lon=row['center_longitude'],
                            priority=row['density_per_km2'] / 100.0,  # Normalize priority
                            density=row['density_per_km2']
                        )
                        hotspots.append(hotspot)
                    
                    # Optimize routes
                    optimizer = PatrolRouteOptimizer(
                        max_route_distance_km=max_distance,
                        max_shift_hours=8.0,
                        average_speed_kmh=30.0
                    )
                    
                    routes = optimizer.optimize(
                        hotspots=hotspots,
                        num_officers=num_officers,
                        depot_lat=depot_lat,
                        depot_lon=depot_lon
                    )
                    
                    # Display routes
                    st.subheader("Optimized Routes")
                    
                    for route in routes:
                        with st.expander(f"Officer {route.officer_id}: {len(route.hotspots)} hotspots, {route.total_distance:.1f} km"):
                            st.write(f"**Estimated Duration:** {route.estimated_duration:.1f} hours")
                            st.write(f"**Hotspots:** {[h.cluster_id for h in route.hotspots]}")
                    
                    # Route map
                    if len(routes) > 0:
                        st.subheader("Route Map")
                        
                        # Prepare data for map
                        route_data = []
                        for route in routes:
                            for i, hotspot in enumerate(route.hotspots):
                                route_data.append({
                                    'officer': route.officer_id,
                                    'route_order': i,
                                    'latitude': hotspot.center_lat,
                                    'longitude': hotspot.center_lon,
                                    'cluster_id': hotspot.cluster_id
                                })
                        
                        if route_data:
                            route_df = pd.DataFrame(route_data)
                            
                            fig = px.scatter_mapbox(
                                route_df,
                                lat="latitude",
                                lon="longitude",
                                color="officer",
                                size_max=15,
                                zoom=10,
                                height=600,
                                mapbox_style="open-street-map",
                                title="Patrol Routes"
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Route optimization error: {e}")
                logger.error(f"Route optimization error: {e}", exc_info=True)

# Tab 4: Statistics
with tab4:
    st.header("Crime Statistics")
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Incidents", f"{len(df):,}")
    
    with col2:
        if 'incident_date' in df.columns:
            date_range_days = (df['incident_date'].max() - df['incident_date'].min()).days
            st.metric("Date Range", f"{date_range_days} days")
        else:
            st.metric("Date Range", "N/A")
    
    with col3:
        if 'crime_type' in df.columns:
            unique_crimes = df['crime_type'].nunique()
            st.metric("Crime Types", unique_crimes)
        else:
            st.metric("Crime Types", "N/A")
    
    with col4:
        if 'arrest' in df.columns:
            arrest_rate = df['arrest'].mean() * 100
            st.metric("Arrest Rate", f"{arrest_rate:.1f}%")
        else:
            st.metric("Arrest Rate", "N/A")
    
    # Crime type distribution
    if 'crime_type' in df.columns:
        st.subheader("Crime Type Distribution")
        
        crime_counts = df['crime_type'].value_counts().head(10)
        
        fig = px.bar(
            x=crime_counts.values,
            y=crime_counts.index,
            orientation='h',
            labels={'x': 'Count', 'y': 'Crime Type'},
            title="Top 10 Crime Types"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Temporal trends
    if 'incident_date' in df.columns:
        st.subheader("Temporal Trends")
        
        # Daily counts
        daily_counts = df.groupby(df['incident_date'].dt.date).size().reset_index(name='count')
        daily_counts.columns = ['date', 'count']
        
        fig = px.line(
            daily_counts,
            x='date',
            y='count',
            labels={'date': 'Date', 'count': 'Incidents'},
            title="Daily Crime Incidents"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Geospatial distribution
    if 'latitude' in df.columns and 'longitude' in df.columns:
        st.subheader("Geospatial Distribution")
        
        # Sample data for map (can be slow with large datasets)
        sample_size = min(10000, len(df))
        sample_df = df.sample(sample_size)
        
        fig = px.density_mapbox(
            sample_df,
            lat='latitude',
            lon='longitude',
            radius=10,
            zoom=10,
            height=600,
            mapbox_style="open-street-map",
            title="Crime Density Heatmap"
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Foresight Crime Prediction Platform** | Predictive Crime Intelligence")

