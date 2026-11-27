const languages = new Set(['ne', 'en', 'ta', 'si', 'hi']);
const storageKey = 'gulfpath-language';

function readLanguage() {
  try {
    return localStorage.getItem(storageKey);
  } catch {
    return null;
  }
}

document.addEventListener('click', event => {
  const link = event.target.closest('[data-language]');
  if (!link) return;
  try {
    localStorage.setItem(storageKey, link.hreflang);
  } catch {
    // Each language link works without storage.
  }
});

const alias = document.body.dataset.alias;
if (alias) {
  const current = new URL(location.href);
  const requested = current.searchParams.get('lang');
  const language = requested ?? readLanguage();
  if (languages.has(language) && (language !== 'ne' || requested === 'ne')) {
    const page = alias === 'privacy' ? 'privacy/' : '';
    const next = new URL('/' + language + '/' + page, current);
    current.searchParams.delete('lang');
    next.search = current.search;
    next.hash = current.hash;
    location.replace(next);
  }
}

if ('IntersectionObserver' in window &&
    !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('arrive');
      observer.unobserve(entry.target);
    }
  }, { threshold: 0.3 });
  for (const step of document.querySelectorAll('.timeline li')) observer.observe(step);
}

const errorRouteLanguage = location.pathname.split('/')[1];
const errorLanguage = languages.has(errorRouteLanguage) ? errorRouteLanguage : readLanguage();
const errorTemplate = document.getElementById('error-' + errorLanguage);
if (errorTemplate) {
  document.documentElement.lang = errorLanguage;
  document.title = errorTemplate.dataset.title;
  document.body.replaceChildren(errorTemplate.content.cloneNode(true));
}
