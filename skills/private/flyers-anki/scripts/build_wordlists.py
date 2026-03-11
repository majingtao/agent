from pathlib import Path
import csv, json, re, html

ROOT = Path(__file__).resolve().parents[1]
TXT = ROOT / 'source' / 'flyers_2025_wordlist.txt'
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)

TITLE = 'Pre A1 Starters, A1 Movers and A2 Flyers alphabetic vocabulary list'
END_TITLE = 'Pre A1 Starters, A1 Movers and\nA2 Flyers grammatical vocabulary list'
SKIP = {
    TITLE,
    'Grammatical key','adjective','adverb','conjunction','determiner','discourse marker','exclamation',
    'interrogative','noun','possessive','preposition','pronoun','verb',
    'adj','adv','conj','det','dis','excl','int','n','poss','prep','pron','v',
    'S','M','F'
}
SPECIAL_OFFICIAL = {
    'Betty','David','Emma','Frank','George','Harry','Helen','Holly','Katy','Michael','Oliver','Richard','Robert','Sarah','Sophia','William',
    'a hundred','a thousand','a million','zero','21st','22nd','23rd','24th','25th','26th','27th','28th','29th','30th','31st'
}
HIGH_FREQ_TOPICS = {
    'time': {'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','January','February','March','April','May','June','July','August','September','October','November','December','morning','afternoon','evening','night','today','tomorrow','yesterday','time','timetable','hour','minute','week','month','year','a.m. (for time)','p.m. (for time)','quarter','midday','midnight'},
    'school': {'book','bookcase','bookshop','class','classroom','computer','dictionary','eraser (UK rubber)','homework','language','music','notebook','page','paper','pen','pencil','question','read','school','story','study','subject','teacher','telephone','timetable','word','write'},
    'food': {'apple','banana','bean','bread','burger','cake','candy (UK sweet(s))','carrot','cheese','chicken','chips (US fries)','chocolate','coconut','cookie (UK biscuit)','cereal','grape','honey','ice cream','jam','juice','lemonade','meal','milk','onion','orange','pear','pepper','pizza','potato','rice','salt','sandwich','sausage','soup','strawberry','sugar','tea','water','watermelon','yoghurt','biscuit (US cookie)'},
    'animals': {'animal','bear','bee','bird','butterfly','camel','cat','chicken','cow','crocodile','dog','dolphin','donkey','duck','eagle','elephant','fish','frog','giraffe','goat','hippo','horse','insect','kangaroo','kitten','lion','lizard','monkey','mouse','octopus','panda','parrot','penguin','puppy','rabbit','shark','sheep','snake','spider','swan','tiger','tortoise','whale','zebra','zoo'},
    'places': {'airport','apartment (UK flat)','bank','beach','bridge','bus station','bus stop','café','car park','castle','chemist(\'s)','cinema','city','country','farm','garden','hospital','hotel','house','kitchen','library','market','museum','park','playground','police station','post office','railway','restaurant','road','room','school','shop','street','supermarket','town','university'},
    'actions': {'answer','ask','buy','carry','catch','clean','close','come','cook','count','draw','drink','drive','eat','find','finish','give','go','help','jump','learn','listen','look','make','open','paint','play','put','read','ride','run','say','see','show','sing','sit','sleep','smile','spell','swim','talk','tell','think','throw','walk','watch','write','find out','go out','look after','look like','turn off','turn on'},
}

MEDIUM_HIGH_FREQ = {
    'afraid','again','angry','answer','beautiful','behind','best','better','big','black','blue','boat','body','bottom','box','boy','brown','chair','classmate','clothes','cloud','cold','colour (US color)','countryside','cross','day','dress','ear','easy','egg','English','face','family','farm','field','film (US movie)','flower','food','friend','funny','game','garden','girl','glad','good','grandparent','green','grey (US gray)','ground','happy','hat','head','here','home','house','inside','jacket','kitchen','know','lake','leg','lesson','like','line','live','long','man','many','monster','morning','mother','mouth','name','new','next','old','park','part','party','person','phone','pink','plane','playground','pretty','rain','red','right','river','room','sad','sea','shoe','short','sister','small','snow','sports centre (US center)','star','street','sun','table','tail','tall','teacher','television/TV','test','thing','tired','train','tree','trousers','ugly','wall','water','white','window','woman/women','yellow','young'
}

TRICKY_EXTRA = {'because','beautiful','blanket','bracelet','calendar','chemist(\'s)','competition','conversation','delicious','environment','everywhere','flashlight (UK torch)','frightening','information','instrument','interested','interesting','journalist','kilometre (US kilometer)','medicine','motorway','programme (US program)','restaurant','scissors','skyscraper','spaceship','strawberry','straight on','sunglasses','suitcase','theatre (US theater)','through','timetable','umbrella','uniform','university','wonderful','yoghurt'}


def norm(s: str) -> str:
    return s.replace('’', "'").replace('\ufeff', '').strip()


def dedupe(seq):
    seen = set(); out = []
    for x in seq:
        k = x.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(x)
    return out


