from pathlib import Path
import csv
import genanki

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'data' / 'smf_selected_dictation.csv'
OUT = ROOT / 'out'
OUT.mkdir(exist_ok=True)
CSV_OUT = OUT / 'smf_dictation_template.csv'
APKG_OUT = OUT / 'SMF_Dictation_Template.apkg'
README_OUT = OUT / 'SMF_Dictation_Template_README.md'

MODEL_ID = 25030901
DECK_ID = 25030902
MODEL_NAME = 'SMF Dictation Template'
DECK_NAME = 'SMF::Dictation Template'


def build_csv():
    with SRC.open(encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    out_rows = []
    for r in rows:
        out_rows.append({
            'English': r['word'],
            'Chinese': '',
            'Audio_UK': '',
            'Audio_US': '',
            'Example_EN': '',
            'Example_ZH': '',
            'Level': r['level_label'],
            'Topic': r['topic'],
            'Source': r['source'],
        })

    with CSV_OUT.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)
    return out_rows


def build_apkg(rows):
    model = genanki.Model(
        MODEL_ID,
        MODEL_NAME,
        fields=[
            {'name': 'English'},
            {'name': 'Chinese'},
            {'name': 'Audio_UK'},
            {'name': 'Audio_US'},
            {'name': 'Example_EN'},
            {'name': 'Example_ZH'},
            {'name': 'Level'},
            {'name': 'Topic'},
            {'name': 'Source'},
        ],
        templates=[{
            'name': 'Dictation Card',
            'qfmt': '''<div class="wrap">
  <div class="title">听写卡</div>
  <div class="sub">默认自动播放英式；按钮1英式，按钮2美式。</div>
  <div class="audio-row">
    <button onclick="playUk()">按钮1：英式</button>
    <button onclick="playUs()">按钮2：美式</button>
  </div>
  <div class="help">正面不显示中文提示，不显示答案。</div>
</div>

<div id="uk" style="display:none;">{{Audio_UK}}</div>
<div id="us" style="display:none;">{{Audio_US}}</div>

<script>
function clickAudio(containerId) {
  var root = document.getElementById(containerId);
  if (!root) return;
  var el = root.querySelector('a.replay-button, .soundLink, [title="Replay Audio"]');
  if (el) { el.click(); }
}
function playUk(){ clickAudio('uk'); }
function playUs(){ clickAudio('us'); }
setTimeout(playUk, 300);
</script>''',
            'afmt': '''<div class="wrap back">
  <div class="title">答案</div>
  <div><b>单词：</b>{{English}}</div>
  <div><b>中文：</b>{{Chinese}}</div>
  <div><b>分层：</b>{{Level}}</div>
  <div><b>主题：</b>{{Topic}}</div>
  <div><b>默认训练发音：</b>英式</div>
  <hr>
  <div><b>英文例句：</b>{{Example_EN}}</div>
  <div><b>中文例句：</b>{{Example_ZH}}</div>
  <div class="audio-row" style="margin-top:16px;">
    <button onclick="playUk()">按钮1：英式</button>
    <button onclick="playUs()">按钮2：美式</button>
  </div>
</div>

<div id="uk" style="display:none;">{{Audio_UK}}</div>
<div id="us" style="display:none;">{{Audio_US}}</div>

<script>
function clickAudio(containerId) {
  var root = document.getElementById(containerId);
  if (!root) return;
  var el = root.querySelector('a.replay-button, .soundLink, [title="Replay Audio"]');
  if (el) { el.click(); }
}
function playUk(){ clickAudio('uk'); }
function playUs(){ clickAudio('us'); }
</script>'''
        }],
        css='''.card { font-family: Arial, sans-serif; font-size: 20px; color: #111; background: #fff; }
.wrap { line-height: 1.7; }
.title { font-size: 28px; font-weight: 700; margin-bottom: 12px; }
.sub, .help { color: #666; font-size: 15px; }
.audio-row { display: flex; gap: 10px; margin: 16px 0; }
button { font-size: 16px; padding: 8px 12px; border-radius: 8px; border: 1px solid #bbb; background: #f7f7f7; }
hr { margin: 14px 0; }
'''
    )

    deck = genanki.Deck(DECK_ID, DECK_NAME)
    for r in rows:
        note = genanki.Note(
            model=model,
            fields=[
                r['English'], r['Chinese'], r['Audio_UK'], r['Audio_US'],
                r['Example_EN'], r['Example_ZH'], r['Level'], r['Topic'], r['Source']
            ],
            tags=['smf', 'dictation_template']
        )
        deck.add_note(note)

    package = genanki.Package(deck)
    package.write_to_file(str(APKG_OUT))


def build_readme(rows):
    README_OUT.write_text(f'''# SMF Dictation Template

## 文件

- `smf_dictation_template.csv`：可继续补中文、音频、例句的模板底稿
- `SMF_Dictation_Template.apkg`：Anki 模板牌组

## 当前基线

- 来源词库：`smf_selected_dictation.csv`
- 词数：{len(rows)}

## 字段

- English
- Chinese
- Audio_UK
- Audio_US
- Example_EN
- Example_ZH
- Level
- Topic
- Source

## 说明

- 当前是模板底稿，不含最终中文、双发音音频与例句内容
- 用于后续继续填充并生成正式听写牌组
''', encoding='utf-8')


rows = build_csv()
build_apkg(rows)
build_readme(rows)
print(f'built {len(rows)} rows')
