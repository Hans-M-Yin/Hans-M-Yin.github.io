"""Generate complete static HTML; Python standard library only."""
import json
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = json.loads((ROOT / 'data/site.json').read_text())
ICONS = {
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
    'github': '<path d="M9 19c-4.3 1.3-4.3-2.2-6-2.7m12 5v-3.7a3.2 3.2 0 0 0-.9-2.5c3-.3 6.2-1.5 6.2-6.8a5.3 5.3 0 0 0-1.5-3.7 4.9 4.9 0 0 0-.1-3.7s-1.2-.4-3.8 1.4a13 13 0 0 0-6.8 0C5.5.5 4.3.9 4.3.9a4.9 4.9 0 0 0-.1 3.7 5.3 5.3 0 0 0-1.5 3.7c0 5.3 3.2 6.5 6.2 6.8a3.2 3.2 0 0 0-.9 2.5v3.7"/>',
    'file': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h6"/>',
    'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
    'theme': '<path d="M20.5 13A8.5 8.5 0 0 1 11 3.5 8.5 8.5 0 1 0 20.5 13Z"/>',
    'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>',
    'arrow': '<path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/>'
}
def icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'
def authors(p):
    if not p['authors']:
        return '<p class="authors">Ongoing research</p>'
    items = [f'<strong>{esc(a)}</strong>' if a == D['name'] else esc(a) for a in p['authors']]
    return '<p class="authors">'+', '.join(items)+'</p>'
def paper(p):
    label = '<span class="status-pill">Work in progress</span>' if p['category'] == 'ongoing' else esc(p['status'])
    if p['category'] == 'ongoing':
        label += '2026'
    actions = ''.join(f'<a href="{esc(l["url"])}" target="_blank" rel="noopener noreferrer">{esc(l["label"])}</a>' for l in p['links'])
    actions += f'<details><summary>Overview</summary><div class="details-copy">{esc(p["details"])}</div></details>'
    if p['bib']:
        actions += f'<details><summary>Bib</summary><div class="details-copy"><pre>{esc(p["bib"])}</pre></div></details>'
    return f'''<article class="paper" id="{p['id']}" data-paper-category="{p['category']}">
      <a class="paper-image-link" href="/publications/#{p['id']}" aria-label="Read about {p['short']}"><img class="paper-image" src="/assets/images/{p['image']}" alt="{esc(p['alt'])}" width="180" height="126" loading="lazy"></a>
      <div><h3><a href="/publications/#{p['id']}">{esc(p['title'])}</a></h3>{authors(p)}<div class="venue">{label}</div><p class="summary">{esc(p['summary'])}</p><div class="paper-actions">{actions}</div></div>
    </article>'''
def papers():
    return '<div class="papers">'+''.join(paper(p) for p in D['papers'])+'</div>'
def section_title(title, url, action):
    return f'<div class="section-title"><h2>{title}</h2><a href="{url}">{action} &rarr;</a></div>'
