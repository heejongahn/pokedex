require('./pokedex');

const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');

searchForm.addEventListener('submit', (e) => {
  e.preventDefault();
  showSpinner();
  window.location.href = `/${searchInput.value}`;
});

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
