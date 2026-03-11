from pathlib import Path
import csv, hashlib, json, random, re, time
import requests
from gtts import gTTS
import genanki

ROOT = Path(__file__).resolve().parent
SRC_TXT = ROOT / 'source' / 'flyers-a2-pages.txt'
OUT_DIR = ROOT / 'out'
MEDIA_DIR = OUT_DIR / 'media'
CSV_PATH = OUT_DIR / 'flyers_anki_import.csv'
JSON_PATH = OUT_DIR / 'flyers_words.json'
APKG_PATH = OUT_DIR / 'Flyers_Paper_Dictation_TTS_v2.apkg'
DECK_NAME = 'Flyers::Paper Dictation (TTS) v2'
MODEL_ID = 1607392320
DECK_ID = 2059400111

OUT_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

POS_RE = re.compile(r'\s+(adj|adv|conj|det|dis|excl|int|n|poss|prep|pron|v)(\s*\+\s*(adj|adv|conj|det|dis|excl|int|n|poss|prep|pron|v))*$')
SKIP = {
    'A2 Flyers A–Z wordlist','Grammatical key','adjective','adverb','conjunction','determiner',
    'discourse marker','exclamation','interrogative','noun','possessive','preposition','pronoun','verb',
    'adj','adv','conj','det','dis','excl','int','n','poss','prep','pron','v'
}


def parse_terms():
    text = SRC_TXT.read_text(encoding='utf-8').split('Numbers')[0]
    lines = [ln.strip() for ln in text.splitlines()]
    clean = []
    for ln in lines:
        if not ln or ln in SKIP:
            continue
        if ln.startswith('A2 Flyers A–Z wordlist'):
            continue
        if re.fullmatch(r'[A-Z]', ln) or re.fullmatch(r'\d+', ln):
            continue
        clean.append(ln)

    entries = []
    i = 0
    while i < len(clean):
        ln = clean[i]
        cand = ln
        while i + 1 < len(clean):
            if POS_RE.search(cand) or cand in ['a.m. (for time)', 'p.m. (for time)']:
                break
            nxt = clean[i + 1]
            if nxt in ['a.m. (for time)', 'p.m. (for time)']:
                break
            cand = f'{cand} {nxt}'
            i += 1
        entries.append(cand)
        i += 1

    terms = []
    for e in entries:
        term = POS_RE.sub('', e).strip()
        term = term.replace('chemist(’s)', "chemist('s)")
        term = term.replace('…', '...')
        terms.append(term)

    fixed = []
    for t in terms:
        if t == 'for prep of time forget':
            fixed.extend(['for', 'forget'])
            continue
        fixed.append(t)

    seen = set()
    result = []
    for t in fixed:
        key = t.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(t)
    return result


def classify_level(term: str) -> str:
    if re.search(r'[()/]|\.\.\.|-|\'|\b[a-z]\.[a-z]\.|\bUS\b|\bUK\b', term):
        return 'tricky'
    if ' ' in term:
        return 'tricky'
    if len(term) <= 5:
        return 'core'
    return 'extended'


def clean_for_tts(term: str) -> str:
    # Prefer the headword for speaking; remove parenthetical regional notes.
    spoken = re.sub(r'\s*\([^)]*\)', '', term).strip()
    spoken = spoken.replace(' ... ', ' as ')
    spoken = spoken.replace('/', ' or ')
    return spoken


def translate_word(term: str) -> str:
    q = clean_for_tts(term)
    url = 'https://translate.googleapis.com/translate_a/single'
    params = {'client': 'gtx', 'sl': 'en', 'tl': 'zh-CN', 'dt': 't', 'q': q}
    last_error = None
    for attempt in range(5):
        try:
            r = requests.get(url, params=params, timeout=20)
            r.raise_for_status()
            data = r.json()
            return ''.join(part[0] for part in data[0]).strip()
        except Exception as e:
            last_error = e
            time.sleep(1 + attempt * 2)
    print(f'[WARN] translate failed for {term}: {last_error}', flush=True)
    return q


def make_audio(term: str) -> str:
    spoken = clean_for_tts(term)
    base = hashlib.md5(spoken.encode('utf-8')).hexdigest()[:16]
    filename = f'{base}.mp3'
    path = MEDIA_DIR / filename
    if not path.exists():
        last_error = None
        for attempt in range(5):
            try:
                tts = gTTS(spoken, lang='en', tld='co.uk', slow=False)
                tts.save(str(path))
                time.sleep(0.2)
                break
            except Exception as e:
                last_error = e
                time.sleep(1 + attempt * 2)
        else:
            raise RuntimeError(f'gTTS failed for {term}: {last_error}')
    return filename


def build_package(items):
    model = genanki.Model(
        MODEL_ID,
        'Flyers Paper Dictation Model v2',
        fields=[
            {'name': 'English'},
            {'name': 'Chinese'},
            {'name': 'Audio'},
            {'name': 'Level'},
            {'name': 'Source'},
        ],
        templates=[{
            'name': 'Paper Dictation',
            'qfmt': '''<div style="font-family: Arial; font-size: 20px; text-align:center; line-height:1.6;">
<div style="font-size:28px; font-weight:700; margin-bottom:12px;">听写卡</div>
<div style="margin-bottom:14px;">先听，再让孩子在纸上写。</div>
<div style="font-size:22px; margin:14px 0;">{{Audio}}</div>
<div style="color:#666; font-size:16px;">写完后翻面，由家长手动判断对错。</div>
</div>''',
            'afmt': '''<div style="font-family: Arial; font-size: 20px; line-height:1.7;">
<div style="font-size:28px; font-weight:700; text-align:center; margin-bottom:14px;">答案</div>
<div><b>单词：</b>{{English}}</div>
<div><b>中文：</b>{{Chinese}}</div>
<div><b>分层：</b>{{Level}}</div>
<div><b>音频：</b>{{Audio}}</div>
<div style="margin-top:14px; color:#666; font-size:15px;">建议：写对点 Good；模糊点 Hard；写错点 Again。</div>
</div>'''
        }],
        css='''.card { background:#fff; color:#111; }'''
    )

    deck = genanki.Deck(DECK_ID, DECK_NAME)
    media_files = []
    for item in items:
        media_files.append(str(MEDIA_DIR / item['audio_file']))
        note = genanki.Note(
            model=model,
            fields=[
                item['english'],
                item['chinese'],
                f"[sound:{item['audio_file']}]",
                item['level'],
                item['source'],
            ],
            tags=['flyers', item['level']]
        )
        deck.add_note(note)

    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(str(APKG_PATH))


def main():
    terms = parse_terms()
    items = []
    for i, term in enumerate(terms, start=1):
        print(f'[{i}/{len(terms)}] {term}', flush=True)
        chinese = translate_word(term)
        audio_file = make_audio(term)
        items.append({
            'english': term,
            'chinese': chinese,
            'audio_file': audio_file,
            'level': classify_level(term),
            'source': 'Cambridge English A2 Flyers word list (official PDF)',
        })

    with CSV_PATH.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['English', 'Chinese', 'Audio', 'Level', 'Source'])
        writer.writeheader()
        for item in items:
            writer.writerow({
                'English': item['english'],
                'Chinese': item['chinese'],
                'Audio': f"[sound:{item['audio_file']}]",
                'Level': item['level'],
                'Source': item['source'],
            })

    JSON_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
    build_package(items)
    print(f'Built: {APKG_PATH}')


if __name__ == '__main__':
    main()
