<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <h1>ShareChat Data Processing Pipeline</h1>
  <p>This repository contains a data processing pipeline for scraping, text extraction, translation, sentiment analysis, and sentiment labeling of ShareChat posts. The pipeline is designed to process multilingual posts and generate aggregate sentiment scores for each post.</p>

  <h2>Usage</h2>

  <ol>
    <li>
      <h3>Scraping:</h3>
      <ul>
        <li>Run the <code>main.py</code> script located in the <code>sharechat_scraper</code> directory using the command <code>python3 main.py</code>.</li>
        <li>Modify the <code>constants.py</code> file to include leader tags. Leader tags are identifiers for specific ShareChat users. Add leader tags to the <code>LEADER_TAGS</code> list in <code>constants.py</code>.</li>
      </ul>
    </li>
    <li>
      <h3>Image to Text Conversion:</h3>
      <ul>
        <li>Execute the <code>tesseract.sh</code> script to extract text from images. Use the command <code>./tesseract.sh</code>.</li>
      </ul>
    </li>
    <li>
      <h3>Text Translation:</h3>
      <ul>
        <li>Run the <code>translation.py</code> script using Python 3 to translate multilingual text to English and perform preprocessing on the English text.</li>
        <li>Execute <code>python3 translation.py</code>.</li>
        <li>Preprocessed English texts are saved in <code>translations.pickle</code>.</li>
      </ul>
    </li>
    <li>
      <h3>Sentiment Score Calculation for Each Post:</h3>
      <ul>
        <li>Run the <code>sentiment_analysis.py</code> script to calculate sentiment scores for each post.</li>
        <li>Execute <code>python3 sentiment_analysis.py</code>.</li>
        <li>All sentiment scores for each post are saved in <code>sentiments.pickle</code>.</li>
      </ul>
    </li>
    <li>
      <h3>Aggregate Sentiment Score Calculation and Labeling:</h3>
      <ul>
        <li>Execute the <code>sentiment_labeller.py</code> script to calculate aggregate sentiment scores and label each post.</li>
        <li>Use the command <code>python3 sentiment_labeller.py</code>.</li>
        <li>Labelled results are stored in <code>results.pickle</code>.</li>
      </ul>
    </li>
  </ol>

  <h2>Result Implementation</h2>
  <p> User interface (UI) for visualizing sentiment analysis results for each leader. run index.html in frontend</p>
  <h2>Project Demonstration </h2>
  <p>https://youtu.be/nNgTlCs4e5U</p>
</body>
</html>
