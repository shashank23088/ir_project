// Sample data for leaders and languages
const leaders = [
  {
    name: 'Narendra Modi',
    image: 'modi.png',
    description: 'Prime Minister of India',
    plots: ['hmodi1.png', 'hmodi2.png', 'hmodi3.png', 'hmodi4.png']
  },
  {
    name: 'Rahul Gandhi',
    image: 'rahul.png',
    description: 'Leader of the Indian National Congress',
    plots: ['hrahul1.png', 'hrahul2.png', 'hrahul3.png', 'hrahul4.png']
  },
  {
    name: 'Arvind Kejriwal',
    image: 'arvind.png',
    description: 'Chief Minister of Delhi',
    plots: ['harvind1.png', 'harvind2.png', 'harvind3.png','harvind4.png']
  },
   {
    name: 'Asaduddin Owaisi',
    image: 'owaisi.png',
    description: 'President of All IMIM',
    plots: ['howaisi1.png', 'howaisi2.png', 'howaisi3.png','howaisi4.png']
  },
   {
    name: 'Akhilesh Yadav',
    image: 'akhilesh.png',
    description: 'Former CM of Uttar Pradesh',
    plots: ['hakhilesh1.png', 'hakhilesh2.png', 'hakhilesh3.png','hakhilesh4.png']
  }
];

const languages = ['Hindi', 'Bengali','Punjabi'];

// Get the necessary HTML elements
const leaderSelect = document.getElementById('leader-select');
const languageSelect = document.getElementById('language-select');
const leaderImage = document.querySelector('.leader-image');
const leaderDescription = document.querySelector('.leader-description');
const visualizationContainer = document.querySelectorAll('.sentiment-plot');
const tooltips = document.querySelectorAll('.tooltip');

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

// Function to update the leader's image, description, and visualizations
function updateVisualizations() {
  const selectedLeader = leaders.find(leader => leader.name === leaderSelect.value);
  const selectedLanguage = languageSelect.value;

  // Update the leader's image
  leaderImage.src = selectedLeader.image;

  // Update the leader's description
  leaderDescription.textContent = selectedLeader.description;

  // Update the visualization plots based on the language and leader
  if (selectedLanguage === 'Bengali' && selectedLeader.name === 'Narendra Modi') {
    // Update the visualization plots for Modi in Spanish
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = `bmodi${i + 1}.png`;
    }
  } 
 
  else if (selectedLanguage === 'Bengali' && selectedLeader.name === 'Rahul Gandhi') {
    // Update the visualization plots for Rahul in Spanish
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = `brahul${i + 1}.png`;
    }
  } 

  
  else if (selectedLanguage === 'Bengali' && selectedLeader.name === 'Arvind Kejriwal') {
    // Update the visualization plots for Rahul in Spanish
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = `barvind${i + 1}.png`;
    }
  } 
   else if (selectedLanguage === 'Bengali' && selectedLeader.name === 'Asaduddin Owaisi') {
    // Update the visualization plots for Rahul in Spanish
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = `bowaisi${i + 1}.png`;
    }
  } 
   else if (selectedLanguage === 'Bengali' && selectedLeader.name === 'Akhilesh Yadav') {
    // Update the visualization plots for Rahul in Spanish
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = `bakhilesh${i + 1}.png`;
    }
  } 
  else if (selectedLanguage === 'Punjabi' && selectedLeader.name === 'Narendra Modi') {
    // Update the visualization plots for Modi in Spanish
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = `pmodi${i + 1}.png`;
    }
  } 
 
  else if (selectedLanguage === 'Punjabi' && selectedLeader.name === 'Rahul Gandhi') {
    // Update the visualization plots for Rahul in Spanish
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = `prahul${i + 1}.png`;
    }
  } 

  
  else if (selectedLanguage === 'Punjabi' && selectedLeader.name === 'Arvind Kejriwal') {
    // Update the visualization plots for Rahul in Spanish
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = `parvind${i + 1}.png`;
    }
  } 
   else if (selectedLanguage === 'Punjabi' && selectedLeader.name === 'Asaduddin Owaisi') {
    // Update the visualization plots for Rahul in Spanish
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = `powaisi${i + 1}.png`;
    }
  } 
   else if (selectedLanguage === 'Punjabi' && selectedLeader.name === 'Akhilesh Yadav') {
    // Update the visualization plots for Rahul in Spanish
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = `pakhilesh${i + 1}.png`;
    }
  } 

  else {
    // Update the visualization plots based on the leader's default plots
    selectedLeader.plots.forEach((plot, index) => {
      visualizationContainer[index].src = plot;
    });
  }
}



// Initialize sentiment plots with the first leader's data
window.onload = function() {
  const initialLeader = leaders[0];
  leaderImage.src = initialLeader.image;
  leaderDescription.textContent = initialLeader.description;
  initialLeader.plots.forEach((plot, index) => {
    visualizationContainer[index].src = plot;
  });
};

// Tooltip functionality
tooltips.forEach((tooltip, index) => {
  const plot = visualizationContainer[index];
  const tooltipText = tooltip.getAttribute('data-text');

  plot.addEventListener('mouseenter', () => {
    tooltip.textContent = tooltipText;
    tooltip.style.visibility = 'visible';
    tooltip.style.opacity = '1';
  });

  plot.addEventListener('mouseleave', () => {
    tooltip.style.visibility = 'hidden';
    tooltip.style.opacity = '0';
  });
});
