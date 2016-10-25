require('./pokedex');
import 'whatwg-fetch';

const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');


const addSpinner = (elem, event) => {
  elem.addEventListener(event, () => {
    showSpinner();
  });
}

searchForm.addEventListener('submit', (e) => {
  e.preventDefault();
  showSpinner();
  window.location.href = `/${searchInput.value}`;
});

const links = document.querySelectorAll('a');
for (const link of links) {
  addSpinner(link, 'click');
}

const backToTopBtn = document.getElementById('back-to-top')
backToTopBtn.addEventListener('click', (e) => {
  window.scroll(0, 0);
});

// Make sure back to top button is used only when vertical scroll is available
const hasVScroll = document.body.scrollHeight > window.innerHeight;
if (!hasVScroll) {
  backToTopBtn.style.display = 'none';
}

const showSpinner = () => {
  const spinner = document.getElementsByClassName('spinner')[0]
  if (spinner) {
    spinner.style.display = 'block';
  }
}

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

      searchRecommendation.innerText = '';

      if (candidates) {
        searchRecommendation.style.display = 'block';
        candidates.map(candidate => {
          const link = document.createElement('a');
          searchRecommendation.appendChild(link);
          link.href = `/${candidate}`;
          link.innerText = candidate;
          addSpinner(link, 'click');
        });
      }
    });

    // Hide it when focus is out
    searchForm.addEventListener('blur', (e) => {
      searchRecommendation.innerText = '';
      searchRecommendation.style.display = 'none';
    });
  });
