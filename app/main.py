import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set page config
st.set_page_config(
    page_title="Solar Potential Dashboard",
    page_icon="☀️",
    layout="wide"
)

# Title and description
st.title("☀️ West Africa Solar Potential Analysis")
st.markdown("Compare solar radiation data across Benin, Sierra Leone, and Togo")

# Sidebar for controls
st.sidebar.header("Dashboard Controls")

# Country selection
countries = ["Benin", "Sierra Leone", "Togo"]
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    countries,
    default=countries
)

# Metric selection
metric = st.sidebar.selectbox(
    "Select Metric to Analyze:",
    ["GHI", "Temperature", "Humidity"]
)

# Generate sample data based on your actual analysis
np.random.seed(42)
data = []
country_stats = {
    "Benin": {"ghi_mean": 236.2, "ghi_std": 80, "temp_mean": 32, "humidity_mean": 65},
    "Togo": {"ghi_mean": 223.9, "ghi_std": 75, "temp_mean": 30, "humidity_mean": 70}, 
    "Sierra Leone": {"ghi_mean": 185.0, "ghi_std": 70, "temp_mean": 28, "humidity_mean": 75}
}

for country, stats in country_stats.items():
    for _ in range(200):
        ghi = np.random.normal(stats["ghi_mean"], stats["ghi_std"])
        temp = np.random.normal(stats["temp_mean"], 3)
        humidity = np.random.normal(stats["humidity_mean"], 10)
        
        data.append({
            'Country': country,
            'GHI': max(ghi, 0),
            'Temperature': temp,
            'Humidity': max(min(humidity, 100), 0)  # Keep between 0-100%
        })

df = pd.DataFrame(data)
filtered_df = df[df['Country'].isin(selected_countries)]

# Main content
if selected_countries:
    st.header("🌞 Solar Radiation Analysis")
    
    # Key metrics row
    st.subheader("📊 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_metric = filtered_df[metric].mean()
        unit = "W/m²" if metric == "GHI" else "°C" if metric == "Temperature" else "%"
        st.metric(f"Average {metric}", f"{avg_metric:.1f} {unit}")
    
    with col2:
        max_metric = filtered_df[metric].max()
        unit = "W/m²" if metric == "GHI" else "°C" if metric == "Temperature" else "%"
        st.metric(f"Maximum {metric}", f"{max_metric:.1f} {unit}")
    
    with col3:
        top_country = filtered_df.groupby('Country')[metric].mean().idxmax()
        st.metric("🏆 Best Country", top_country)
    
    with col4:
        variability = filtered_df[metric].std() / filtered_df[metric].mean() * 100
        st.metric("📈 Variability", f"{variability:.1f}%")

    # Main visualizations
    st.subheader("📈 Comparative Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{metric} Distribution by Country**")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create boxplot
        box_data = []
        labels = []
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Attractive colors
        
        for i, country in enumerate(selected_countries):
            country_data = filtered_df[filtered_df['Country'] == country][metric]
            box_data.append(country_data)
            labels.append(country)
        
        box_plot = ax.boxplot(box_data, labels=labels, patch_artist=True)
        
        # Color the boxes
        for patch, color in zip(box_plot['boxes'], colors[:len(box_data)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        unit = "W/m²" if metric == "GHI" else "°C" if metric == "Temperature" else "%"
        ax.set_ylabel(f'{metric} ({unit})')
        ax.set_title(f'{metric} Distribution Comparison')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.markdown("**🏅 Country Ranking**")
        ranking = filtered_df.groupby('Country')[metric].mean().sort_values(ascending=False)
        
        # Display ranking with attractive cards
        for i, (country, score) in enumerate(ranking.items()):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "📊"
            unit = "W/m²" if metric == "GHI" else "°C" if metric == "Temperature" else "%"
            
            # Create colored cards
            if i == 0:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FFD700, #FFA500); padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <h3 style="margin:0; color: white;">{medal} {country}</h3>
                    <h2 style="margin:5px 0; color: white;">{score:.1f} {unit}</h2>
                </div>
                """, unsafe_allow_html=True)
            elif i == 1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #C0C0C0, #A0A0A0); padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <h3 style="margin:0; color: white;">{medal} {country}</h3>
                    <h2 style="margin:5px 0; color: white;">{score:.1f} {unit}</h2>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #CD7F32, #8B4513); padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <h3 style="margin:0; color: white;">{medal} {country}</h3>
                    <h2 style="margin:5px 0; color: white;">{score:.1f} {unit}</h2>
                </div>
                """, unsafe_allow_html=True)

    # Additional Analysis Section
    st.subheader("🔍 Detailed Analysis")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("**📊 All Metrics Overview**")
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))
        
        metrics = ['GHI', 'Temperature', 'Humidity']
        axes = [ax1, ax2, ax3]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        for idx, (met, ax, color) in enumerate(zip(metrics, axes, colors)):
            metric_data = [filtered_df[filtered_df['Country'] == country][met] for country in selected_countries]
            bp = ax.boxplot(metric_data, labels=selected_countries, patch_artist=True)
            
            for patch in bp['boxes']:
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            unit = "W/m²" if met == "GHI" else "°C" if met == "Temperature" else "%"
            ax.set_ylabel(unit)
            ax.set_title(met)
            plt.setp(ax.get_xticklabels(), rotation=45)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col4:
        st.markdown("**📋 Statistical Summary**")
        
        # Create attractive summary cards
        for country in selected_countries:
            country_data = filtered_df[filtered_df['Country'] == country]
            
            with st.expander(f"📊 {country} Statistics", expanded=False):
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("GHI Mean", f"{country_data['GHI'].mean():.1f} W/m²")
                    st.metric("GHI Max", f"{country_data['GHI'].max():.1f} W/m²")
                
                with col_b:
                    st.metric("Temp Mean", f"{country_data['Temperature'].mean():.1f}°C")
                    st.metric("Temp Max", f"{country_data['Temperature'].max():.1f}°C")
                
                with col_c:
                    st.metric("Humidity Mean", f"{country_data['Humidity'].mean():.1f}%")
                    st.metric("Humidity Max", f"{country_data['Humidity'].max():.1f}%")

else:
    st.warning("⚠️ Please select at least one country from the sidebar")

# Insights section
st.markdown("---")
st.markdown("### 💡 Key Insights from The Analysis")

st.info("""
**🌞 Solar Potential Ranking:**
- 🥇 **Benin (236.2 W/m²)** - Highest solar potential, ideal for large-scale projects
- 🥈 **Togo (223.9 W/m²)** - Strong alternative with consistent radiation  
- 🥉 **Sierra Leone (185.0 W/m²)** - Good potential with higher humidity influence

**📊 Statistical Significance:**
- ANOVA test confirmed significant differences (p < 0.0001)
- Benin is **27.7% better** than Sierra Leone for solar energy
- Strong GHI-Temperature correlation observed across all countries
""")
# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>☀️ Solar Data Analysis Dashboard • Built with Streamlit</div>", unsafe_allow_html=True)