def parse_combined_list(text: str):
    first = text.find(TITLE)
    start = text.find(TITLE, first + 1)
    end = text.find(END_TITLE, start)
    section = text[start:end]
    lines = [norm(ln) for ln in section.splitlines()]
    out = []
    i = 0
    while i < len(lines):
        s = lines[i]
        if not s or s in SKIP or re.fullmatch(r'[A-Z]', s) or re.fullmatch(r'\d+', s):
            i += 1; continue
        cur = s
        while i + 1 < len(lines):
            if re.search(r'\s+[SMF](\s*\+\s*[SMF])*$', cur):
                break
            nxt = lines[i + 1]
            if not nxt or nxt in SKIP or re.fullmatch(r'[A-Z]', nxt) or re.fullmatch(r'\d+', nxt):
                break
            cur += ' ' + nxt
            i += 1
        m = re.search(r'\s+([SMF](\s*\+\s*[SMF])*)$', cur)
        if m:
            term = norm(cur[:m.start()])
            term = re.sub(r'\s+(adj|adv|conj|det|dis|excl|int|n|poss|prep|pron|v)(\s*\+\s*(adj|adv|conj|det|dis|excl|int|n|poss|prep|pron|v))*$','', term).strip()
            if term:
                out.append(term)
        i += 1
    out.extend(sorted(SPECIAL_OFFICIAL))
    out = [x for x in out if x not in {'Combined lists'}]
    return dedupe(out)


def phrase_type(word):
    return 'phrase' if ' ' in word else 'word'


def special_type(word):
    if word in SPECIAL_OFFICIAL:
        if re.fullmatch(r'\d+(st|nd|rd|th)', word) or word in {'a hundred','a thousand','a million','zero'}:
            return 'number'
        return 'official_write'
    return ''


def official_write(word):
    return 'yes' if word in SPECIAL_OFFICIAL else 'no'


def topic(word):
    for topic_name, vocab in HIGH_FREQ_TOPICS.items():
        if word in vocab:
            return topic_name
    return 'general'


def write_priority(word):
    if official_write(word) == 'yes':
        return 'must_write'
    if word in TRICKY_EXTRA:
        return 'tricky'
    if word in set().union(*HIGH_FREQ_TOPICS.values()):
        return 'core'
    if phrase_type(word) == 'phrase' or len(word) >= 11 or any(ch in word for ch in ['(', ')', '/', '-']):
        return 'tricky'
    return 'extended'


def training_include(word):
    if official_write(word) == 'yes':
        return 'yes'
    if word in TRICKY_EXTRA:
        return 'yes'
    if word in set().union(*HIGH_FREQ_TOPICS.values()):
        return 'yes'
    if word in MEDIUM_HIGH_FREQ:
        return 'yes'
    if phrase_type(word) == 'word' and len(word) <= 3 and word[0].islower():
        return 'yes'
    return 'no'


def level_label(priority):
    return {
        'must_write': '必写（must_write）',
        'core': '核心（core）',
        'extended': '扩展（extended）',
        'tricky': '易错（tricky）',
    }[priority]


def rows_from_words(words):
    rows = []
    for w in words:
        pri = write_priority(w)
        rows.append({
            'word': w,
            'phrase_type': phrase_type(w),
            'range': 'Pre A1 Starters + A1 Movers + A2 Flyers',
            'official_write': official_write(w),
            'training_include': training_include(w),
            'write_priority': pri,
            'level_label': level_label(pri),
            'topic': topic(w),
            'special_type': special_type(w),
            'source': 'Cambridge combined alphabetic vocabulary list (2025 PDF)',
        })
    return rows


def save_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def make_html(title, subtitle, rows, count_label):
    parts = [f'''<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>body{{font-family:Arial;padding:24px}} h1{{font-size:28px;margin:0 0 6px}} .sub{{color:#555;margin-bottom:10px}} .meta{{padding:10px 12px;background:#f4f6fb;border-radius:8px;margin:12px 0 18px}} table{{border-collapse:collapse;width:100%;font-size:12px}} th,td{{border:1px solid #ddd;padding:6px 8px;text-align:left;vertical-align:top}} th{{background:#eef2f7}}</style>
</head><body><h1>{html.escape(title)}</h1><div class="sub">{html.escape(subtitle)}</div><div class="meta"><b>{html.escape(count_label)}</b>：{len(rows)}</div><table><thead><tr><th>#</th><th>word</th><th>phrase_type</th><th>official_write</th><th>training_include</th><th>write_priority</th><th>topic</th></tr></thead><tbody>''']
    for i, r in enumerate(rows, 1):
        parts.append(f"<tr><td>{i}</td><td>{html.escape(r['word'])}</td><td>{r['phrase_type']}</td><td>{r['official_write']}</td><td>{r['training_include']}</td><td>{html.escape(r['level_label'])}</td><td>{r['topic']}</td></tr>")
    parts.append('</tbody></table></body></html>')
    return ''.join(parts)

text = TXT.read_text(encoding='utf-8')
words = parse_combined_list(text)
full_rows = rows_from_words(words)
selected_rows = [r for r in full_rows if r['training_include'] == 'yes' or r['official_write'] == 'yes']

save_csv(DATA / 'smf_full_vocab.csv', full_rows)
save_csv(DATA / 'smf_selected_dictation.csv', selected_rows)
summary = {
    'full_count': len(full_rows),
    'selected_count': len(selected_rows),
    'official_write_count': sum(1 for r in full_rows if r['official_write'] == 'yes'),
}
(DATA / 'wordlist_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
(DATA / 'smf_full_vocab_review.html').write_text(make_html('Starters + Movers + Flyers 全量词库初稿', '仅取 combined alphabetic vocabulary list 这一部分。', full_rows, '全量词数'), encoding='utf-8')
(DATA / 'smf_selected_dictation_review.html').write_text(make_html('Starters + Movers + Flyers 听写筛选词库初稿', '基于 combined alphabetic vocabulary list，在官方明确项基础上补考试高频与易错词，目标约 400。', selected_rows, '筛选词数'), encoding='utf-8')
print(summary)
