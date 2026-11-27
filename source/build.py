"""Render the checked-in static website. Run from any directory with Python 3."""
from datetime import date
from html import escape as h
import json
from pathlib import Path
from urllib.parse import quote
import xml.etree.ElementTree as ET

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parent
CONFIG = json.loads((SOURCE / 'settings.json').read_text())
ORIGIN = CONFIG['website']
PHONE = CONFIG['phone']
BRAND = 'GulfPath Overseas'
TAGLINE = 'Your Pathway to Gulf Careers'
LANG = {'en': 'English', 'ne': 'नेपाली', 'ta': 'தமிழ்', 'si': 'සිංහල', 'hi': 'हिन्दी'}
LOCALE = dict(en='en_US', ne='ne_NP', ta='ta_LK', si='si_LK', hi='hi_IN')
COPY = json.loads((SOURCE / 'base.json').read_text())
for row in (SOURCE / 'copy.txt').read_text().splitlines():
    key, *values = row.split('|')
    for language, value in zip(LANG, values, strict=True):
        COPY[language][key] = value

ICON = (SOURCE / 'whatsapp.svg').read_text().strip()
PAGES = {'': 'home', 'about': 'about', 'jobs': 'jobs', 'privacy': 'privacy'}
FLAGS = ('🇴🇲', '🇦🇪', '🇸🇦', '🇶🇦', '🇰🇼', '🇧🇭')
AGENCY_LINKS = (
    ('Sri Lanka · SLBFE', 'https://applications.slbfe.lk/feb/la/la_main.asp?LID=1'),
    ('Nepal · Department of Foreign Employment', 'https://foreignjob.dofe.gov.np/'),
)
REPORT_LINKS = (
    ('Sri Lanka · SLBFE', 'https://www.slbfe.lk/complaint-management/'),
    ('Nepal · Department of Foreign Employment (complaint@dofe.gov.np)', 'mailto:complaint@dofe.gov.np'),
)


def route(lang, page=''):
    return f'/{lang}/' + (f'{page}/' if page else '')


def anchor(url, label, attrs=''):
    return f'<a href="{h(url, quote=True)}"{attrs}>{h(label)}</a>'


def section(ident, title, body):
    return (f'<section class="wrap section-space" id="{ident}" aria-labelledby="{ident}-title">'
            f'<h2 id="{ident}-title">{h(title)}</h2>{body}</section>')


def paragraph(value):
    return f'<p>{h(value)}</p>'


def official_links(links):
    attrs = ' lang="en"'
    return '<ul>' + ''.join(f'<li>{anchor(url, name, attrs)}</li>' for name, url in links) + '</ul>'


