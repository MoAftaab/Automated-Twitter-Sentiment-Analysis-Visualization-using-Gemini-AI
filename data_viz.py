import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Read the data
df = pd.read_csv('data_analysis.csv')

# Convert date string to datetime
df['date'] = pd.to_datetime(df['date'])

# Create month-year column for grouping
df['month_year'] = df['date'].dt.to_period('M')

# Calculate average score per month
monthly_averages = df.groupby('month_year')['score'].mean()

# Define sentiment categories with original 5-point scale
sentiment_categories = {
    1: 'Very Negative',
    2: 'Negative',
    3: 'Neutral',
    4: 'Positive',
    5: 'Very Positive'
}

# Convert scores to sentiment categories
def get_sentiment_category(score):
    if pd.isna(score):
        return 'Neutral'
    score = float(score)
    return sentiment_categories.get(int(score), 'Neutral')

df['sentiment'] = df['score'].apply(get_sentiment_category)

# Define category orders
# For legend - from most positive to most negative
legend_order = ['Very Positive', 'Positive', 'Neutral', 'Negative', 'Very Negative']
# For stacking - from most negative to most positive (will appear from bottom to top)
stack_order = ['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']

# Calculate percentage of each sentiment per month
monthly_sentiments = pd.crosstab(
    df['month_year'], 
    df['sentiment'], 
    normalize='index'
) * 100

# Reorder columns for stacking (this affects the bar order)
monthly_sentiments = monthly_sentiments.reindex(columns=stack_order)

# Set up the plot style
plt.style.use('bmh')  # Using a built-in style that's similar to seaborn
fig, ax1 = plt.subplots(figsize=(10, 7))  # Reduced figure width to bring bars closer

# Define colors for 5 categories (matching the example)
# Colors ordered to match legend order (very positive to very negative)
color_dict = {
    'Very Positive': '#186099',  # Dark Blue
    'Positive': '#789bbf',      # Blue
    'Neutral': '#CCCCCC',       # Grey
    'Negative': '#FFE5B4',      # Light Yellow
    'Very Negative': '#e6b553'  # Yellow
}

# Get colors in stacking order
colors = [color_dict[cat] for cat in stack_order]

# Create stacked bar chart
bars = monthly_sentiments.plot(
    kind='bar',
    stacked=True,
    color=colors,
    width=0.6,
    ax=ax1
)

# Create secondary y-axis for average score
ax2 = ax1.twinx()

# Plot average score line with markers and labels
x_positions = range(len(monthly_averages))
line = ax2.plot(x_positions, monthly_averages.values, 
         color='black', linewidth=2, label='Average Score',
         marker='o', markersize=8)[0]  # Get the line handle

# Add value labels above each point
for x, y in zip(x_positions, monthly_averages.values):
    ax2.annotate(f'{y:.2f}', 
                 xy=(x, y), 
                 xytext=(0, 10),
                 textcoords='offset points',
                 ha='center',
                 va='bottom',
                 fontsize=10)

# Set y-axis limits and labels
ax1.set_ylim(0, 100)
ax2.set_ylim(1, 5)
ax2.set_ylabel('Average Sentiment Score', fontsize=12)

# Customize the plot
ax1.set_title('Food Price Sentiment Analysis Over Time (5-Point Scale)', pad=20, fontsize=14)
ax1.set_xlabel('Time Period', fontsize=12)
ax1.set_ylabel('Percentage of Tweets', fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Create custom legend with desired order
legend_handles = [plt.Rectangle((0,0),1,1, facecolor=color_dict[label]) for label in legend_order]
legend_handles.append(line)  # Add the average score line
legend_labels = legend_order + ['Average Score']

ax1.legend(legend_handles, legend_labels,
          title='Sentiment Level', bbox_to_anchor=(1.15, 1), loc='upper left')

# Remove all gridlines
ax1.grid(False)
ax2.grid(False)

# Set background color to white for better contrast
ax1.set_facecolor('white')
fig.patch.set_facecolor('white')

# Adjust margins to reduce spacing between bars
plt.margins(x=0.01)  # Reduce horizontal margins

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the plot
plt.savefig('sentiment_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Visualization saved as sentiment_analysis.png") 