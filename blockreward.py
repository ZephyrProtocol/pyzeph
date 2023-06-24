def calculate_zephyr_block_reward(block_height):
    M = 2**64
    emission_speed_factor = 20
    tail_emission = 0.6 * 10**12
    treasury_fund = 500000 * 10**12  # 500,000 coins in atomic units

    circulation = treasury_fund

    for h in range(1, block_height + 1):
        block_reward = (M - circulation) * 2**(-emission_speed_factor) * 10**-12
        block_reward = max(block_reward, tail_emission / 10**12)
        circulation += block_reward * 10**12

    return block_reward

# Usage
block_height = 4628000
reward = calculate_zephyr_block_reward(block_height)
print(f"The block reward for block {block_height} is {reward} ZEPH")

def calculate_zephyr_block_reward_for_range(starting_block_height, number_of_blocks):
    M = 2**64
    emission_speed_factor = 20
    tail_emission = 0.6 * 10**12
    treasury_fund = 500000 * 10**12  # 500,000 coins in atomic units

    circulation = treasury_fund
    total_reward = 0

    tail_emission_enabled = False

    for h in range(1, starting_block_height + number_of_blocks):
        block_reward = (M - circulation) * 2**(-emission_speed_factor) * 10**-12
        block_reward = max(block_reward, tail_emission / 10**12)

        if not tail_emission_enabled and block_reward == tail_emission / 10**12:
            tail_emission_enabled = True
            print(f"Tail emission enabled at block {h}")

        circulation += block_reward * 10**12
        if h >= starting_block_height:
            total_reward += block_reward

    return total_reward


def calc_number_of_blocks(period, unit):
    blocks_per_day = 720  # Number of blocks per day
    days_per_month = 30  # Approximate number of days per month
    days_per_year = 365  # Number of days per year

    if unit == "d":  # Days
        return period * blocks_per_day
    elif unit == "w":  # Weeks
        return period * 7 * blocks_per_day
    elif unit == "m":  # Months
        return period * days_per_month * blocks_per_day
    elif unit == "y":  # Years
        return period * days_per_year * blocks_per_day
    else:
        raise ValueError("Invalid time period unit. Use 'd' for days, 'm' for months, or 'y' for years.")

# Usage
period = 1
unit = "m"
num_blocks = calc_number_of_blocks(period, unit)
print(f"The number of blocks for a period of {period} {unit} is {num_blocks}.")


# Usage
starting_block_height = 1  # Replace with your starting block number
number_of_blocks = 17468  # Replace with the number of blocks you want to calculate the reward for
total_reward = calculate_zephyr_block_reward_for_range(starting_block_height, number_of_blocks)
print(f"The total block reward for blocks {starting_block_height} to {starting_block_height + number_of_blocks - 1} is {total_reward} ZEPH")

print(f"the treasury_fund must be:", 796494.580 - total_reward)

total = 18400000
treasury_fund = 500000

# num_blocks = calc_number_of_blocks(1, "m")
# emmision_1_month = calculate_zephyr_block_reward_for_range(1, num_blocks) + treasury_fund
# print(f"1 Month:", emmision_1_month, f"({round(emmision_1_month/total*100,2)}%)")

# num_blocks = calc_number_of_blocks(6, "m")
# emmision_6_month = calculate_zephyr_block_reward_for_range(1, num_blocks) + treasury_fund
# print(f"6 Months:", emmision_6_month, f"({round(emmision_6_month/total*100,2)}%)")

# num_blocks = calc_number_of_blocks(1, "y")
# print(num_blocks)
# emmision_1_year = calculate_zephyr_block_reward_for_range(1, num_blocks) + treasury_fund
# print(f"1 Year:", emmision_1_year, f"({round(emmision_1_year/total*100,2)}%)")

# num_blocks = calc_number_of_blocks(2, "y")
# emmision_2_year = calculate_zephyr_block_reward_for_range(1, num_blocks) + treasury_fund
# print(f"2 Years:", emmision_2_year, f"({round(emmision_2_year/total*100,2)}%)")

