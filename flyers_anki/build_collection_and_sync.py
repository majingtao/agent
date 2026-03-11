from pathlib import Path
import json, shutil
from anki.collection import Collection
from anki.notes import Note

ROOT = Path('/root/.openclaw/workspace/flyers_anki')
ITEMS = json.loads((ROOT / 'out' / 'flyers_words.json').read_text(encoding='utf-8'))
SRC_MEDIA = ROOT / 'out' / 'media'
WORK = ROOT / 'ankiweb_manual_sync'
COL_PATH = WORK / 'collection.anki2'
USERNAME = 'xiaoxiao520@gmail.com'
PASSWORD = '5Mjtadmin'
DECK_NAME = 'Flyers::Paper Dictation (TTS) v2'
MODEL_NAME = 'Flyers Paper Dictation Model v2'

if WORK.exists():
    shutil.rmtree(WORK)
WORK.mkdir(parents=True, exist_ok=True)

col = Collection(str(COL_PATH))
try:
    # model
    m = col.models.by_name(MODEL_NAME)
    if not m:
        m = col.models.new(MODEL_NAME)
        for field_name in ['English', 'Chinese', 'Audio', 'Level', 'Source']:
            col.models.add_field(m, col.models.new_field(field_name))
        t = col.models.new_template('Paper Dictation')
        t['qfmt'] = '''<div style="font-family: Arial; font-size: 20px; text-align:center; line-height:1.6;">
<div style="font-size:28px; font-weight:700; margin-bottom:12px;">听写卡</div>
<div style="margin-bottom:14px;">先听，再让孩子在纸上写。</div>
<div style="font-size:22px; margin:14px 0;">{{Audio}}</div>
<div style="color:#666; font-size:16px;">写完后翻面，由家长手动判断对错。</div>
</div>'''
        t['afmt'] = '''<div style="font-family: Arial; font-size: 20px; line-height:1.7;">
<div style="font-size:28px; font-weight:700; text-align:center; margin-bottom:14px;">答案</div>
<div><b>单词：</b>{{English}}</div>
<div><b>中文：</b>{{Chinese}}</div>
<div><b>分层：</b>{{Level}}</div>
<div><b>音频：</b>{{Audio}}</div>
<div style="margin-top:14px; color:#666; font-size:15px;">建议：写对点 Good；模糊点 Hard；写错点 Again。</div>
</div>'''
        col.models.add_template(m, t)
        m['css'] = '.card { background:#fff; color:#111; }'
        col.models.add(m)

    did = col.decks.id(DECK_NAME)
    model = col.models.by_name(MODEL_NAME)
    media_name_map = {}

    for idx, item in enumerate(ITEMS, start=1):
        audio_file = item['audio_file']
        src = SRC_MEDIA / audio_file
        if audio_file not in media_name_map:
            media_name_map[audio_file] = col.media.add_file(str(src))
        synced_name = media_name_map[audio_file]

        n = Note(col, model)
        n['English'] = item['english']
        n['Chinese'] = item['chinese']
        n['Audio'] = f"[sound:{synced_name}]"
        n['Level'] = item['level']
        n['Source'] = item['source']
        n.tags = ['flyers', item['level']]
        col.add_note(n, did)
        if idx % 100 == 0:
            print(f'added {idx}/{len(ITEMS)}')

    print('notes total:', col.note_count())
    print('login...')
    auth = col.sync_login(USERNAME, PASSWORD, None)
    out = col.sync_collection(auth, False)
    print('sync_collection:', out)
    if out.new_endpoint:
        auth.endpoint = out.new_endpoint

    print('full upload...')
    col.close_for_full_sync()
    col.full_upload_or_download(auth=auth, server_usn=out.server_media_usn, upload=True)
    print('full upload done')

    col.reopen(after_full_sync=True)
    col.media.force_resync()
    print('media sync...')
    col.sync_media(auth)
    print('media sync done')
finally:
    col.close()
    print('closed')
