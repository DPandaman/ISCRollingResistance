# IMPORTANT:
# This sctip
# Overall file was Rolling Resistance Data.csv
#     -> This file contained data from multiple trial runs, 'pull-backs', bad data, etc
#     -> FIltered files do not match up with the videos, so I am using the overall .csv file right now.
# Sectioned data is located in the Separated Data folder: (descriptions based on videos. Data somehow does not align)
#     -> Trial #1: Not a good sample, Calypso stopped almost instantly + values do not fluctuate
#     -> Trial #2: Do not use, filtering between trials
#     -> Trial #3: Good data sample 
#     -> Trial #4: Good data sample
#     -> Trial #5: Not a good sample, Calypso stopped almost instantly + values do not fluctuate
#     -> Trial #6: Good data sample
# Hopefully this data and my script are useful to analyze how we can improve the car
# pls guys we need better data and we need it to be separated really good bc its lowkey kinda dummy rn :(
# Further plans are to get more data samples from better running conditions (ex. road, weather, measuring instruments)
# -Devanshu Pandya

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

# Function to compute average acceleration from CSV
def compute_average_acceleration(csv_file, nrows=3000):
    # Read the CSV file into DataFrame
    df = pd.read_csv(csv_file)
    
    # Process the data for each of the 3 runs (each set of x, y, z)
    run_columns = ['Acceleration - x (m/s²) Run 1', 'Acceleration - y (m/s²) Run 1', 'Acceleration - z (m/s²) Run 1',
                   'Acceleration - x (m/s²) Run 2', 'Acceleration - y (m/s²) Run 2', 'Acceleration - z (m/s²) Run 2',
                   'Acceleration - x (m/s²) Run 3', 'Acceleration - y (m/s²) Run 3', 'Acceleration - z (m/s²) Run 3']
    
    # Calculate the magnitude for each run
    magnitudes = []
    for i in range(0, len(run_columns), 3):  # Loop over each run (x, y, z for each run)
        x = df[run_columns[i]]
        y = df[run_columns[i+1]]
        z = df[run_columns[i+2]]
        
        # Calculate magnitude for each row in the dataframe for this run
        magnitudes.append(np.sqrt(x**2 + y**2 + z**2))

    # Convert list of magnitudes into a DataFrame (one column per run)
    magnitude_df = pd.DataFrame(magnitudes).transpose()
    magnitude_df.columns = ['Run 1 Magnitude', 'Run 2 Magnitude', 'Run 3 Magnitude']
    
    # Calculate the average magnitude across all runs for each row (optional)
    magnitude_df['Average Magnitude'] = magnitude_df.mean(axis=1)
    
    # Compute the overall average across all rows for each run
    avg_magnitude_run1 = magnitude_df['Run 1 Magnitude'].mean()
    avg_magnitude_run2 = magnitude_df['Run 2 Magnitude'].mean()
    avg_magnitude_run3 = magnitude_df['Run 3 Magnitude'].mean()
    
    #avg_magnitude_all_runs = magnitude_df['Average Magnitude'].mean()

    avg_magnitude_all_runs = (avg_magnitude_run1 + avg_magnitude_run2 + avg_magnitude_run3) / 3

    print(f"Average Acceleration Magnitude (Run 1): {avg_magnitude_run1:.2f} m/s²")
    print(f"Average Acceleration Magnitude (Run 2): {avg_magnitude_run2:.2f} m/s²")
    print(f"Average Acceleration Magnitude (Run 3): {avg_magnitude_run3:.2f} m/s²")
    print(f"Overall Average Acceleration Magnitude: {avg_magnitude_all_runs:.2f} m/s²")

    estimated_mass = 180 #in kilograms
    initial_velocity = 12 #in km/h
    final_velocity = 0 #it should always be 0
    distance_stopping = 160 #measured in feet (20 parking spaces times 8 feet per space)
    calculate_rolling_resistance_coefficient(estimated_mass, initial_velocity, final_velocity, distance_stopping)

    #plot_trial_runs(avg_magnitude_run1, avg_magnitude_run2, avg_magnitude_run3)
    plot_trial_runs(csv_file)




def calculate_rolling_resistance_coefficient(mass_lbs, initial_speed, final_speed, distance_released):
    # Convert mass from pounds to kilograms
    g = 9.8  
    mass_kg = mass_lbs * 0.453592
    distance_m = distance_released * 0.3048
    fspeed = final_speed *  0.2778

    initial_KE = 0.5 * mass_kg * initial_speed ** 2
    final_KE = 0.5 * mass_kg * fspeed ** 2
    F_rolling = (initial_KE - final_KE) / distance_m

    # Calculate the rolling resistance coefficient
    c_rolling = F_rolling / (mass_kg * g)
    print("Extimated Coefficient of Rolling Resistance is: ", c_rolling)
    #Would be more precise and accurate if we had the moment-of-inertia for the wheels, but I can't find data for that



 
def plot_trial_runs(csv_file):
    # Read the CSV file into DataFrame
    df1 = pd.read_csv(csv_file)
    
    # Extract the time and acceleration data for each run
    time = df1['Time (s) Run 1'] 
    
    # Compute the magnitude of acceleration for each run (x, y, z components)
    acc_run1 = np.sqrt(df1['Acceleration - x (m/s²) Run 1']**2 + df1['Acceleration - y (m/s²) Run 1']**2 + df1['Acceleration - z (m/s²) Run 1']**2)
    acc_run2 = np.sqrt(df1['Acceleration - x (m/s²) Run 2']**2 + df1['Acceleration - y (m/s²) Run 2']**2 + df1['Acceleration - z (m/s²) Run 2']**2)
    acc_run3 = np.sqrt(df1['Acceleration - x (m/s²) Run 3']**2 + df1['Acceleration - y (m/s²) Run 3']**2 + df1['Acceleration - z (m/s²) Run 3']**2)

 
    plt.figure(figsize=(10, 6))
    plt.plot(time, acc_run1, label='Run 1', color='b')
    plt.plot(time, acc_run2, label='Run 2', color='g')
    plt.plot(time, acc_run3, label='Run 3', color='r')

    # Labels and title
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.title('Check terminal for numbers')
    plt.legend()

    # Grid and show the plot
    plt.grid(True)
    plt.show()



#MAIN STUFF
csv_file = 'RollingResistanceData.csv' #.csv that I am using rn
compute_average_acceleration(csv_file)


