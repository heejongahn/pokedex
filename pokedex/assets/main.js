require('./pokedex');
import 'whatwg-fetch';

// Show spinner, then redirect when form submitted
const showSpinner = () => {
  const spinner = document.getElementsByClassName('spinner')[0]
  if (spinner) {
    spinner.style.display = 'block';
  }
}
const searchForm = document.getElementById('search-form');
searchForm.addEventListener('submit', (e) => {
  e.preventDefault();
  showSpinner();
  window.location.href = `/${searchInput.value}`;
});

// Make all link clicks show spinner too
const addShowSpinner = (elem, event) => {
  elem.addEventListener(event, () => {
    showSpinner();
  });
}

[...document.querySelectorAll('a')].map(link => {
  addShowSpinner(link, 'click');
});

// Back to top functionality
const backToTopBtn = document.getElementById('back-to-top')
backToTopBtn.addEventListener('click', (e) => {
  window.scroll(0, 0);
});

// Make sure back to top button is used only when vertical scroll is available
const hasVScroll = document.body.scrollHeight > window.innerHeight;
if (!hasVScroll) {
  backToTopBtn.style.display = 'none';
}

// Search recommendation, using fetch
const searchInput = document.getElementById('search-input');
const searchRecommendation = document.getElementById('search-recommendation');
fetch('/name_map').
  then(result => result.json()).
  then(result => {
    const names = result.name_map;

    // Update search recommendation
    searchInput.addEventListener('input', (e) => {
      const candidates = names.filter(name =>
          (e.target.value !== '' &&
            name.toLowerCase().includes(e.target.value.toLowerCase()))
      ).slice(0, 10);

      // Clear previously appended children
      searchRecommendation.innerText = '';

      if (candidates) {
        candidates.map(candidate => {
          const link = document.createElement('a');
          searchRecommendation.appendChild(link);
          link.href = `/${candidate}`;
          link.innerText = candidate;
          addShowSpinner(link, 'click'); // Don't forget the spinner
        });
      }
    });
  });
