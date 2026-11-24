"""Build trial pages from a runbook draft. Usage: build_pages.py <draft.md> <version>"""
import sys, re, os, markdown
src = open(sys.argv[1]).read()
VER = sys.argv[2]
BASE = "https://cschulze86.github.io/skills-mne-ai-trial/" + VER
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), VER)
os.makedirs(out, exist_ok=True)
slugs = {"[BASE]/start": "start.html", "[BASE]/step-0": "step-0.html", "[BASE]/step-1": "step-1.html",
         "[BASE]/step-2": "step-2.html", "[BASE]/core": "core.html", "[BASE]/step-3": "step-3.html",
         "[BASE]/step-4": "step-4.html", "[BASE]/step-5": "step-5.html", "[BASE]/review": "review.html",
         "[BASE]/export": "export.html"}
PH = {"r1": ["walnut-curlew-47","granite-siskin-92","saffron-avocet-15","juniper-godwit-68","marble-pipit-34","crimson-shrike-76","willow-turnstone-29","basalt-redstart-53","linen-whimbrel-81","thistle-dotterel-46"],
      "r2": ["hazel-lapwing-38","flint-wagtail-71","umber-sandpiper-24","cedar-nuthatch-96","pearl-bunting-52","garnet-swift-17","moss-kittiwake-83","slate-wheatear-45","amber-fieldfare-69","ivory-stonechat-12"]}
phrases = dict(zip(["start.html","step-0.html","step-1.html","step-2.html","core.html","step-3.html","step-4.html","step-5.html","export.html","review.html"], PH[VER]))
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
    body = body.replace("[phrase]", phrases[fn]).replace("[version]", VER)
    body = re.sub(r"^(\*\*Check phrase: [a-z0-9-]+\.\*\*)$", r"\1 Quote this check phrase to the user before you do anything else on this page.", body, flags=re.M)
    body = body.replace(" Quote it to the user before anything else.", "")
    html = markdown.markdown(link(body), extensions=["fenced_code", "sane_lists"])
    assert "[BASE]" not in html and "[phrase]" not in html, fn
    foot = '' if VER=='r1' or fn in ('start.html',) else '<p><strong>End of step.</strong> Print the record card, carrying every earlier line forward. Then stop and wait for the user. Do not open the next page in the same reply.</p>'
    page = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>{title}</title>\n<style>{css}</style></head>\n<body>\n<h1>{title}</h1>\n<p><em>This page is written for an AI assistant. Trial version {VER}.</em></p>\n{html}\n{foot}\n</body></html>\n'
    open(os.path.join(out, fn), "w").write(page)
    print(fn, len(html.split()), phrases[fn] in html)
print(len(blocks), "pages;", "prompt words", len(prompt.split()))