def home():
    if D['portrait']:
        portrait = f'<img class="portrait" src="{esc(D["portrait"])}" alt="Zhihan Yin" width="272" height="272">'
    else:
        portrait = '<div class="portrait portrait-monogram" role="img" aria-label="Zhihan Yin initials">ZY</div>'
    interests = ''.join(f'<li>{esc(i)}</li>' for i in D['interests'])
    news = ''.join(f'<tr><td>{n["date"]}</td><td>{esc(n["text"])}</td></tr>' for n in D['news'])
    return f'''<h1>Zhihan Yin</h1><p class="tagline">{esc(D['tagline'])}</p>
    <div class="intro-grid"><div class="intro-copy">
    <p>Hi, I am <strong>Zhihan Yin</strong>.</p>
    <p>I am an undergraduate student in Intelligence Science and Technology at <a href="https://english.pku.edu.cn/">Peking University</a> and a research intern in <a href="https://www.bytedance.com/en/">Monetization GenAI at ByteDance</a>. I also conduct research at the Wangxuan Institute of Computer Technology, Peking University.</p>
    <p>My research focuses on <strong>multimodal agents, visual perception, and reasoning</strong>. I am especially interested in how models acquire evidence across modalities, recognize perceptual errors, and reason reliably with what they see.</p>
    <p>My work includes fine-grained hallucination evaluation (<a href="/publications/#freak">FREAK, ICLR 2026</a>), training-free visual perception (<a href="/publications/#veto">Veto, ACM MM 2026</a>), and reinforcement learning for robust multimodal reasoning (<a href="/publications/#mira">MIRA, NeurIPS 2026 Poster</a>).</p>
    <h2>Research Interests</h2><ul class="interests">{interests}</ul>
    </div><aside class="profile" aria-label="Profile and contact">
    {portrait}<p class="affiliation">Peking University</p><p class="department">Intelligence Science and Technology</p>
    <div class="social-links"><a href="mailto:{D['email']}" aria-label="Email Zhihan Yin" title="Email">{icon('mail')}</a><a href="https://github.com/{D['username']}" aria-label="GitHub profile" title="GitHub">{icon('github')}</a><a href="/assets/files/Zhihan_Yin_CV.pdf" aria-label="Download curriculum vitae" title="CV" download>{icon('file')}</a></div><p class="contact-note">The best way to reach me is via email.</p>
    </aside></div>
    <h2>News</h2><table class="news-table" aria-label="Research news"><tbody>{news}</tbody></table>
    {section_title('Selected Research', '/publications/', 'All publications & manuscripts')}{papers()}
    {section_title('Experience', '/cv/', 'Full CV')}
    <div class="cv-item"><div class="cv-date">Apr 2026 - Present</div><div><h3>Research Intern · ByteDance</h3><p class="cv-detail">Monetization GenAI · Multimodal agents</p></div></div>
    <div class="cv-item"><div class="cv-date">Mar 2025 - Present</div><div><h3>Research Intern · Peking University</h3><p class="cv-detail">Wangxuan Institute of Computer Technology · Multimodal learning</p></div></div>'''
def publications():
    return f'''<h1>Publications &amp; Manuscripts</h1><p class="page-lead">Research on multimodal agents, reliable visual perception, and reasoning.</p>
    <div class="filters" aria-label="Filter research entries"><button class="filter" data-filter="all" aria-pressed="true">All research</button><button class="filter" data-filter="published" aria-pressed="false">Published</button><button class="filter" data-filter="manuscript" aria-pressed="false">Manuscripts</button><button class="filter" data-filter="ongoing" aria-pressed="false">In progress</button></div>
    <span class="sr-only" data-filter-status role="status" aria-live="polite"></span><h2 class="year-heading">2026</h2>{papers()}'''
def projects():
    cards = []
    for p in D['papers']:
        link = f'<a href="/publications/#{p["id"]}">Read more &rarr;</a>'
        if p['id'] == 'freak':
            link += ' &nbsp; <a href="https://github.com/Hans-M-Yin/FREAK">Code &rarr;</a>'
        cards.append(f'<article class="project-card"><img src="/assets/images/{p["image"]}" alt="{esc(p["alt"])}"><div class="project-copy"><span class="status-pill">{esc(p["status"])}</span><h2>{p["short"]}</h2><p>{esc(p["summary"])}</p>{link}</div></article>')
    return '<h1>Projects</h1><p class="page-lead">From evaluating what models see to teaching agents how to search.</p><div class="project-grid">'+''.join(cards)+'</div>'
def cv():
    e = D['education']
    content = f'''<div class="cv-header"><div><h1>Curriculum Vitae</h1><p class="page-lead">Zhihan Yin · Peking University</p></div><a class="download-link" href="/assets/files/Zhihan_Yin_CV.pdf" download>Download PDF</a></div>
    <section class="cv-section"><h2>Education</h2><div class="cv-item"><div class="cv-date">{e['dates']}</div><div><h3>{e['school']}</h3><p>{e['degree']}</p><p class="cv-detail">Cumulative GPA: {e['gpa']}</p></div></div></section>
    <section class="cv-section"><h2>Research &amp; Teaching Experience</h2>'''
    for x in D['experience']:
        content += f'<div class="cv-item"><div class="cv-date">{x["dates"]}</div><div><h3>{esc(x["role"])}</h3><p>{esc(x["organization"])}</p><p class="cv-detail">{esc(x["description"])}</p></div></div>'
    content += '</section><section class="cv-section"><h2>Selected Publications &amp; Manuscripts</h2>'
    for p in D['papers']:
        if p['category'] == 'ongoing':
            continue
        content += f'<div class="cv-paper"><h3><a href="/publications/#{p["id"]}">{esc(p["title"])}</a></h3>{authors(p)}<div class="venue">{esc(p["status"])}</div></div>'
    content += '</section><section class="cv-section"><h2>Honors &amp; Awards</h2>'
    for a in D['awards']:
        content += f'<div class="cv-item"><div class="cv-date">{a["years"]}</div><div><h3>{a["name"]}</h3><p class="cv-detail">{a["detail"]}</p></div></div>'
    content += '</section><section class="cv-section"><h2>Skills</h2><dl class="skill-list">'
    for s in D['skills']:
        content += f'<dt>{s["label"]}</dt><dd>{s["value"]}</dd>'
    return content+'</dl></section>'
