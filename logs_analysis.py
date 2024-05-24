import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geoip2.database import Reader

def load_data(filename='web_server_logs.csv'):
    """
    Load web server logs from a CSV file.

    Args:
        filename (str): The name of the CSV file to load data from.

    Returns:
        pd.DataFrame: A DataFrame containing the web server logs.
    """
    return pd.read_csv(filename, encoding='utf-8')

def get_country_from_ip(ip, reader):
    try:
        response = reader.city(ip)
        return response.country.name
    except Exception:
        return "Unknown"

def analyze_logs(logs, reader):
    """
    Analyze web server logs to extract insights.

    Args:
        logs (pd.DataFrame): The web server logs DataFrame.
        reader (geoip2.database.Reader): The GeoIP2 reader instance.

    Returns:
        dict: A dictionary containing analysis results.
    """
    logs['Country'] = logs['IP Address'].apply(get_country_from_ip, args=(reader,))

    visits_per_country = logs['Country'].value_counts()
    main_interests = logs['Endpoint'].value_counts()

    logs['Timestamp'] = pd.to_datetime(logs['Timestamp'], format='%H:%M:%S')
    logs['Next Timestamp'] = logs.groupby('IP Address')['Timestamp'].shift(-1)
    logs['Duration'] = (logs['Next Timestamp'] - logs['Timestamp']).dt.total_seconds().fillna(0)
    average_duration = logs['Duration'].mean()
    duration_std = logs['Duration'].std()

    return {
        'visits_per_country': visits_per_country,
        'main_interests': main_interests,
        'average_duration': average_duration,
        'duration_std': duration_std
    }

def generate_visualizations(analysis_results):
    """
    Generate visualizations from analysis results.

    Args:
        analysis_results (dict): The analysis results.
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x=analysis_results['visits_per_country'].index, y=analysis_results['visits_per_country'].values)
    plt.title('Number of Visits per Country')
    plt.xlabel('Country')
    plt.ylabel('Number of Visits')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('visits_per_country.png')

    plt.figure(figsize=(10, 6))
    sns.barplot(x=analysis_results['main_interests'].index, y=analysis_results['main_interests'].values)
    plt.title('Main Interests based on Viewed Endpoints')
    plt.xlabel('Endpoint')
    plt.ylabel('Number of Visits')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('main_interests.png')

def save_report(analysis_results, filename='report.txt'):
    """
    Save a report of the analysis results to a text file.

    Args:
        analysis_results (dict): The analysis results.
        filename (str): The name of the text file to save the report to.
    """
    report = f"""
    Report:
    ---------
    Number of Visits per Country:
    {analysis_results['visits_per_country'].to_string()}

    Main Interests based on Viewed Endpoints:
    {analysis_results['main_interests'].to_string()}

    Average Duration: {analysis_results['average_duration']} seconds
    Standard Deviation of Duration: {analysis_results['duration_std']} seconds
    """
    with open(filename, "w", encoding='utf-8') as file:
        file.write(report)

if __name__ == "__main__":
    logs = load_data()
    reader = Reader('GeoLite2-City.mmdb')
    analysis_results = analyze_logs(logs, reader)
    generate_visualizations(analysis_results)
    save_report(analysis_results)
    reader.close()
