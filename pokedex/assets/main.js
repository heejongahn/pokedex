require('./pokedex');

const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');

searchForm.addEventListener('submit', (e) => {
  e.preventDefault();
  window.location.href = `/${searchInput.value}`;
});
