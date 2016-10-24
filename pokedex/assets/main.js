require('./pokedex');

const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');

searchForm.addEventListener('submit', (e) => {
  e.preventDefault();
  window.location.href = `/${searchInput.value}`;
});

const backToTopBtn = document.getElementById('back-to-top')
backToTopBtn.addEventListener('click', (e) => {
  window.scroll(0, 0);
});
