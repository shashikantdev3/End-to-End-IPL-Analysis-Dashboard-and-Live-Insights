# End-to-End IPL Analysis Dashboard and Live Insights

This project provides a comprehensive solution for analyzing Indian Premier League (IPL) data, offering both historical insights and a live score dashboard. It covers the entire data lifecycle from cleaning and ETL to visualization.

## Features

-   **Data Cleaning and Preprocessing**: Jupyter notebook for cleaning and preparing raw IPL data.
-   **ETL Pipeline**: Python scripts for Extracting, Transforming, and Loading IPL match and ball-by-ball data.
-   **Historical IPL Analysis Dashboard**: Power BI dashboard for in-depth analysis of past IPL seasons.
-   **Live IPL Score Dashboard**: Power BI dashboard designed to provide real-time or near real-time match insights.
-   **Database Connection Testing**: Python script to test database connectivity for data storage.

## Technologies Used

-   **Python**: For data cleaning, ETL processes, and database interactions.
    -   Jupyter Notebooks
-   **Microsoft Power BI**: For creating interactive dashboards and visualizations.
-   **Microsoft Excel**: For storing raw and intermediate data.
-   **SQL**: For database management and querying.

## Project Structure

-   `Data Cleaning.ipynb`: Jupyter notebook for data cleaning and exploration.
-   `ETL_pipeline.py`: Python script containing the ETL logic.
-   `IPL Historical Analysis.pbix`: Power BI file for historical data analysis.
-   `IPL Live Score Dashboard.pbix`: Power BI file for live score visualization.
-   `db_connection_test.py`: Python script to verify database connections.
-   `ipl_matches_2008_2025.xlsx`: Excel file containing IPL match data.
-   `ipl_ball_by_ball_2008_2025.xlsx`: Excel file containing ball-by-ball IPL data.
-   `historical_data/`: Directory likely containing additional historical data files.
-   `Live Data Excel/`: Directory likely used for live data feeds or temporary storage.
-   `Team_Logo.xlsx`: Excel file potentially storing team logos or related metadata.
-   `Analysis_bg.png`, `Points Table Bg.png`, `IPL-BG-Second.png`, `Main Background.png`: Image files used for dashboard backgrounds and aesthetics.
-   `Cleaned_IPL_Player_Summary_With_Img.csv`: Cleaned CSV containing player summaries with image links.

## Setup and Usage

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/shashikantdev3/End-to-End-IPL-Analysis-Dashboard-and-Live-Insights.git
    cd "End-to-End IPL Analysis Dashboard and Live Insights"
    ```
2.  **Prepare Data**: Ensure `ipl_matches_2008_2025.xlsx` and `ipl_ball_by_ball_2008_2025.xlsx` are in the project root or specified data directories.
3.  **Run ETL Pipeline**:
    Execute the `ETL_pipeline.py` script to process and load the data. You may need to configure database connection details within this script or `db_connection_test.py` first.
    ```bash
    python ETL_pipeline.py
    ```
4.  **Open Power BI Dashboards**:
    Open `IPL Historical Analysis.pbix` and `IPL Live Score Dashboard.pbix` with Power BI Desktop to view the dashboards. Ensure Power BI is configured to connect to your data source (which should be populated by the ETL pipeline).

## Contributing

Feel free to fork this repository, submit pull requests, or open issues for any bugs or feature requests. 
