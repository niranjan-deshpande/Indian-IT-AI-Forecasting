"""Extract plain text from a .docx. Usage: python3 -I docx_text.py FILE"""
import sys, zipfile, re, html
with zipfile.ZipFile(sys.argv[1]) as z:
    x = z.read("word/document.xml").decode("utf8")
x = re.sub(r"</w:p>", "\n", x)
x = re.sub(r"<w:tab/>", "\t", x)
print(html.unescape(re.sub(r"<[^>]+>", "", x)))