# num_blocks = calc_number_of_blocks(5, "y")
# emmision_5_year = calculate_zephyr_block_reward_for_range(1, num_blocks) + treasury_fund
# print(f"5 Years:", emmision_5_year, f"({round(emmision_5_year/total*100,2)}%)")

# num_blocks = calc_number_of_blocks(14, "y")
# emmision_10_year = calculate_zephyr_block_reward_for_range(1, num_blocks) + treasury_fund
# print(f"10 Years:", emmision_10_year, f"({round(emmision_10_year/total*100,2)}%)")

import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import numpy as np

tail_emission_start = 13.369 # years or block 3513570
results = []
results.append(treasury_fund)
total_years = 20
previous_emission = treasury_fund  # Start with the initial treasury fund
blocks_per_year = calc_number_of_blocks(1, "y")

# for i in range(1, total_years + 1):
#     emission = calculate_zephyr_block_reward_for_range((i - 1) * blocks_per_year + 1, blocks_per_year)
#     previous_emission += emission
#     results.append(previous_emission)

# print(results)
results = [500000, 4478548.787501788, 7575107.483122898, 9985201.280526588, 11861010.100329667, 13320977.646921225, 14457290.268227883, 15341697.854105568, 16030044.32081877, 16565793.748800272, 16982774.82368396, 17307316.872130465, 17559912.367595684, 17756510.8812081, 17916977.59693679, 18074657.59693757, 18232337.596938353, 18390017.596939135, 18547697.596939918, 18705377.5969407, 18863057.596941482]

import numpy as np

# Define the maximum supply before tail emission
M = 2**64 / 10**12

# Create a matplotlib line plot
plt.figure(figsize=(10, 6))

# Calculate percent emission for each year
percent_emission = [(r/M)*100 for r in results]

# Generate x values
x = np.array(range(0, total_years + 1))

# Fit polynomial of degree 2 (quadratic) for pre-tail emission
pre_tail_emission = percent_emission[:int(tail_emission_start) + 1]
pre_fit = np.polyfit(range(int(tail_emission_start) + 1), pre_tail_emission, 4)
pre_func = np.poly1d(pre_fit)

# Fit line for after tail emission
after_tail_emission = percent_emission[int(tail_emission_start):]
after_fit = np.polyfit(range(int(tail_emission_start), total_years + 1), after_tail_emission, 1)
after_func = np.poly1d(after_fit)

# Plot the curve and line with light grey color and 50% transparency
plt.plot(range(int(tail_emission_start) + 1), pre_func(range(int(tail_emission_start) + 1)), label='Curved Emission', color='darkblue', alpha=0.5)

# Plot the original data as a scatter plot
plt.scatter(x, percent_emission, color='red', label='Data')

# Label each point with its y value
for i, txt in enumerate(percent_emission):
    if i > 0:
        plt.text(x[i] + 0.2, percent_emission[i] - 1, f'{txt:.1f}%', fontsize=8, horizontalalignment='left')
    else:
        plt.text(x[i] + 0.2, percent_emission[i] - 1, f'{txt:.1f}% (Treasury Fund)', fontsize=8, horizontalalignment='left')

plt.title('Cumulative Zephyr Emission over 20 Years')
plt.xlabel('Year')
plt.ylabel('Cumulative Emission (%) of Maximum supply before Tail Emission')
plt.ylim(0, 105)  # Make the graph intersect the y-axis at 0

# Adjust x-axis to show each year
plt.xticks(range(0, total_years + 1))

# Adjust y-axis to start from 0
plt.margins(x=0)

# Add vertical line
plt.axvline(tail_emission_start, color='orange', linestyle='--')
plt.text(tail_emission_start + 0.1, 50, 'Tail emission starts', color='orange')  # Adjusted the y-coordinate

# Plot line of best fit
plt.plot(range(int(tail_emission_start), total_years + 1), after_func(range(int(tail_emission_start), total_years + 1)), '--', color='red', label='Post-Tail Emission Fit')

# Add a legend
plt.legend()

# Show the plot
plt.show()


