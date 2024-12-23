import pandas as pd

def compute_energy_difference(demand_file, supply_file, output_file):
    # Read the energy demand and supply datasets
    demand_df = pd.read_csv(demand_file, parse_dates=['Datetime'])
    supply_df = pd.read_csv(supply_file, parse_dates=['Datetime'])

    # Merge the two dataframes on the 'Datetime' column
    merged_df = pd.merge(demand_df, supply_df, on='Datetime')

    # Calculate the energy difference
    merged_df['Energy Difference (MJ)'] = merged_df['Energy Supplied (MJ)'] - merged_df['Energy Demand (MJ)']

    # Save the result to a new CSV file
    merged_df[['Datetime', 'Energy Difference (MJ)']].to_csv(output_file, index=False)
    print(f"File saved as {output_file}")


def calculate_energy_stats(difference_file):
    # Read energy difference from the provided CSV file
    df = pd.read_csv(difference_file, parse_dates=["Datetime"])

    # Calculate the summed values
    total_difference = df["Energy Difference (MJ)"].sum()

    # Calculate the sum of only the negative energy differences
    negative_difference_sum = df[df["Energy Difference (MJ)"] < 0]["Energy Difference (MJ)"].sum()
    positive_difference_sum = df[df["Energy Difference (MJ)"] > 0]["Energy Difference (MJ)"].sum()

    # Find the highest and lowest energy differences
    highest_difference = df["Energy Difference (MJ)"].max()
    lowest_difference = df["Energy Difference (MJ)"].min()

    # Print out the results
    print(f"Total Energy Difference: \n{round(total_difference / 1000, 2)} GJ \n{round(total_difference / 3600000, 2)} GWh")
    print(f"\nMax energy supplied (hour): \n{round(highest_difference / 1000, 2)} GJ \n{round(highest_difference / 3600, 2)} MWh")
    print(f"\nMax energy required (hour): \n{round(lowest_difference / 1000, 2)} GJ \n{round(lowest_difference / 3600, 2)} MWh")
    print(f"\nSum of Negative Energy Differences (H₂ resupply req): \n{round(negative_difference_sum / 1000, 2)} GJ \n{round(negative_difference_sum / 3600000, 2)} GWh")
    print(f"\nSum of Positive Energy Differences (H₂ resupply req): \n{round(positive_difference_sum / 1000, 2)} GJ \n{round(positive_difference_sum / 3600000, 2)} GWh")

    print(f"\n\nBattery size req: \n{round(lowest_difference / 1000, 2)*3} GJ \n{round(lowest_difference / 3600, 2)*3} MWh")

if __name__ == "__main__":
    DEMAND_FILE = 'SimulationData/energy_demand_3200_houses.csv'
    SUPPLY_FILE = 'SimulationData/hourly_solar_energy_production.csv'
    OUTPUT_FILE = 'SimulationData/energy_difference.csv'
    DIFFERENCE_FILE = 'SimulationData/energy_difference.csv'

    # compute_energy_difference(DEMAND_FILE, SUPPLY_FILE, OUTPUT_FILE)
    calculate_energy_stats(DIFFERENCE_FILE)
