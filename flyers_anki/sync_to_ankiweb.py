from pathlib import Path
from anki.collection import Collection
from anki import import_export_pb2

COL_PATH = Path('/root/.openclaw/workspace/flyers_anki/ankiweb_sync/collection.anki2')
MEDIA_PATH = COL_PATH.parent / 'collection.media'
PKG_PATH = Path('/root/.openclaw/workspace/flyers_anki/out/Flyers_Paper_Dictation_TTS.apkg')
USERNAME = 'xiaoxiao520@gmail.com'
PASSWORD = '5Mjtadmin'

COL_PATH.parent.mkdir(parents=True, exist_ok=True)

print('opening collection:', COL_PATH)
col = Collection(str(COL_PATH))
try:
    print('importing package...')
    req = import_export_pb2.ImportAnkiPackageRequest(
        package_path=str(PKG_PATH),
        options=import_export_pb2.ImportAnkiPackageOptions(
            merge_notetypes=False,
            with_scheduling=True,
            with_deck_configs=True,
        ),
    )
    log = col.import_anki_package(req)
    print('import done')
    print(log)

    print('logging in...')
    auth = col.sync_login(USERNAME, PASSWORD, None)
    print('sync auth ok')

    print('checking sync status...')
    status = col.sync_status(auth)
    print(status)

    print('performing full upload...')
    col.full_upload_or_download(auth=auth, server_usn=None, upload=True)
    print('full upload done')

    print('syncing media...')
    col.sync_media(auth)
    print('media sync done')
finally:
    col.close()
    print('collection closed')
