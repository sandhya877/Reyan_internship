const google = require('googlethis');

const options = {
  page: 0,
  safe: false, // Safe Search
  parse_ads: false, // If set to true, sponsored results will be parsed
  additional_params: {
    hl: 'en',
    gl: 'us',
  },
  num: 20, // Number of results to retrieve (e.g., top 20)
};

async function performGoogleSearch() {
  const response = await google.search('how to unlock ipad without password', options);

  // Extract and print only the URLs
  const urls = response.results.map((result) => result.url);
  urls.forEach((url, index) => console.log(`Result ${index + 1}: ${url}`));
}

performGoogleSearch();