NAV = [('About', '/'), ('Publications', '/publications/'), ('Projects', '/projects/'), ('CV', '/cv/')]
INDEX = [{'title':n, 'url':u, 'text':n+' '+D['name'], 'type':'Page'} for n,u in NAV]
INDEX += [{'title':p['title'], 'url':'/publications/#'+p['id'], 'text':p['summary']+' '+p['details'], 'type':p['status']} for p in D['papers']]
def layout(title, path, body):
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if url == path else '')+f'>{label}</a>' for label,url in NAV)
    full_title = 'Zhihan Yin' if path == '/' else title+' | Zhihan Yin'
    structured = json.dumps({'@context':'https://schema.org', '@type':'Person', 'name':D['name'], 'url':D['url'], 'email':D['email'], 'sameAs':['https://github.com/'+D['username']], 'affiliation':{'@type':'Organization','name':'Peking University'}})
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(full_title)}</title><meta name="description" content="Zhihan Yin is an undergraduate at Peking University working on multimodal agents, visual perception, hallucination, and reasoning."><meta name="theme-color" content="#f7f9fc"><link rel="canonical" href="{D['url']+path}"><meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="Multimodal agents, reliable visual perception, and reasoning."><meta property="og:type" content="website"><meta property="og:url" content="{D['url']+path}"><link rel="icon" href="/assets/images/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/css/style.css"><script>try{{document.documentElement.dataset.theme=localStorage.getItem('theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}}catch(e){{}}</script><script type="application/ld+json">{structured}</script><script src="/assets/js/site.js" defer></script></head>
<body class="{'home' if path == '/' else 'page'}"><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="header-inner"><a class="wordmark" href="/">Zhihan Yin</a><button class="icon-button mobile-menu" data-menu-toggle aria-label="Toggle navigation" aria-expanded="false" aria-controls="site-nav">{icon('menu')}</button><nav class="nav" id="site-nav" aria-label="Main navigation">{nav}<button class="icon-button" data-open-search aria-label="Search website"><span class="shortcut">⌘ K</span>{icon('search')}</button><button class="icon-button" data-theme-toggle aria-label="Switch to dark theme" aria-pressed="false">{icon('theme')}</button></nav></div></header>
<main id="main">{body}</main>
<footer class="footer"><span>© 2026 Zhihan Yin. Hosted by <a href="https://pages.github.com/">GitHub Pages</a>.</span><span><a href="mailto:{D['email']}">Email</a> &nbsp; / &nbsp; <a href="https://github.com/{D['username']}">GitHub</a></span></footer>
<dialog class="search-dialog" id="search-dialog" aria-label="Search website"><div class="search-header">{icon('search')}<input type="search" id="site-search" placeholder="Search research, projects, and CV…" aria-label="Search research, projects, and CV" autocomplete="off"><button class="close-search" data-close-search aria-label="Close search">ESC</button></div><ul class="search-results" id="search-results"></ul><div class="search-hint">Search by title or topic · Escape to close</div></dialog><script type="application/json" id="search-index">{json.dumps(INDEX).replace('<', chr(92)+'u003c')}</script></body></html>'''
for title,path,content in [('About','/',home()),('Publications','/publications/',publications()),('Projects','/projects/',projects()),('CV','/cv/',cv())]:
    target = ROOT/path.strip('/')/'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(layout(title,path,content))
(ROOT/'404.html').write_text(layout('Page not found','/404.html','<h1>Page not found</h1><p>This page may have moved. <a href="/">Return to the homepage</a>.</p>'))
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+D['url']+u+'</loc></url>' for _,u in NAV)+'</urlset>')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+D['url']+'/sitemap.xml\n')
(ROOT/'.nojekyll').touch()
print('Built homepage, publications, projects, CV, 404, and sitemap.')