class Page:
    def __init__(self, lang, kind):
        self.lang = lang
        self.kind = kind
        self.t = COPY[lang]
        self.home = route(lang)
        self.privacy = route(lang, 'privacy')

    def wa(self, topic, label=None, css='cta'):
        text = f'{self.t["draft"]} {topic}.'
        number = ''.join(char for char in PHONE if char.isascii() and char.isdigit())
        url = 'https://wa.me/' + number + '?text=' + quote(text, safe='')
        label = label or self.t['whatsapp']
        return (f'<a class="{css}" href="{url}" aria-label="{h(label, quote=True)}">'
                f'{ICON}<span>{h(label)}</span></a>')

    def languages(self, footer=False):
        page = self.kind if self.kind in PAGES else ''
        links = []
        for language, name in LANG.items():
            attrs = f' lang="{language}" hreflang="{language}"'
            attrs += ' data-language'
            if language == self.lang and self.kind != '404':
                attrs += ' aria-current="page"'
            links.append(anchor(route(language, page), name, attrs))
        label = f'{self.t["choose"]} · {BRAND}' if footer else self.t['choose']
        return f'<nav class="languages" aria-label="{h(label)}">{"".join(links)}</nav>'

    def nav(self, css):
        links = [(self.home, 'home', ''), (route(self.lang, 'jobs'), 'jobs', 'jobs'),
                 (route(self.lang, 'about'), 'aboutNav', 'about'), (self.home + '#contact', 'contactNav', None)]
        label = BRAND if css == 'desktop-nav' else self.t['contactNav'] + ' · ' + BRAND
        return f'<nav class="{css}" aria-label="{h(label)}">' + ''.join(
            anchor(path, self.t[key], ' aria-current="page"' if page == self.kind else '')
            for path, key, page in links) + '</nav>'

    def footer(self):
        t = self.t
        links = [(route(self.lang, 'about'), 'about'), (self.home + '#process', 'process'),
                 (route(self.lang, 'jobs'), 'jobs'), (route(self.lang, 'about') + '#fraud', 'fraud'),
                 (self.home + '#faq', 'faq'), (self.privacy, 'privacy'), (self.home + '#contact', 'contact')]
        menu = ''.join(f'<li>{anchor(path, t[key])}</li>' for path, key in links)
        return f'''<footer class="site-footer"><div class="wrap">
          <div class="footer-row">{self.brand()}<ul class="footer-links">{menu}</ul></div>
          {paragraph(t['footer'])}
          {self.wa(t['general'])}
          {self.languages(True)}
          <small lang="en">© {CONFIG['privacy_updated'][:4]} {BRAND}</small>
        </div></footer>'''

    def brand(self):
        return (f'<a class="brand" href="{self.home}" lang="en">'
                '<img src="/logo.webp" alt="" width="52" height="52" decoding="async">'
                f'<span><strong>{BRAND}</strong><small>{TAGLINE}</small></span></a>')

    def heading(self, key, description):
        return (f'<div class="page-heading"><div class="wrap"><h1>{h(self.t[key])}</h1>'
                f'<p class="intro">{h(self.t[description])}</p></div></div>')

    def process(self):
        t = self.t
        steps = ''.join(f'<li><span>{h(step)}</span></li>' for step in t['steps'].split(';'))
        return section('process', t['process'], paragraph(t['vary']) + f'<ol class="timeline">{steps}</ol>'
                       + self.wa(t['process'], t['process'] + ' · WhatsApp'))

    def countries(self):
        t = self.t
        cards = []
        for flag, country in zip(FLAGS, t['destinationNames'].split(';'), strict=True):
            extra = paragraph(t['subtitle']) if flag == '🇴🇲' else ''
            cards.append(f'<details name="destination"><summary><span aria-hidden="true">{flag}</span> '
                         f'{h(country)}</summary><div>{extra}{paragraph(t["destinationInfo"])}'
                         f'{self.wa(country, country + " · WhatsApp")}</div></details>')
        return section('destinations', t['countries'], '<div class="country-grid">' + ''.join(cards) + '</div>')

    def faq(self):
        t = self.t
        pairs = [('jobs', 'empty'), ('eligibility', 'eligText'), ('apply', 'applyText'),
                 ('fees', 'fraudText'), ('salary', 'salaryText'), ('visa', 'vary'),
                 ('documents', 'docsText'), ('agency', 'verify'), ('contract', 'conditionsCopy'),
                 ('privacy', 'policyBody4'), ('whatsapp', 'applyText'), ('fraud', 'fraudText')]
        cards = ''.join(f'<details><summary>{h(t[q])}</summary><div>{paragraph(t[a])}</div></details>'
                        for q, a in pairs)
        return section('faq', t['faq'], f'<div class="accordion">{cards}</div>')

    def contact(self):
        t = self.t
        hours = CONFIG['hours'].get(self.lang, {})
        schedule = paragraph(hours.get('schedule', t['hours']))
        for detail in ('timezone', 'response', 'out_of_hours'):
            if detail in hours:
                schedule += paragraph(hours[detail])
        links = ''.join(self.wa(t[key], t[key]) for key in ('employment', 'general', 'privacyMessage'))
        return section('contact', t['contact'], f'''<div class="contact-panel">
          <div><strong lang="en">{BRAND}</strong><p dir="ltr">{h(PHONE)}</p>
          <p>{anchor(ORIGIN, ORIGIN.removeprefix("https://"))}</p>{schedule}</div>
          <div class="actions">{links}{anchor(self.privacy, t['privacy'])}</div></div>''')

    def home_content(self):
        t = self.t
        return f'''<section class="hero" id="home"><div class="wrap hero-grid">
          <div><p class="eyebrow">{h(t['eyebrow'])}</p><h1>{h(t['hero'])}</h1>
          <p class="intro">{h(t['lead'])}</p><div class="actions">{self.wa(t['employment'])}
          {anchor('#process', t['process'], ' class="cta secondary"')}</div>
          <p class="hero-disclosure">{h(t['footer'])} {anchor(self.privacy, t['privacy'])}</p></div>
          <figure class="hero-media"><figcaption id="video-caption">{h(t['videoNote'])}</figcaption>
          <div class="video-frame"><video id="promo" aria-labelledby="video-caption" controls
            playsinline preload="none" poster="/poster.jpg" width="1280" height="720">
            <source src="/oman-video.mp4" type="video/mp4">
            {anchor('/oman-video.mp4', t['videoFallback'])}
          </video></div><details class="video-summary"><summary>{h(t['videoTitle'])}</summary>
          <div>{paragraph(t['summary'])}</div></details></figure></div></section>
          {section('about', t['about'], paragraph(t['roleCopy']) + anchor(route(self.lang, 'about'), t['about']))}
          {self.process()}{self.countries()}{self.faq()}{self.contact()}'''

    def about_content(self):
        t = self.t
        trust = ''.join(f'<article class="trust-card"><h3>{h(t[key])}</h3>{paragraph(t[key + "Copy"])}</article>'
                        for key in ('role', 'agency', 'conditions', 'expectations'))
        return (self.heading('about', 'mission')
                + section('role', t['trustTitle'], f'<div class="trust-grid">{trust}</div>')
                + section('verification', t['agency'], paragraph(t['verify']) + official_links(AGENCY_LINKS)
                          + self.wa(t['agency'], t['agency'] + ' · WhatsApp'))
                + section('fraud', t['fraud'], paragraph(t['fraudText']) + official_links(REPORT_LINKS))
                + self.contact())

    def vacancy_cards(self):
        t = self.t
        cards = []
        states = ('confirmed', 'pending', 'closed', 'information')
        labels = dict(zip(states, t['status'].split(';'), strict=True))
        for row in CONFIG['vacancies']:
            status = row['status']
            copy = row['translations'][self.lang]
            title = copy['title']
            fields = [copy['destination'], copy['category']]
            terms = ''
            if status == 'confirmed':
                stamp = date.fromisoformat(row['verified_on']).isoformat()
                fields += [row['employer'], row['agency'], f'{t["verified"]} {stamp}']
                fields.append(copy['eligibility'])
                term_keys = ('pay', 'accommodation', 'meals', 'transport', 'medical', 'hours',
                             'overtime', 'duration', 'leave')
                values = copy.get('terms', {})
                items = []
                for key, label in zip(term_keys, t['payFields'].split(';'), strict=True):
                    value = values.get(key, t['contractDependent'])
                    items.append(f'<dt>{h(label)}</dt><dd>{h(value)}</dd>')
                terms = '<dl class="vacancy-terms">' + ''.join(items) + '</dl>'
            cta = self.wa(title, title + ' · WhatsApp') if status == 'confirmed' else ''
            cards.append(f'<article class="trust-card"><p class="eyebrow">{h(labels[status])}</p>'
                         f'<h3>{h(title)}</h3>{"".join(map(paragraph, fields))}{terms}{cta}</article>')
        enquiry = '' if any(row['status'] == 'confirmed' for row in CONFIG['vacancies']) else paragraph(t['empty'])
        grid = '<div class="trust-grid vacancy-grid">' + ''.join(cards) + '</div>' if cards else ''
        return enquiry + grid + self.wa(t['employment'])

    def jobs_content(self):
        t = self.t
        checks = ''.join(f'<label><input type="checkbox"> {h(t[key])}</label>'
                         for key in ('passport', 'identity', 'education', 'experience', 'professional',
                                     'medical', 'contract', 'otherDocs'))
        return (self.heading('jobs', 'lead')
                + section('vacancies', t['jobs'], self.vacancy_cards())
                + section('eligibility', t['eligibility'], paragraph(t['eligText'])
                          + self.wa(t['eligibility'], t['eligibility'] + ' · WhatsApp'))
                + section('salary', t['salary'], paragraph(t['salaryText'])
                          + self.wa(t['salary'], t['salary'] + ' · WhatsApp'))
                + section('documents', t['documents'], paragraph(t['docsText'])
                          + f'<fieldset class="checklist"><legend>{h(t["documents"])}</legend>{checks}</fieldset>')
                + self.countries() + self.contact())

    def privacy_content(self):
        t = self.t
        stamp = CONFIG['privacy_updated']
        sections = []
        for i in range(6):
            body = paragraph(t[f'policyBody{i}'])
            if i == 2:
                body += paragraph(t['storage'])
                body += official_links((('WhatsApp · Privacy Policy', 'https://www.whatsapp.com/legal/privacy-policy'),
                                        ('GitHub · Privacy Statement', 'https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement')))
            sections.append(section(f'privacy-{i}', t[f'policyHeading{i}'], body))
        return (f'<div class="page-heading"><div class="wrap"><h1>{h(t["privacy"])}</h1>'
                f'<p>{h(t["updated"])} <time datetime="{stamp}">{stamp}</time></p></div></div>'
                f'<div class="privacy-body">{"".join(sections)}</div>'
                + section('privacy-contact', t['privacyMessage'], self.wa(t['privacyMessage'], t['privacyMessage'])))

    def missing_content(self):
        return self.heading('missing', 'missingText') + section(
            'return', self.t['home'], anchor(self.home, self.t['home'], ' class="cta"'))

    def metadata(self, title, desc):
        if self.kind == '404':
            return '<meta name="robots" content="noindex,follow">'
        url = ORIGIN + route(self.lang, self.kind)
        options = {code: ORIGIN + route(code, self.kind) for code in LANG}
        options['x-default'] = options['ne']
        alternates = ''.join(f'<link rel="alternate" hreflang="{code}" href="{link}">'
                             for code, link in options.items())
        image = ORIGIN + '/social-preview.jpg'
        tags = {'title': title, 'description': desc, 'type': 'website', 'url': url,
                'site_name': BRAND, 'image': image, 'image:width': '1200', 'image:height': '630',
                'image:alt': BRAND, 'locale': LOCALE[self.lang]}
        og = ''.join(f'<meta property="og:{key}" content="{h(value, quote=True)}">' for key, value in tags.items())
        og += ''.join(f'<meta property="og:locale:alternate" content="{locale}">'
                      for code, locale in LOCALE.items() if code != self.lang)
        twitter = {'card': 'summary_large_image', 'title': title, 'description': desc, 'image': image,
                   'image:alt': BRAND}
        social = ''.join(f'<meta name="twitter:{key}" content="{h(value, quote=True)}">'
                         for key, value in twitter.items())
        org = ORIGIN + '/#organization'
        site = ORIGIN + '/#website'
        nodes = [
            {'@type': 'Organization', '@id': org, 'name': BRAND, 'url': ORIGIN + '/',
             'logo': ORIGIN + '/logo.webp'},
            {'@type': 'WebSite', '@id': site, 'name': BRAND, 'url': ORIGIN + '/',
             'inLanguage': list(LANG), 'publisher': {'@id': org}},
            {'@type': 'WebPage', '@id': url + '#page', 'name': title, 'description': desc,
             'url': url, 'inLanguage': self.lang, 'isPartOf': {'@id': site}},
        ]
        if self.kind:
            breadcrumbs = [(self.t['home'], ORIGIN + self.home), (title.split(' | ')[0], url)]
            nodes.append({'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': i, 'name': name, 'item': item}
                for i, (name, item) in enumerate(breadcrumbs, 1)]})
        schema = json.dumps({'@context': 'https://schema.org', '@graph': nodes}, ensure_ascii=False)
        schema = schema.replace('<', r'\u003c')
        return (f'<link rel="canonical" href="{url}">{alternates}{og}{social}'
                f'<script type="application/ld+json">{schema}</script>')

    def render(self, alias=''):
        t = self.t
        heading, summary, content = {
            '': ('hero', 'lead', self.home_content),
            'about': ('about', 'mission', self.about_content),
            'jobs': ('jobs', 'eligText', self.jobs_content),
            'privacy': ('privacy', 'policyBody0', self.privacy_content),
            '404': ('missing', 'missingText', self.missing_content),
        }[self.kind]
        title, desc = f'{t[heading]} | {BRAND}', t[summary]
        topic = t['privacyMessage'] if self.kind == 'privacy' else t['employment']
        validator_note = ('<!-- [html-validate-disable no-multiple-main, unique-landmark] -->'
                          if self.kind == '404' else '')
        return f'''<!DOCTYPE html>
{validator_note}
<html lang="{self.lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#073F30">
<title>{h(title)}</title>
<meta name="description" content="{h(desc, quote=True)}">
{self.metadata(title, desc)}
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="stylesheet" href="/site.css">
<script defer src="/site.js"></script>
</head>
<body data-alias="{alias}">
{self.layout(content, topic)}
{self.error_templates()}
</body>
</html>
'''

    def layout(self, content, topic):
        t = self.t
        return f'''
{anchor('#main', t['skip'], ' class="skip"')}
<header class="site-header"><div class="wrap header-row">{self.brand()}{self.nav('desktop-nav')}</div>
<div class="locale-bar"><div class="wrap locale-row">{self.languages()}</div></div></header>
<main id="main" tabindex="-1">{content()}</main>
{self.footer()}
{self.nav('mobile-nav')}
<div class="floating-rail">{self.wa(topic, t['whatsapp'], 'floating-wa')}</div>
'''

    def error_templates(self):
        if self.kind != '404':
            return ''
        templates = []
        for language in LANG:
            if language == self.lang:
                continue
            page = Page(language, '404')
            title = h(f'{page.t["missing"]} | {BRAND}', quote=True)
            layout = page.layout(page.missing_content, page.t['employment'])
            templates.append(f'<template id="error-{language}" data-title="{title}">{layout}</template>')
        return ''.join(templates)


