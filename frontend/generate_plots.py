import matplotlib.pyplot as plt
import numpy as np

# Set the random seed for reproducibility
np.random.seed(0)

# Generate random data for the plots
x = np.arange(10)
y = np.random.rand(10)

# Create a line plot
plt.figure()
plt.plot(x, y, marker='o')
plt.title('Line Plot')
plt.savefig('line_plot.png')  # Save the figure
plt.close()  # Close the plot to free up memory

# Create a bar plot
plt.figure()
plt.bar(x, y, color='orange')
plt.title('Bar Plot')
plt.savefig('bar_plot.png')  # Save the figure
plt.close()  # Close the plot to free up memory

# Create a scatter plot
plt.figure()
plt.scatter(x, y, color='green')
plt.title('Scatter Plot')
plt.savefig('scatter_plot.png')  # Save the figure
plt.close()  # Close the plot to free up memory

# Create a pie chart
plt.figure()
plt.pie(y, labels=x, autopct='%1.1f%%', startangle=140)
plt.title('Pie Chart')
plt.savefig('pie_chart.png')  # Save the figure
plt.close()  # Close the plot to free up memory
