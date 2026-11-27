const defaultLanguage = 'ne';
const page = document.body.dataset.page;
const video = document.querySelector('#promo');
const playToggle = document.querySelector('#play-toggle');
const soundToggle = document.querySelector('#sound-toggle');
const languageButtons = document.querySelectorAll('[data-lang]');
const translatedNodes = document.querySelectorAll('[data-copy]');
const translatedAttributes = document.querySelectorAll('[data-copy-aria]');
const languageLinks = [...document.querySelectorAll('[data-language-link]')]
  .map(link => ({ link, original: link.getAttribute('href') }));
const whatsappLinks = document.querySelectorAll('[data-wa]');
const navigation = document.querySelectorAll('nav [data-route]');
const sections = [...document.querySelectorAll('#home, #about, #contact')];
let language = defaultLanguage;

function syncVideoControls() {
  if (!video) return;
  const copy = COPY[language];
  playToggle.textContent = video.paused ? copy.play : copy.pause;
  soundToggle.textContent = video.muted ? copy.soundOn : copy.soundOff;
  soundToggle.setAttribute('aria-pressed', String(!video.muted));
}

function renderLanguage(nextLanguage, animate = false) {
  language = Object.prototype.hasOwnProperty.call(COPY, nextLanguage) ? nextLanguage : defaultLanguage;
  const copy = COPY[language];
  document.documentElement.lang = language;
  document.title = copy[page === 'home' ? 'homeTitle' : 'privacyTitle'];
  for (const node of translatedNodes) node.textContent = copy[node.dataset.copy];
  for (const node of translatedAttributes) node.setAttribute('aria-label', copy[node.dataset.copyAria]);
  for (const button of languageButtons) {
    button.setAttribute('aria-pressed', String(button.dataset.lang === language));
  }
  for (const link of whatsappLinks) {
    link.href = 'https://wa.me/96875253754?text=' + encodeURIComponent(copy[link.dataset.wa]);
    link.setAttribute('aria-label', link.dataset.wa === 'privacyMessage' && link.classList.contains('floating-wa')
      ? copy.privacyMessage : copy.whatsapp);
  }
  for (const { link, original } of languageLinks) {
    if (original.startsWith('#') || language === defaultLanguage) {
      link.setAttribute('href', original);
    } else {
      const [path, hash] = original.split('#');
      link.setAttribute('href', path + '?lang=' + language + (hash ? '#' + hash : ''));
    }
  }
  syncVideoControls();
  if (animate && document.querySelector('main').animate && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelector('main').animate([{ opacity: 0.78 }, { opacity: 1 }], { duration: 160 });
  }
}

for (const button of languageButtons) {
  button.addEventListener('click', () => {
    const nextLanguage = button.dataset.lang;
    if (nextLanguage === language) return;
    const url = new URL(location.href);
    if (nextLanguage === defaultLanguage) url.searchParams.delete('lang');
    else url.searchParams.set('lang', nextLanguage);
    history.replaceState(null, '', url);
    renderLanguage(nextLanguage, true);
  });
}

if (video) {
  video.controls = false;
  document.querySelector(".video-controls").hidden = false;
  playToggle.addEventListener('click', () => {
    if (video.paused) video.play().catch(syncVideoControls);
    else video.pause();
  });
  soundToggle.addEventListener('click', () => {
    video.muted = !video.muted;
    if (video.paused && !video.muted) video.play().catch(syncVideoControls);
  });
  for (const event of ['play', 'pause', 'volumechange', 'loadedmetadata']) {
    video.addEventListener(event, syncVideoControls);
  }
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    video.autoplay = false;
    video.pause();
  }
}

function updateNavigation() {
  let current = 'privacy';
  if (page === 'home') {
    const contact = sections[sections.length - 1];
    const contactVisible = contact.getBoundingClientRect().top < innerHeight - 120;
    const atEnd = Math.ceil(scrollY + innerHeight) >= document.documentElement.scrollHeight;
    current = 'home';
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= innerHeight * 0.38) current = section.id;
    }
    if (atEnd && contactVisible) current = 'contact';
  }
  for (const link of navigation) {
    if (link.dataset.route === current) link.setAttribute('aria-current', page === 'privacy' ? 'page' : 'location');
    else link.removeAttribute('aria-current');
  }
}

renderLanguage(new URLSearchParams(location.search).get('lang'));
updateNavigation();

let pending = false;
function scheduleNavigationUpdate() {
  if (pending) return;
  pending = true;
  requestAnimationFrame(() => {
    pending = false;
    updateNavigation();
  });
}
if (sections.length) {
  addEventListener('scroll', scheduleNavigationUpdate, { passive: true });
  addEventListener('resize', scheduleNavigationUpdate);
  for (const button of languageButtons) button.addEventListener('click', scheduleNavigationUpdate);
}

if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('arrive');
      observer.unobserve(entry.target);
    }
  }, { threshold: 0.15 });
  document.querySelectorAll('.trust-card, .contact-panel, .policy-section').forEach(node => observer.observe(node));
}
