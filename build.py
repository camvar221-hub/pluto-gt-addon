import re
metas=[]
catalog=[]
count=0
with open('pluto.m3u', 'r', encoding='utf-8', errors='ignore') as f:
    lines=f.readlines()
i=0
while i < len(lines):
  line=lines[i].strip()
  if line.startswith('#EXTINF'):
    name_match=re.search(r',(.+)$', line)
    name=name_match.group(1).strip() if name_match else f"Canal {count}"
    logo_match=re.search(r'tvg-logo="([^"]+)"', line)
    logo=logo_match.group(1) if logo_match else ""
    id_match=re.search(r'tvg-id="([^"]+)"', line)
    tvg_id=id_match.group(1) if id_match else f"ch{count}"
    # next line is URL
    if i+1 < len(lines):
      url=lines[i+1].strip()
      if url.startswith('http'):
        pid=f"pluto_{tvg_id.replace('.','_')}_{count}"
        pid=re.sub(r'[^a-zA-Z0-9_]', '_', pid)
        # limit to 40 channels para que no sea gigante
        if count < 40:
          metas.append((pid,name,logo,url))
        count+=1
  i+=1

# manifest
import json, os
manifest={
  "id": "com.camvar.plutogt.real",
  "version": "3.0.0",
  "name": "Pluto TV GT - FINAL FIX",
  "description": "40 canales Pluto TV USA con links firmados - funciona en GT",
  "resources": ["catalog","meta","stream"],
  "types": ["tv"],
  "catalogs": [{"type":"tv","id":"pluto_gt","name":"Pluto TV"}],
  "idPrefixes": ["pluto_"]
}
with open('manifest.json','w') as out:
  json.dump(manifest,out,indent=2)

catalog_metas=[]
for pid,name,logo,url in metas:
  catalog_metas.append({
    "id": pid,
    "type": "tv",
    "name": name,
    "poster": logo,
    "posterShape": "landscape"
  })
  meta_obj={
    "meta": {
      "id": pid,
      "type": "tv",
      "name": name,
      "poster": logo,
      "logo": logo,
      "description": f"{name} - En vivo Pluto TV",
      "videos": [{"id": f"{pid}:1", "title": f"En Vivo - {name}", "released": "2024-01-01"}]
    }
  }
  stream_obj={
    "streams": [{
      "name": "Pluto TV",
      "title": f"{name} - En Vivo",
      "url": url,
      "behaviorHints": {"notWebReady": False}
    }]
  }
  os.makedirs('meta/tv', exist_ok=True)
  os.makedirs('stream/tv', exist_ok=True)
  with open(f'meta/tv/{pid}.json','w') as mf:
    json.dump(meta_obj,mf)
  with open(f'stream/tv/{pid}.json','w') as sf:
    json.dump(stream_obj,sf)

with open('catalog/tv/pluto_gt.json','w') as cf:
  json.dump({"metas": catalog_metas}, cf)

print(f"Built {len(metas)} channels")
