import os
import json

async def get_theme(name, type):
    f = open("nana/assistant/theme/theme.json")
    theme = json.load(f)
    f.close()
    return theme["Nana-Theme"][name][type]