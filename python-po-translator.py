#!/usr/env/bin python
from googletrans import Translator, LANGCODES
import polib
import asyncio

async def translate_text(text: str):
    translator = Translator(service_urls=[
        'translate.google.com'
        ])
    result = translator.translate(text, dest='en', src="fr")
    return await result.text

async def do_translate():
    translator = Translator()
    #source file
    po = polib.pofile('./locale/en/LC_MESSAGES/django.po') 
    for entry in po.untranslated_entries():
        print("Entry : ", entry.msgid)
        result = await translator.translate(entry.msgid, dest='en', src="fr")
        new_entry = polib.POEntry(
        msgid=entry.msgid,
        msgstr=result.text,
        occurrences=entry.occurrences )
        po.append(new_entry)
        print("Entry Done")

    #save as new file
    po.save('newDjango.po')
#deal with duplicates later 
if __name__ == "__main__":
    asyncio.run(do_translate())