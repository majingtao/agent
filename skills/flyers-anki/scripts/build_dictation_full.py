from pathlib import Path
import csv, hashlib, html, json, re, time
import requests
from gtts import gTTS
import genanki

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'data' / 'smf_selected_dictation.csv'
OUT = ROOT / 'out'
MEDIA = OUT / 'dictation_full_media'
OUT.mkdir(exist_ok=True)
MEDIA.mkdir(exist_ok=True)
CSV_OUT = OUT / 'smf_dictation_full.csv'
JSON_OUT = OUT / 'smf_dictation_full.json'
APKG_OUT = OUT / 'SMF_Dictation_Full.apkg'
README_OUT = OUT / 'SMF_Dictation_Full_README.md'

MODEL_ID = 25030911
DECK_ID = 25030912
MODEL_NAME = 'SMF Dictation Full'
DECK_NAME = 'SMF::Dictation Full'

GOOGLE = 'https://translate.googleapis.com/translate_a/single'

PHRASE_EXAMPLES = {
    'bus station': 'We are waiting at the bus station.',
    'bus stop': 'The children are standing at the bus stop.',
    'look after': 'I look after my little brother after school.',
    'look like': 'This cloud looks like a rabbit.',
    'go out': 'We do not go out in the rain.',
    'turn on': 'Please turn on the light.',
    'turn off': 'Please turn off the computer.',
    'find out': 'We want to find out the answer.',
    'at the moment': 'She is doing her homework at the moment.',
    'post office': 'My mother is at the post office.',
    'police station': 'The police station is near the park.',
    'railway station': 'We will meet at the railway station.',
}
VERB_WORDS = {
    'buy','find','finish','go','help','jump','learn','listen','look','make','open','paint','play','put','read','ride','run','say','see','show','sing','sit','sleep','smile','spell','swim','talk','tell','think','throw','walk','watch','write','act','ask','carry','clean','close','come','cook','count','draw','drink','drive','eat','give','turn','touch','study','save','search','thank','win'
}
ADJ_HINTS = {'brown','beautiful','broken','busy','friendly','important','interested','interesting','noisy','popular','same','soft','special','strange','sure','tidy','unfriendly','unhappy','wonderful','young','tall','short','happy','sad','cold','hot','clean','dirty','easy','ugly'}


def fetch_translate(text: str) -> str:
    last = None
    for i in range(5):
        try:
            r = requests.get(GOOGLE, params={'client':'gtx','sl':'en','tl':'zh-CN','dt':'t','q':text}, timeout=20)
            r.raise_for_status()
            data = r.json()
            return ''.join(part[0] for part in data[0]).strip()
        except Exception as e:
            last = e
            time.sleep(1 + i)
    raise RuntimeError(f'translate failed for {text}: {last}')


def clean_tts_text(word: str) -> str:
    spoken = re.sub(r'\s*\([^)]*\)', '', word).strip()
    spoken = spoken.replace(' ... ', ' as ')
    return spoken


def make_audio(word: str, region: str) -> str:
    spoken = clean_tts_text(word)
    key = hashlib.md5(f'{region}:{spoken}'.encode()).hexdigest()[:16]
    name = f'{key}_{region}.mp3'
    path = MEDIA / name
    if not path.exists():
        tld = 'co.uk' if region == 'uk' else 'com'
        last = None
        for i in range(5):
            try:
                gTTS(spoken, lang='en', tld=tld, slow=False).save(str(path))
                time.sleep(0.15)
                break
            except Exception as e:
                last = e
                time.sleep(1 + i)
        else:
            raise RuntimeError(f'gTTS failed for {word}/{region}: {last}')
    return name


def infer_example(word: str, phrase_type: str, topic: str) -> str:
    if word in PHRASE_EXAMPLES:
        return PHRASE_EXAMPLES[word]
    if phrase_type == 'phrase':
        return f'We can use "{word}" in a simple sentence.'
    wl = word.lower()
    if wl in VERB_WORDS:
        return f'I can {wl} it after school.'
    if wl in ADJ_HINTS:
        return f'This is a {wl} one.'
    if topic == 'animals':
        return f'I can see a {wl} at the zoo.'
    if topic == 'food':
        return f'I like eating {wl} for lunch.'
    if topic == 'school':
        return f'I can see the {wl} in my classroom.'
    if topic == 'places':
        return f'We can go to the {wl} today.'
    if topic == 'time':
        return f'We will talk about {wl} in class today.'
    if topic == 'actions':
        return f'I can {wl} with my friends.'
    if topic == 'people':
        return f'The {wl} is very kind.'
    article = 'an' if wl[:1] in 'aeiou' else 'a'
    return f'I can see {article} {wl} here.'


def highlight_target(sentence: str, word: str) -> str:
    target = word
    pattern = re.compile(re.escape(target), re.I)
    if pattern.search(sentence):
        return pattern.sub(lambda m: f'<span style="color:red;"><b>{html.escape(m.group(0))}</b></span>', sentence, count=1)
    return html.escape(sentence)


