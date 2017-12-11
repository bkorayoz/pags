from whoosh.index import create_in
from whoosh.fields import *
#import datetime
import json
#import re
#import psycopg2 as dbapi2
import requests
#from flask import redirect, Blueprint
#from flask.helpers import url_for
#from flask import Flask
#from flask import render_template
#from flask import request
#from flask_login import UserMixin, LoginManager
#from passlib.apps import custom_app_context as pwd_context
#from flask import current_app
from whoosh.qparser import QueryParser
dsn = """user='vagrant' password='vagrant' host='localhost' port=5432 dbname='pags'"""

def fetch_requirements(title):
    r = requests.get("https://www.game-debate.com/game/api/list").json()

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    ix = create_in("gamelist", schema)
    writer = ix.writer()
    for game in r:
        writer.add_document(title=game['g_title'], path=u"/a",content=game['g_title'])
    writer.commit()
    with  ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(title)
        results = searcher.search(query)
        if results.is_empty():
            return False
        title = results[0]['title']
        game_dict = next((item for item in r if item['g_title'] == title), False)
        if game_dict is False:
            return False
        game_id = game_dict['g_id']

        game_page = requests.get("https://www.game-debate.com/games/index.php?g_id=" + game_id).text

        game_page = game_page.splitlines()
        requirements = {'Minimum':{'CPU':{},'GPU':{}},'Recommended':{'CPU':{},'GPU':{}}}

        minimum_cpu_line = [line for line in game_page if "Minimum processor requirement" in line]
        if len(minimum_cpu_line) != 0:
            minimum_intel_cpu_line = game_page[game_page.index(minimum_cpu_line[0])+3]
            split0 = minimum_intel_cpu_line.split('&cpu=', 1)
            split1 = split0[1].split('" title="', 1)
            minimum_intel_cpu = split1[0]

            minimum_amd_cpu_line = game_page[game_page.index(minimum_cpu_line[0])+5]
            split0 = minimum_amd_cpu_line.split('&cpu=', 1)
            split1 = split0[1].split('" title="', 1)
            minimum_amd_cpu = split1[0]

            if 'GHz' in minimum_intel_cpu or 'MHz' in minimum_intel_cpu:
                minimum_intel_cpu = minimum_intel_cpu.rsplit(' ', 1)[0]
            if 'GHz' in minimum_amd_cpu or 'MHz' in minimum_amd_cpu:
                minimum_amd_cpu = minimum_amd_cpu.rsplit(' ', 1)[0]

            requirements['Minimum']['CPU']['Intel'] = minimum_intel_cpu
            requirements['Minimum']['CPU']['AMD'] = minimum_amd_cpu

        recommended_cpu_line = [line for line in game_page if "Recommended processor requirement" in line]
        if len(recommended_cpu_line) != 0:
            recommended_intel_cpu_line = game_page[game_page.index(recommended_cpu_line[0])+3]
            split0 = recommended_intel_cpu_line.split('&cpu=', 1)
            split1 = split0[1].split('" title="', 1)
            recommended_intel_cpu = split1[0]

            recommended_amd_cpu_line = game_page[game_page.index(recommended_cpu_line[0])+5]
            split0 = recommended_amd_cpu_line.split('&cpu=', 1)
            split1 = split0[1].split('" title="', 1)
            recommended_amd_cpu = split1[0]

            if 'GHz' in recommended_intel_cpu or 'MHz' in recommended_intel_cpu:
                recommended_intel_cpu = recommended_intel_cpu.rsplit(' ', 1)[0]
            if 'GHz' in recommended_amd_cpu or 'MHz' in recommended_amd_cpu:
                recommended_amd_cpu = recommended_amd_cpu.rsplit(' ', 1)[0]

            requirements['Recommended']['CPU']['Intel'] = recommended_intel_cpu
            requirements['Recommended']['CPU']['AMD'] = recommended_amd_cpu

        minimum_gpu_line = [line for line in game_page if "Minimum graphic card requirement" in line]
        if len(minimum_gpu_line) != 0:
            minimum_nvidia_gpu_line = game_page[game_page.index(minimum_gpu_line[0])+3]
            split0 = minimum_nvidia_gpu_line.split('&graphics=', 1)
            split1 = split0[1].split('" title="', 1)
            minimum_nvidia_gpu = split1[0]

            minimum_amd_gpu_line = game_page[game_page.index(minimum_gpu_line[0])+5]
            split0 = minimum_amd_gpu_line.split('&graphics=', 1)
            split1 = split0[1].split('" title="', 1)
            minimum_amd_gpu = split1[0]

            if 'GB' in minimum_nvidia_gpu or 'MB' in minimum_nvidia_gpu:
                minimum_nvidia_gpu = minimum_nvidia_gpu.rsplit(' ', 1)[0]
            if 'GB' in minimum_amd_gpu or 'MB' in minimum_amd_gpu:
                minimum_amd_gpu = minimum_amd_gpu.rsplit(' ', 1)[0]

            requirements['Minimum']['GPU']['Nvidia'] = minimum_nvidia_gpu
            requirements['Minimum']['GPU']['AMD'] = minimum_amd_gpu

        recommended_gpu_line = [line for line in game_page if "Recommended graphic card requirement" in line]
        if len(recommended_gpu_line) != 0:
            recommended_nvidia_gpu_line = game_page[game_page.index(recommended_gpu_line[0])+3]
            split0 = recommended_nvidia_gpu_line.split('&graphics=', 1)
            split1 = split0[1].split('" title="', 1)
            recommended_nvidia_gpu = split1[0]

            recommended_amd_gpu_line = game_page[game_page.index(recommended_gpu_line[0])+5]
            split0 = recommended_amd_gpu_line.split('&graphics=', 1)
            split1 = split0[1].split('" title="', 1)
            recommended_amd_gpu = split1[0]

            if 'GB' in recommended_nvidia_gpu or 'MB' in recommended_nvidia_gpu:
                recommended_nvidia_gpu = recommended_nvidia_gpu.rsplit(' ', 1)[0]
            if 'GB' in recommended_amd_gpu or 'MB' in recommended_amd_gpu:
                recommended_amd_gpu = recommended_amd_gpu.rsplit(' ', 1)[0]

            requirements['Recommended']['GPU']['Nvidia'] = recommended_nvidia_gpu
            requirements['Recommended']['GPU']['AMD'] = recommended_amd_gpu

        minimum_ram_line = [line for line in game_page if "Minimum RAM Requirement" in line]
        if len(minimum_ram_line) != 0:
            split0 = minimum_ram_line[0].split('Minimum RAM Requirement">', 1)
            split1 = split0[1].split('</span>', 1)
            minimum_ram = split1[0]

            requirements['Minimum']['RAM'] = minimum_ram

        recommended_ram_line = [line for line in game_page if "Recommended RAM Requirement" in line]
        if len(recommended_ram_line) != 0:
            split0 = recommended_ram_line[0].split('Recommended RAM Requirement">', 1)
            split1 = split0[1].split('</span>', 1)
            recommended_ram = split1[0]

            requirements['Recommended']['RAM'] = recommended_ram




    # Uncomment to return json string
    #    return json.dumps(requirements, indent=2)
        return requirements
