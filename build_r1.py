"""Build the r1 trial pages from the runbook draft. Usage: build_r1.py <draft.md>"""
import sys, re, os, markdown
src = open(sys.argv[1]).read()
BASE = "https://cschulze86.github.io/skills-mne-ai-trial/r1"
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r1")
slugs = {"[BASE]/start": "start.html", "[BASE]/step-0": "step-0.html", "[BASE]/step-1": "step-1.html",
         "[BASE]/step-2": "step-2.html", "[BASE]/core": "core.html", "[BASE]/step-3": "step-3.html",
         "[BASE]/step-4": "step-4.html", "[BASE]/step-5": "step-5.html", "[BASE]/review": "review.html",
         "[BASE]/export": "export.html"}
phrases = {"start.html": "walnut-curlew-47", "step-0.html": "granite-siskin-92", "step-1.html": "saffron-avocet-15",
           "step-2.html": "juniper-godwit-68", "core.html": "marble-pipit-34", "step-3.html": "crimson-shrike-76",
           "step-4.html": "willow-turnstone-29", "step-5.html": "basalt-redstart-53", "export.html": "linen-whimbrel-81",
           "review.html": "thistle-dotterel-46"}
def link(text):
    for k in sorted(slugs, key=len, reverse=True):
        text = text.replace(k, BASE + "/" + slugs[k])
    return text
# prompt file
m = re.search(r"## Part A.*?```\n(.*?)```", src, re.S)
prompt = link(m.group(1))
open(os.path.join(out, "AI_assistant_prompt.txt"), "w").write(prompt)
# pages
partb = src[src.index("## Part B"):src.index("## Notes for Charles")]
blocks = re.split(r"\n### ", partb)[1:]
css = "body{font-family:Georgia,serif;max-width:44rem;margin:2rem auto;padding:0 1rem;line-height:1.5}pre{background:#f2f2f2;padding:.8rem;white-space:pre-wrap}"
for b in blocks:
    head, body = b.split("\n", 1)
    mm = re.search(r"\(`(\[BASE\]/[a-z0-9-]+)`\)", head)
    fn = slugs[mm.group(1)]
    title = head[:mm.start()].strip()
    body = body.replace("---", "").strip()
    body = body.replace("[phrase]", phrases[fn]).replace("[version]", "r1")
    body = re.sub(r"^(\*\*Check phrase: [a-z0-9-]+\.\*\*)$", r"\1 Quote this check phrase to the user before you do anything else on this page.", body, flags=re.M)
    body = body.replace(" Quote it to the user before anything else.", "")
    html = markdown.markdown(link(body), extensions=["fenced_code", "sane_lists"])
    assert "[BASE]" not in html and "[phrase]" not in html, fn
    page = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>{title}</title>\n<style>{css}</style></head>\n<body>\n<h1>{title}</h1>\n<p><em>This page is written for an AI assistant. Trial version r1.</em></p>\n{html}\n</body></html>\n'
    open(os.path.join(out, fn), "w").write(page)
    print(fn, len(html.split()), phrases[fn] in html)
print(len(blocks), "pages;", "prompt words", len(prompt.split()))
