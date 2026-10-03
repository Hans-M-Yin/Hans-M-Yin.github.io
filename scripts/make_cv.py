"""Build the public CV from the same verified data as the website (reportlab)."""
import json
from pathlib import Path
from html import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/site.json').read_text())
out = ROOT / 'assets/files/Zhihan_Yin_CV.pdf'
styles = getSampleStyleSheet()
font_dir = Path(reportlab.__file__).parent / 'fonts'
for name, filename in [('CVSans','Vera.ttf'),('CVSans-Bold','VeraBd.ttf'),('CVSans-Italic','VeraIt.ttf'),('CVSans-BoldItalic','VeraBI.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
pdfmetrics.registerFontFamily('CVSans', normal='CVSans', bold='CVSans-Bold', italic='CVSans-Italic', boldItalic='CVSans-BoldItalic')
styles.add(ParagraphStyle(name='Name', fontName='CVSans-Bold', fontSize=22, leading=27, textColor=colors.HexColor('#182638'), spaceAfter=6))
styles.add(ParagraphStyle(name='SectionTitle', fontName='CVSans-Bold', fontSize=9, leading=12, textColor=colors.HexColor('#3d689e'), spaceBefore=10, spaceAfter=4))
styles.add(ParagraphStyle(name='Text', fontName='CVSans', fontSize=8.5, leading=11, spaceAfter=3))
styles.add(ParagraphStyle(name='SmallText', fontName='CVSans', fontSize=7.5, leading=10, spaceAfter=3, textColor=colors.HexColor('#4b5563')))
story = []
def p(text, style='Text'):
    return Paragraph(text, styles[style])
def section(title):
    story.extend([p(title.upper(), 'SectionTitle'), HRFlowable(width='100%', thickness=.5, color=colors.HexColor('#dce3ec')), Spacer(1, 5)])
story.extend([p(escape(data['name']), 'Name'), p(f'<link href="mailto:{data["email"]}">{data["email"]}</link> | <link href="{data["url"]}">hans-m-yin.github.io</link> | <link href="https://github.com/{data["username"]}">GitHub</link>')])
section('Research interests')
story.append(p('Multimodal agents; autonomous cross-modal search; vision-language model reasoning; fine-grained visual perception and hallucination; alignment and RL post-training.'))
section('Education')
e = data['education']
story.extend([p(f'<b>{e["school"]}</b> | {e["dates"]}'), p(f'{e["degree"]} | Cumulative GPA: {e["gpa"]}')])
section('Selected publications and manuscripts')
for paper in data['papers']:
    if paper['category'] == 'ongoing':
        continue  # Author list and final publication details are not yet available.
    authors = ', '.join('<b>'+escape(a)+'</b>' if a == data['name'] else escape(a) for a in paper['authors'])
    story.append(KeepTogether([p('<b>'+escape(paper['title'])+'</b>'), p(authors, 'SmallText'), p('<i>'+escape(paper['status'])+'</i>', 'SmallText'), p(escape(paper['summary']), 'SmallText'), Spacer(1, 5)]))
section('Research and teaching experience')
for x in data['experience']:
    story.append(KeepTogether([p(f'<b>{escape(x["role"])}</b>, {escape(x["organization"])}'), p(x['dates'], 'SmallText'), p(escape(x['description']), 'SmallText')]))
section('Honors and awards')
for a in data['awards']:
    story.append(p(f'<b>{a["name"]}</b> ({a["detail"]}) | {a["years"]}'))
section('Skills')
for s in data['skills']:
    story.append(p(f'<b>{s["label"]}:</b> {s["value"]}'))
doc = SimpleDocTemplate(str(out), pagesize=A4, rightMargin=34, leftMargin=34, topMargin=30, bottomMargin=30, title='Zhihan Yin - Curriculum Vitae', author='Zhihan Yin')
doc.build(story)
print(out)
