// Sample data for leaders and languages
const leaders = [
  { name: 'Modi', image: 'modi.png', plots: ['scatter_plot.png', 'line_plot.png', 'bar_plot.png', 'pie_chart.png', 'scatter_plot.png', 'scatter_plot.png'] },
  { name: 'Rahul', image: 'rahul.png', plots: ['scatter_plot.png', 'line_plot.png', 'bar_plot.png', 'pie_chart.png', 'scatter_plot.png', 'scatter_plot.png'] },
  { name: 'Arvind', image: 'arvind.png', plots: ['scatter_plot.png', 'line_plot.png', 'bar_plot.png', 'pie_chart.png', 'scatter_plot.png', 'scatter_plot.png'] }
];

const languages = ['Hindi', 'English', 'Spanish', 'French', 'German'];

// Get the necessary HTML elements
const leaderSelect = document.getElementById('leader-select');
const languageSelect = document.getElementById('language-select');
const leaderImage = document.querySelector('.leader-image');
const visualizationContainer = document.querySelectorAll('.sentiment-plot');

// Populate the dropdown menus
leaders.forEach(leader => {
  const option = document.createElement('option');
  option.value = leader.name;
  option.text = leader.name;
  leaderSelect.add(option);
});

languages.forEach(language => {
  const option = document.createElement('option');
  option.value = language;
  option.text = language;
  languageSelect.add(option);
});

// Event listener for dropdown changes
leaderSelect.addEventListener('change', updateVisualizations);
languageSelect.addEventListener('change', updateVisualizations);

// Function to update the leader's image and visualizations
function updateVisualizations() {
  const selectedLeader = leaders.find(leader => leader.name === leaderSelect.value);
  const selectedLanguage = languageSelect.value;

  // Update the leader's image
  leaderImage.src = selectedLeader.image;

  // Update the visualization plots
  selectedLeader.plots.forEach((plot, index) => {
      document.getElementById(`sentiment-plot-${index + 1}`).src = plot;
  });
}

// Initialize sentiment plots with the first leader's data
window.onload = function() {
  const initialLeader = leaders[0];
  leaderImage.src = initialLeader.image;
  initialLeader.plots.forEach((plot, index) => {
      document.getElementById(`sentiment-plot-${index + 1}`).src = plot;
  });
};