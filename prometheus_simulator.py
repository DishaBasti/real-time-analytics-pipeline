from prometheus_client import start_http_server, Gauge, Counter
import time
import csv
from datetime import datetime

# Prometheus metrics
state_program_preferences = Gauge('state_program_preferences', 'Program Preferences by State', ['state', 'program'])
match_tournament_views = Gauge('match_tournament_views', 'Match Views During Tournaments', ['state'])
program_watch_time = Gauge('program_watch_time', 'Time Spent Watching Programs', ['state', 'program'])
urban_rural_news_views = Gauge('urban_rural_news_views', 'News Views by Urban vs Rural', ['location'])
instant_switches = Counter('instant_switches', 'Instant Switch Events During Important Times', ['state'])
program_views_counter = Counter('program_views_counter', 'Total Views per Program', ['state', 'program'])

def simulate_real_time_data(file_path, filter_date=None, max_rows=1000, delay=1):
    row_count = 0
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row_count >= max_rows:
                print(f"Reached the limit of {max_rows} rows. Stopping.")
                break

            try:
                timestamp = row['Timestamp']
                timestamp_date = datetime.strptime(timestamp, "%d-%m-%Y %H:%M:%S").date()
            except ValueError:
                print(f"Skipping invalid timestamp: {row['Timestamp']}")
                continue

            if filter_date and timestamp_date != filter_date:
                continue

            state = row['State']
            program = row['Program']
            user_type = row['User_Type']
            view_minutes = float(row['View_Min'])
            event_type = row['Event_Type']

            state_program_preferences.labels(state=state, program=program).set(view_minutes)
            if "Match" in program and "Tournament" in program:
                match_tournament_views.labels(state=state).set(view_minutes)
            program_watch_time.labels(state=state, program=program).set(view_minutes)
            if user_type == "Urban" and "News" in program:
                urban_rural_news_views.labels(location="Urban").inc(view_minutes)
            elif user_type == "Rural" and "News" in program:
                urban_rural_news_views.labels(location="Rural").inc(view_minutes)
            if event_type == "channel_switch":
                instant_switches.labels(state=state).inc(1)
            program_views_counter.labels(state=state, program=program).inc(1)

            print(f"Metrics updated: {state}, {program}, {view_minutes} mins, {user_type}, {event_type}")
            row_count += 1
            time.sleep(delay)

if __name__ == "__main__":
    start_http_server(8000)
    filter_date = datetime.strptime("02-03-2024", "%d-%m-%Y").date()
    simulate_real_time_data('sample_data.csv', filter_date, max_rows=1000, delay=5)
