// Sample data for leaders and languages
const leaders = [
  {
    name: 'Narendra Modi',
    image: 'modi.png',
    description: 'Prime Minister of India',
    plots: ['nmodi1.png', 'nmodi2.png', 'nmodi3.png', 'nmodi4.png']
  },
  {
    name: 'Rahul Gandhi',
    image: 'rahul.png',
    description: 'Leader of the Indian National Congress',
    plots: ['crahul1.png', 'crahul2.png', 'crahul3.png', 'crahul4.png']
  },
  {
    name: 'Arvind Kejriwal',
    image: 'arvind.png',
    description: 'Chief Minister of Delhi',
    plots: ['aarvind1.png', 'aarvind2.png', 'aarvind3.png','aarvind4.png']
  }
];

const languages = ['Hindi', 'Telgu','Punjabi', 'Bengali','Gujrati'];

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
  if (selectedLanguage === 'Telgu' && selectedLeader.name === 'Narendra Modi') {
    // Update the visualization plots for Modi in Telgu
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = tmodi${i + 1}.png;
    }
  } 
 
  else if (selectedLanguage === 'Telgu' && selectedLeader.name === 'Rahul Gandhi') {
        // Update the visualization plots for Rahul in Telgu
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = trahul${i + 1}.png;
    }
  } 

  
  else if (selectedLanguage === 'Telgu' && selectedLeader.name === 'Arvind Kejriwal') {
    // Update the visualization plots for Arvind in Telgu
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = tarvind${i + 1}.png;
    }
  } 


  else if (selectedLanguage === 'Punjabi' && selectedLeader.name === 'Narendra Modi') {
       // Update the visualization plots for Modi in Punjabi
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = pmodi${i + 1}.png;
    }
  } 

  else if (selectedLanguage === 'Punjabi' && selectedLeader.name === 'Rahul Gandhi') {
       // Update the visualization plots for Rahul in Punjabi
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = prahul${i + 1}.png;
    }
  } 

  else if (selectedLanguage === 'Punjabi' && selectedLeader.name === 'Arvind Kejriwal') {
       // Update the visualization plots for Arvind in Punjabi
    for (let i = 0; i < selectedLeader.plots.length; i++) {
      visualizationContainer[i].src = parvind${i + 1}.png;
    }
  } 

  else if (selectedLanguage === 'Bengali' && selectedLeader.name === 'Narendra Modi') {
    // Update the visualization plots for Modi in Bengali
 for (let i = 0; i < selectedLeader.plots.length; i++) {
   visualizationContainer[i].src = bmodi${i + 1}.png;
 }
} 

else if (selectedLanguage === 'Bengali' && selectedLeader.name === 'Rahul Gandhi') {
    // Update the visualization plots for Rahul in Bengali
 for (let i = 0; i < selectedLeader.plots.length; i++) {
   visualizationContainer[i].src = brahul${i + 1}.png;
 }
} 

else if (selectedLanguage === 'Bengali' && selectedLeader.name === 'Arvind Kejriwal') {
    // Update the visualization plots for Arvind in Bengali
 for (let i = 0; i < selectedLeader.plots.length; i++) {
   visualizationContainer[i].src = barvind${i + 1}.png;
 }
} 

else if (selectedLanguage === 'Gujrati' && selectedLeader.name === 'Narendra Modi') {
  // Update the visualization plots for Modi in Gujrati
for (let i = 0; i < selectedLeader.plots.length; i++) {
 visualizationContainer[i].src = gmodi${i + 1}.png;
}
} 

else if (selectedLanguage === 'Gujrati' && selectedLeader.name === 'Rahul Gandhi') {
  // Update the visualization plots for Rahul in Gujrati
for (let i = 0; i < selectedLeader.plots.length; i++) {
 visualizationContainer[i].src = grahul${i + 1}.png;
}
} 

else if (selectedLanguage === 'Gujrati' && selectedLeader.name === 'Arvind Kejriwal') {
  // Update the visualization plots for Arvind in Gujrati
for (let i = 0; i < selectedLeader.plots.length; i++) {
 visualizationContainer[i].src = garvind${i + 1}.png;
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
