"""Strip HTML to text (stdlib only). Usage: python3 -I html2txt.py in.html out.txt"""
import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s): super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in ('script','style','noscript','svg'): s.skip+=1
        if t in ('p','div','h1','h2','h3','h4','li','br','tr','figcaption','blockquote'): s.out.append('\n')
        if t=='img':
            d=dict(a); 
            if d.get('src') and 'substack' in (d.get('src') or ''): s.out.append(f"\n[IMG {d.get('src')} alt={d.get('alt')}]\n")
    def handle_endtag(s,t):
        if t in ('script','style','noscript','svg'): s.skip=max(0,s.skip-1)
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8',errors='replace').read())
t=re.sub(r'\n\s*\n+','\n\n',''.join(p.out))
open(sys.argv[2],'w').write(t); print(len(t))
