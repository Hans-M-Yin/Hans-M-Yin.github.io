'use strict';
const root = document.documentElement;
const themeButton = document.querySelector('[data-theme-toggle]');
const systemDark = window.matchMedia('(prefers-color-scheme: dark)');
let savedTheme = null;
try { savedTheme = localStorage.getItem('theme'); } catch (_) {}
const applyTheme = (theme) => {
  root.dataset.theme = theme;
  themeButton?.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  themeButton?.setAttribute('aria-pressed', String(theme === 'dark'));
};
applyTheme(savedTheme || (systemDark.matches ? 'dark' : 'light'));
themeButton?.addEventListener('click', () => {
  savedTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
  applyTheme(savedTheme);
  try { localStorage.setItem('theme', savedTheme); } catch (_) {}
});
systemDark.addEventListener('change', () => { if (!savedTheme) applyTheme(systemDark.matches ? 'dark' : 'light'); });

document.querySelector('[data-menu-toggle]')?.addEventListener('click', (event) => {
  const expanded = document.querySelector('.nav').classList.toggle('is-open');
  event.currentTarget.setAttribute('aria-expanded', String(expanded));
});
document.querySelectorAll('[data-filter]').forEach(button => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    let visible = 0;
    document.querySelectorAll('[data-paper-category]').forEach(paper => {
      paper.hidden = filter !== 'all' && paper.dataset.paperCategory !== filter;
      if (!paper.hidden) visible++;
    });
    document.querySelector('[data-filter-status]').textContent = `${visible} research entries shown`;
  });
});

const dialog = document.querySelector('#search-dialog');
const searchInput = document.querySelector('#site-search');
const resultList = document.querySelector('#search-results');
const searchData = JSON.parse(document.querySelector('#search-index').textContent);
const renderSearch = () => {
  const terms = searchInput.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const results = searchData.filter(item => terms.every(term => `${item.title} ${item.text}`.toLowerCase().includes(term)));
  resultList.replaceChildren();
  results.forEach(item => {
    const li = document.createElement('li');
    const link = document.createElement('a');
    link.href = item.url;
    link.append(document.createTextNode(item.title));
    const type = document.createElement('small');
    type.textContent = item.type;
    link.append(type);
    li.append(link);
    resultList.append(li);
  });
  if (!results.length) {
    const empty = document.createElement('li');
    empty.className = 'search-empty';
    empty.textContent = 'No results. Try “agents”, “FREAK”, or “CV”.';
    resultList.append(empty);
  }
};
const openSearch = () => {
  if (!dialog.open) dialog.showModal();
  renderSearch();
  searchInput.focus();
};
document.querySelector('[data-open-search]')?.addEventListener('click', openSearch);
document.querySelector('[data-close-search]')?.addEventListener('click', () => dialog.close());
searchInput.addEventListener('input', renderSearch);
document.addEventListener('keydown', event => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault();
    openSearch();
  }
});
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
resultList.addEventListener('click', event => {
  const link = event.target.closest('a');
  if (!link) return;
  // A search result may target a paper hidden by the current publication filter.
  document.querySelector('[data-filter="all"]')?.click();
  dialog.close();
});
window.addEventListener('hashchange', () => {
  const target = document.getElementById(location.hash.slice(1));
  if (target?.hidden) {
    document.querySelector('[data-filter="all"]')?.click();
    target.scrollIntoView();
  }
});
