from trilium_py.client import ETAPI
from env import trilium_server_url, trilium_token
import os
import json

ea = ETAPI(trilium_server_url, trilium_token)
CACHE_FILE = "note_cache.json"
count = 0


def collect_notes(note_id, note_map, parent_map, parent_id=None):
    global count
    count += 1
    print(count, note_id)
    note = ea.get_note(note_id)
    note_map[note_id] = note

    if parent_id:
        parent_map[note_id] = parent_id

    for child_id in note.get("childNoteIds", []):
        collect_notes(child_id, note_map, parent_map, note_id)


def save_cache(note_map, parent_map):
    with open(CACHE_FILE, "w") as f:
        json.dump({"note_map": note_map, "parent_map": parent_map}, f)


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)
            return data["note_map"], data["parent_map"]
    return {}, {}


def get_all_notes(note_id: str):
    note = ea.get_note(note_id)
    print(note["title"])
    children = []

    for child_id in note.get("childNoteIds", []):
        children.append(get_all_notes(child_id))

    return [note["title"], children]


def get_note_path(note_id, note_map, parent_map):
    path = []

    current_id = note_id
    while current_id in note_map:
        note = note_map[current_id]
        path.append(note["title"])
        current_id = parent_map.get(current_id)
        if current_id is None:
            break

    return list(reversed(path))


def search(keyword: str, refresh=False):
    note_map, parent_map = load_cache()

    if refresh or not note_map:
        root = ea.get_note("root")
        note_map["root"] = root

        for child_id in root.get("childNoteIds", []):
            if child_id == "_hidden":
                continue
            collect_notes(child_id, note_map, parent_map, "root")

        save_cache(note_map, parent_map)

    res = ea.search_note(search=keyword)

    results = []

    for x in res["results"]:
        note_id = x["noteId"]
        title = x["title"]
        path = get_note_path(note_id, note_map, parent_map)
        results.append({"title": title, "path": " > ".join(path)})

    return results
