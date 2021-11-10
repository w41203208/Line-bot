import json
import pathlib
DIR = str(pathlib.Path(__file__).parent.absolute())

print(DIR)

#def write_json_file(json_data,filename, use_pwd_path = False):
#    fname = filename if use_pwd_path else DIR+"/"+filename
#    with(open(fname,"w", encoding="utf-8")) as sw:
#        json.dump(json_data,sw)