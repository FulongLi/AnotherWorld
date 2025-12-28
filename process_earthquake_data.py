"""
Process earthquake data from USGS GeoJSON file and visualize earthquakes with magnitude > 7.0.
Highlights earthquakes with magnitude > 8.0.
"""

import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path


def load_earthquake_data(json_file_path):
    """
    Load earthquake data from GeoJSON file.
    
    Args:
        json_file_path: Path to the JSON file
        
    Returns:
        List of earthquake features
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get('features', [])


def process_earthquake_data(features, min_magnitude=7.0):
    """
    Process earthquake features and extract relevant data.
    
    Args:
        features: List of earthquake feature dictionaries
        min_magnitude: Minimum magnitude threshold
        
    Returns:
        List of dictionaries with processed earthquake data
    """
    earthquakes = []
    
    for feature in features:
        props = feature.get('properties', {})
        mag = props.get('mag')
        time_ms = props.get('time')
        
        # Skip if magnitude or time is missing
        if mag is None or time_ms is None:
            continue
        
        # Filter by minimum magnitude
        if mag > min_magnitude:
            try:
                # Convert time from milliseconds to datetime (UTC)
                # Handle negative timestamps (pre-1970 dates) differently
                if time_ms < 0:
                    # For negative timestamps, calculate directly
                    # Unix epoch is 1970-01-01, so negative values are before that
                    # Convert milliseconds to seconds and add to epoch
                    from datetime import timedelta
                    epoch = datetime(1970, 1, 1)
                    time_dt = epoch + timedelta(milliseconds=time_ms)
                else:
                    time_dt = datetime.utcfromtimestamp(time_ms / 1000.0)
                
                # Filter: only include earthquakes from 1900 onwards
                min_date = datetime(1900, 1, 1)
                if time_dt >= min_date:
                    earthquakes.append({
                        'magnitude': mag,
                        'time': time_dt,
                        'place': props.get('place', 'Unknown'),
                        'time_ms': time_ms
                    })
            except (ValueError, OSError, OverflowError) as e:
                # Skip invalid timestamps
                continue
    
    # Sort by time
    earthquakes.sort(key=lambda x: x['time'])
    
    return earthquakes


def plot_earthquakes(earthquakes, output_file='earthquake_plot.png'):
    """
    Create a plot showing earthquakes with magnitude > 7.0.
    Highlights earthquakes with magnitude > 8.0.
    
    Args:
        earthquakes: List of processed earthquake dictionaries
        output_file: Path to save the plot
    """
    if not earthquakes:
        print("No earthquakes found with magnitude > 7.0")
        return
    
    # Separate earthquakes by magnitude threshold
    earthquakes_7_to_8 = [eq for eq in earthquakes if 7.0 < eq['magnitude'] <= 8.0]
    earthquakes_above_8 = [eq for eq in earthquakes if eq['magnitude'] > 8.0]
    
    # Extract data for plotting
    times_7_to_8 = [eq['time'] for eq in earthquakes_7_to_8]
    mags_7_to_8 = [eq['magnitude'] for eq in earthquakes_7_to_8]
    
    times_above_8 = [eq['time'] for eq in earthquakes_above_8]
    mags_above_8 = [eq['magnitude'] for eq in earthquakes_above_8]
    
    # Create the plot
    plt.figure(figsize=(14, 8))
    
    # Plot earthquakes with magnitude 7.0-8.0
    if earthquakes_7_to_8:
        plt.scatter(times_7_to_8, mags_7_to_8, 
                   c='blue', s=50, alpha=0.6, 
                   label=f'Magnitude 7.0-8.0 (n={len(earthquakes_7_to_8)})',
                   edgecolors='darkblue', linewidths=0.5)
    
    # Plot earthquakes with magnitude > 8.0 (highlighted)
    if earthquakes_above_8:
        # Sort by time for connecting line
        sorted_above_8 = sorted(zip(times_above_8, mags_above_8), key=lambda x: x[0])
        sorted_times_above_8 = [t for t, m in sorted_above_8]
        sorted_mags_above_8 = [m for t, m in sorted_above_8]
        
        # Connect peaks with dashed line
        plt.plot(sorted_times_above_8, sorted_mags_above_8, 
                'r--', alpha=0.5, linewidth=1.5, zorder=4)
        
        # Plot red circles for magnitude > 8.0
        plt.scatter(times_above_8, mags_above_8, 
                   c='red', s=150, alpha=0.8, 
                   label=f'Magnitude > 8.0 (n={len(earthquakes_above_8)})',
                   edgecolors='darkred', linewidths=1.5, zorder=5)
    
    # Customize the plot
    plt.xlabel('Time', fontsize=12, fontweight='bold')
    plt.ylabel('Magnitude', fontsize=12, fontweight='bold')
    plt.title('Earthquakes with Magnitude > 7.0\n(Highlighted: Magnitude > 8.0)', 
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(loc='best', fontsize=10)
    
    # Set x-axis limits - start from 1900
    all_times = times_7_to_8 + times_above_8
    if all_times:
        min_time = min(all_times)
        max_time = max(all_times)
        # Ensure x-axis starts from 1900-01-01
        x_min = datetime(1900, 1, 1)
        # Use the later of: actual max time or 2026 (to show future data)
        x_max = max(max_time, datetime(2026, 1, 1))
        plt.xlim(x_min, x_max)
        print(f"X-axis range: {x_min.strftime('%Y-%m-%d')} to {x_max.strftime('%Y-%m-%d')}")
        print(f"Data range: {min_time.strftime('%Y-%m-%d')} to {max_time.strftime('%Y-%m-%d')}")
    
    # Format x-axis dates - 20 year intervals
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # Set locator to show every 20 years, starting from 1900
    year_locator = mdates.YearLocator(20)
    plt.gca().xaxis.set_major_locator(year_locator)
    plt.gcf().autofmt_xdate()  # Rotate date labels
    
    # Set y-axis limits
    if mags_7_to_8 or mags_above_8:
        all_mags = mags_7_to_8 + mags_above_8
        plt.ylim(min(all_mags) - 0.2, max(all_mags) + 0.3)
    
    # Add horizontal line at magnitude 8.0 for reference
    plt.axhline(y=8.0, color='orange', linestyle='--', linewidth=1, alpha=0.5, 
                label='Magnitude 8.0 threshold')
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {output_file}")
    
    # Display summary statistics
    print(f"\nSummary Statistics:")
    print(f"Total earthquakes with magnitude > 7.0: {len(earthquakes)}")
    print(f"Earthquakes with magnitude 7.0-8.0: {len(earthquakes_7_to_8)}")
    print(f"Earthquakes with magnitude > 8.0: {len(earthquakes_above_8)}")
    
    if earthquakes_above_8:
        print(f"\nEarthquakes with magnitude > 8.0:")
        for eq in earthquakes_above_8:
            print(f"  {eq['time'].strftime('%Y-%m-%d')}: M {eq['magnitude']:.1f} - {eq['place']}")
    
    plt.show()


def main():
    """Main function to process and visualize earthquake data."""
    # Path to the JSON file
    json_file = Path('models/worldearthquakedata.json')
    
    if not json_file.exists():
        print(f"Error: File not found: {json_file}")
        return
    
    print(f"Loading earthquake data from {json_file}...")
    features = load_earthquake_data(json_file)
    print(f"Loaded {len(features)} earthquake records")
    
    print("\nProcessing earthquakes with magnitude > 7.0...")
    earthquakes = process_earthquake_data(features, min_magnitude=7.0)
    print(f"Found {len(earthquakes)} earthquakes with magnitude > 7.0")
    
    print("\nCreating visualization...")
    plot_earthquakes(earthquakes, output_file='earthquake_plot.png')


if __name__ == '__main__':
    main()

