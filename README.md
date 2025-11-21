# Video Game Sales Exploratory Dashboard

An interactive data visualization dashboard built with Python and Streamlit for exploring video game sales data. This project was developed as part of the CEN445 Introduction to Data Visualization course assignment.

## 📊 Project Overview

This dashboard provides comprehensive visualizations and interactive analysis tools for exploring video game sales data across different regions, genres, platforms, and time periods. The application offers 9 distinct visualization techniques, including 6 advanced visualization types, all with interactive features such as filtering, zooming, panning, and hover tooltips.

**GitHub Repository:** [https://github.com/ismaillcann/data-visualization](https://github.com/ismaillcann/data-visualization)

## 📁 Dataset

### Dataset Information
- **Dataset Name:** Video Game Sales
- **Source:** Kaggle - [Video Game Sales Dataset](https://www.kaggle.com/datasets/gregorut/videogamesales)
- **Total Rows:** 16,600 (first 5,000 rows used for analysis)
- **Columns:** 11 columns including:
  - `Rank` - Ranking of overall sales
  - `Name` - The name of the game
  - `Platform` - Platform of the game (e.g., PC, PS4, XBOX)
  - `Year` - Year of the game's release
  - `Genre` - Genre of the game (e.g., Action, Sports, RPG)
  - `Publisher` - Publisher of the game
  - `NA_Sales` - Sales in North America (in millions)
  - `EU_Sales` - Sales in Europe (in millions)
  - `JP_Sales` - Sales in Japan (in millions)
  - `Other_Sales` - Sales in the rest of the world (in millions)
  - `Global_Sales` - Total worldwide sales (in millions)

### Dataset Context
The Video Game Sales dataset contains historical sales data for video games across multiple platforms and regions. It provides insights into market trends, platform preferences, genre popularity, and regional sales patterns in the gaming industry.

## 🎯 Main Goals of Analysis

1. **Temporal Analysis:** Explore sales trends over time and identify peak periods in the gaming industry
2. **Genre Performance:** Analyze which game genres perform best across different time periods
3. **Platform Comparison:** Compare sales performance across different gaming platforms
4. **Regional Insights:** Understand regional preferences and sales distributions (NA, EU, JP, Other)
5. **Market Leaders:** Identify top-performing games, publishers, and platform-genre combinations
6. **Multi-dimensional Relationships:** Discover correlations and relationships between different sales variables

## 🛠️ Data Preprocessing

The dataset underwent comprehensive preprocessing to ensure data quality:

1. **Missing Values Handling:**
   - Publisher missing values were filled with "Unknown"
   - Year missing values were removed (critical for time series analysis)
   - Sales columns were converted to numeric and missing values filled with 0.0

2. **Data Type Conversion:**
   - Year converted to integer
   - Sales columns converted to numeric format
   - Created derived column: `Decade` for temporal grouping

3. **Data Cleaning:**
   - Removed negative sales values (set to 0)
   - Reset index after filtering
   - Created `Total_Regional_Sales` as sum of regional sales columns

4. **Data Filtering:**
   - Used first 5,000 rows for performance optimization
   - Applied user-defined filters for Genre, Platform, Year Range, and Top N games

## 📈 Visualization Techniques

The dashboard includes **9 distinct visualizations**, with **6 advanced visualization types**:

### Basic Visualizations:
1. **Line Chart** - Global Sales Over Time by Year
   - Shows overall sales trends across years
   - Interactive hover tooltips and zoom/pan capabilities

2. **Area Chart** - Genre-wise Sales Over Time
   - Stacked area chart displaying sales contributions by genre over time
   - Color-coded by genre with interactive legend

3. **Bar Chart** - Top 20 Games by Global Sales
   - Horizontal/vertical bar chart with color coding by platform
   - Hover data includes Genre, Publisher, and Year

### Advanced Visualizations:
4. **Sankey Diagram** - Genre ↔ Platform Sales Flow
   - Flow diagram showing relationships between game genres and platforms
   - Node thickness represents sales volume
   - Interactive hover highlighting and color-coded nodes

5. **Treemap** - Genre → Publisher → Game Hierarchy
   - Hierarchical visualization showing sales distribution
   - Size represents sales volume, color represents hierarchy level
   - Interactive click-to-drill-down functionality

6. **Parallel Coordinates** - Regional vs Global Sales Comparison
   - Multi-dimensional visualization comparing regional sales patterns
   - Normalized data for fair comparison
   - Color gradient based on Global Sales

7. **Correlation Heatmap** - Sales Variables Relationships
   - Matrix visualization showing correlations between sales columns
   - Color intensity represents correlation strength
   - Interactive hover tooltips with exact correlation values

8. **Scatter Matrix** - Multi-dimensional Sales Relationships
   - Pairwise scatter plots showing relationships between sales variables
   - Color-coded by Genre
   - Interactive selection and filtering capabilities

9. **Sunburst Chart** - Genre → Platform Sales Structure
   - Hierarchical circular visualization
   - Inner ring: Genres, Outer ring: Platforms
   - Area represents sales volume

## 🎛️ Interactive Components

The dashboard includes **4 interactive filtering components**:

1. **Genre Selectbox** - Filter games by genre (includes "All" option)
2. **Platform Multiselect** - Select multiple platforms for comparison
3. **Year Range Slider** - Filter data by release year range
4. **Top N Games Selectbox** - Display top N games by global sales (All, 50, 100, 200)

All visualizations update dynamically based on filter selections, and each chart includes:
- **Mouse hover effects** with detailed tooltips
- **Zoom and pan** capabilities
- **Color highlighting** on interaction
- **Responsive layout** for different screen sizes

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ismaillcann/data-visualization.git
   cd data-visualization
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure the dataset file is present:**
   - The `vgsales.csv` file should be in the project root directory
   - If not present, download from [Kaggle](https://www.kaggle.com/datasets/gregorut/videogamesales)

5. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

6. **Access the dashboard:**
   - The application will open automatically in your default web browser
   - Default URL: `http://localhost:8501`

### Requirements
The project requires the following Python packages (specified in `requirements.txt`):
- streamlit
- pandas
- numpy
- plotly

## 💡 Key Insights and Findings

1. **Temporal Trends:** The gaming industry experienced significant growth in certain decades, with peak sales periods identifiable through the time series visualizations.

2. **Genre Dominance:** Action and Sports genres consistently show strong performance across different platforms, as revealed by the genre-wise area chart.

3. **Platform Preferences:** Different platforms show distinct genre preferences, with certain platforms dominating specific genres (visible in Sankey and Sunburst charts).

4. **Regional Patterns:** Strong correlations exist between regional sales, particularly between NA and EU sales, while JP sales show more independence (shown in correlation heatmap).

5. **Market Concentration:** Top-performing games account for a disproportionate share of total sales, indicating market concentration in the gaming industry (treemap visualization).

6. **Publisher Performance:** Major publishers dominate certain genres, creating distinct market segments (visible in treemap hierarchy).

7. **Multi-dimensional Relationships:** The parallel coordinates and scatter matrix reveal complex relationships between regional sales patterns, showing that games successful in one region often succeed in others.

## 📁 Project Structure

```
data-visualization/
├── app.py                 # Main Streamlit application
├── vgsales.csv           # Dataset file
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── .gitignore          # Git ignore file
```

## 👥 Team Contributions

- **Team Member 1 / Ömer:** Data preprocessing, basic visualizations (Line, Area, Bar charts), and dashboard layout design
- **Team Member 2 / Ali:** Advanced visualizations (Sankey, Treemap, Parallel Coordinates) and interactivity implementation
- **Team Member 3/ İsmail:** Advanced visualizations (Heatmap, Scatter Matrix, Sunburst), README documentation, and GitHub repository management

## 🔧 Technical Details

- **Framework:** Streamlit (v1.51.0+)
- **Visualization Libraries:** Plotly Express, Plotly Graph Objects
- **Data Processing:** Pandas, NumPy
- **Deployment:** Local Streamlit server (can be deployed to Streamlit Cloud)

## 📝 Notes

- The dashboard uses the first 5,000 rows of the dataset for optimal performance
- All visualizations are interactive and responsive
- Filter selections persist across tab navigation
- Data is cached using Streamlit's `@st.cache_data` decorator for improved performance

## 📄 License

This project is created for educational purposes as part of the CEN445 course assignment.

---

**Course:** CEN445 - Introduction to Data Visualization  
**Institution:** Computer Engineering Faculty 
**Academic Year:** 2024-2025