def write(path, value):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(value, encoding='utf-8')


def build():
    sitemap_ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    html_ns = 'http://www.w3.org/1999/xhtml'
    ET.register_namespace('', sitemap_ns)
    ET.register_namespace('xhtml', html_ns)
    sitemap = ET.Element(f'{{{sitemap_ns}}}urlset')
    for lang in LANG:
        for kind in PAGES:
            path = route(lang, kind)
            write(path.lstrip('/') + 'index.html', Page(lang, kind).render())
            entry = ET.SubElement(sitemap, f'{{{sitemap_ns}}}url')
            ET.SubElement(entry, f'{{{sitemap_ns}}}loc').text = ORIGIN + path
            for code in (*LANG, 'x-default'):
                target = 'ne' if code == 'x-default' else code
                ET.SubElement(entry, f'{{{html_ns}}}link', rel='alternate', hreflang=code,
                              href=ORIGIN + route(target, kind))
    ET.indent(sitemap)
    write('sitemap.xml', ET.tostring(sitemap, encoding='unicode', xml_declaration=True) + '\n')
    write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n')
    write('index.html', Page('ne', '').render('home'))
    write('privacy.html', Page('ne', 'privacy').render('privacy'))
    write('404.html', Page('ne', '404').render())


if __name__ == '__main__':
    build()