with SRC.open(encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

items = []
for idx, r in enumerate(rows, 1):
    word = r['word']
    print(f'[{idx}/{len(rows)}] {word}', flush=True)
    zh = fetch_translate(clean_tts_text(word))
    ex_en_plain = infer_example(clean_tts_text(word), r['phrase_type'], r['topic'])
    ex_zh = fetch_translate(ex_en_plain)
    ex_en = highlight_target(ex_en_plain, clean_tts_text(word))
    audio_uk = make_audio(word, 'uk')
    audio_us = make_audio(word, 'us')
    items.append({
        'English': word,
        'Chinese': zh,
        'Audio_UK': f'[sound:{audio_uk}]',
        'Audio_US': f'[sound:{audio_us}]',
        'Example_EN': ex_en,
        'Example_ZH': ex_zh,
        'Level': r['level_label'],
        'Topic': r['topic'],
        'Source': r['source'],
        'audio_uk_file': audio_uk,
        'audio_us_file': audio_us,
    })

with CSV_OUT.open('w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=['English','Chinese','Audio_UK','Audio_US','Example_EN','Example_ZH','Level','Topic','Source'])
    w.writeheader()
    for item in items:
        w.writerow({k:item[k] for k in ['English','Chinese','Audio_UK','Audio_US','Example_EN','Example_ZH','Level','Topic','Source']})

JSON_OUT.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')

model = genanki.Model(
    MODEL_ID,
    MODEL_NAME,
    fields=[
        {'name': 'English'},{'name': 'Chinese'},{'name': 'Audio_UK'},{'name': 'Audio_US'},
        {'name': 'Example_EN'},{'name': 'Example_ZH'},{'name': 'Level'},{'name': 'Topic'},{'name': 'Source'},
    ],
    templates=[{
        'name': 'Dictation Card',
        'qfmt': '''<div class="wrap"><div class="title">听写卡</div><div class="sub">打开卡片时自动播放一次英式发音。</div><div class="audio-row"><button onclick="playUk()">按钮1：英式</button><button onclick="playUs()">按钮2：美式</button></div><div class="help">正面不显示中文提示，不显示答案。</div></div><div id="uk" style="display:none;">{{Audio_UK}}</div><div id="us" style="display:none;">{{Audio_US}}</div><script>function clickAudio(id){var root=document.getElementById(id);if(!root)return;var el=root.querySelector('a.replay-button, .soundLink, [title="Replay Audio"]');if(el){el.click();}}function playUk(){clickAudio('uk');}function playUs(){clickAudio('us');}setTimeout(playUk,300);</script>''',
        'afmt': '''<div class="wrap back"><div class="title">答案</div><div><b>单词：</b>{{English}}</div><div><b>中文：</b>{{Chinese}}</div><div><b>分层：</b>{{Level}}</div><div><b>主题：</b>{{Topic}}</div><div><b>默认训练发音：</b>英式</div><hr><div><b>英文例句：</b>{{Example_EN}}</div><div><b>中文例句：</b>{{Example_ZH}}</div><div class="audio-row" style="margin-top:16px;"><button onclick="playUk()">按钮1：英式</button><button onclick="playUs()">按钮2：美式</button></div></div><div id="uk" style="display:none;">{{Audio_UK}}</div><div id="us" style="display:none;">{{Audio_US}}</div><script>function clickAudio(id){var root=document.getElementById(id);if(!root)return;var el=root.querySelector('a.replay-button, .soundLink, [title="Replay Audio"]');if(el){el.click();}}function playUk(){clickAudio('uk');}function playUs(){clickAudio('us');}</script>'''
    }],
    css='''.card { font-family: Arial, sans-serif; font-size: 20px; color: #111; background: #fff; } .wrap { line-height: 1.7; } .title { font-size: 28px; font-weight: 700; margin-bottom: 12px; } .sub, .help { color: #666; font-size: 15px; } .audio-row { display:flex; gap:10px; margin:16px 0; } button { font-size:16px; padding:8px 12px; border-radius:8px; border:1px solid #bbb; background:#f7f7f7; } hr { margin:14px 0; }'''
)

deck = genanki.Deck(DECK_ID, DECK_NAME)
media_files = []
for item in items:
    media_files.append(str(MEDIA / item['audio_uk_file']))
    media_files.append(str(MEDIA / item['audio_us_file']))
    note = genanki.Note(model=model, fields=[item['English'], item['Chinese'], item['Audio_UK'], item['Audio_US'], item['Example_EN'], item['Example_ZH'], item['Level'], item['Topic'], item['Source']], tags=['smf','dictation_full'])
    deck.add_note(note)

pkg = genanki.Package(deck)
pkg.media_files = media_files
pkg.write_to_file(str(APKG_OUT))

README_OUT.write_text(f'''# SMF Dictation Full\n\n- 词数：{len(items)}\n- 默认自动播放：英式\n- 按钮1：英式\n- 按钮2：美式\n- 含中文释义、英中例句、双发音\n''', encoding='utf-8')
print(f'built full deck with {len(items)} cards')
