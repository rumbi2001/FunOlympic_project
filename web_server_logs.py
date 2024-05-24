from datetime import datetime, timedelta
from random import randint, choice
import csv
from faker import Faker
import os

fake = Faker()

def generate_ip():
    """
    Generate a random IP address.

    Returns:
        str: A randomly generated IP address.
    """
    return ".".join(map(str, (randint(0, 255) for _ in range(4))))

def generate_logs(num_entries=300):
    """
    Generate a list of web server log entries.

    Args:
        num_entries (int): The number of log entries to generate.

    Returns:
        list: A list of log entries, each entry is a list containing timestamp, IP address, method, endpoint, status,
              country, type of sporting activities, device, browser, and duration.
    """
    endpoints = ["/index.html", "/images/games.jpg", "/searchsports.php", "/football.html"]
    methods = ["GET", "POST"]
    statuses = [200, 304, 404, 500]
    countries = [fake.country() for _ in range(100)]  # Generate a list of 100 random countries
    devices = ["Desktop", "Mobile", "Tablet"]
    browsers = ["Chrome", "Firefox", "Safari", "Edge"]
    sports_activities = ["Football", "Basketball", "Tennis", "Swimming", "Running", "Cycling", "Golf", "Baseball", "Cricket", "Volleyball"]

    log_entries = []
    start_time = datetime.now()

    for _ in range(num_entries):
        timestamp = (start_time + timedelta(seconds=randint(0, 100000))).strftime('%Y-%m-%d %H:%M:%S')
        ip_address = generate_ip()
        method = choice(methods)
        endpoint = choice(endpoints)
        status = choice(statuses)
        country = choice(countries)
        sports_activity = choice(sports_activities)
        device = choice(devices)
        browser = choice(browsers)
        log_entry = [timestamp, ip_address, method, endpoint, status, country, sports_activity, device, browser]
        log_entries.append(log_entry)

    # Sort log entries by timestamp
    log_entries.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'))

    # Calculate and add duration
    for i in range(1, len(log_entries)):
        prev_time = datetime.strptime(log_entries[i - 1][0], '%Y-%m-%d %H:%M:%S')
        curr_time = datetime.strptime(log_entries[i][0], '%Y-%m-%d %H:%M:%S')
        duration = (curr_time - prev_time).total_seconds()
        log_entries[i].append(duration)

    # Add duration for the first log entry
    log_entries[0].append(0.0)

    return log_entries

def save_logs_to_csv(log_entries, filename="web_server_logs.csv"):
    """
    Save log entries to a CSV file. Append if the file exists, else create a new one.

    Args:
        log_entries (list): A list of log entries to save.
        filename (str): The name of the CSV file to save the log entries to.
    """
    # Check if the file exists to determine the write mode
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header only if the file is being created
        if not file_exists:
            writer.writerow(["Timestamp", "IP Address", "Method", "Endpoint", "Status",
                             "Country", "Sports Activity", "Device", "Browser", "Duration"])
        writer.writerows(log_entries)

if __name__ == "__main__":
    logs = generate_logs()
    save_logs_to_csv(logs)
