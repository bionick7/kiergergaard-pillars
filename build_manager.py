import yaml, json
import os, sys
import zipfile
import getopt


IGNORE_KEYS = (
    "PROGRESS_artw",
    "PROGRESS_flavour",
    "PROGRESS_gameplay",
    "PROGRESS_playtest",
)

ACCEPTABLE_TAGS = (
    "tg_burn",
    "tg_cone",
    "tg_blast",
    "tg_burst",
    "tg_accurate",
    "tg_arcing",
    "tg_ap",
    "tg_inaccurate",
    "tg_knockback",
    "tg_loading",
    "tg_ordnance",
    "tg_overkill",
    "tg_overshield",
    "tg_reliable",
    "tg_seeking",
    "tg_smart",
    "tg_threat",
    "tg_thrown",
    "tg_turn",
    "tg_round",
    "tg_ai",
    "tg_danger_zone",
    "tg_deployable",
    "tg_drone",
    "tg_full_action",
    "tg_grenade",
    "tg_heat_self",
    "tg_limited",
    "tg_mine",
    "tg_mod",
    "tg_protocol",
    "tg_quick_action",
    "tg_reaction",
    "tg_shield",
    "tg_unique",
    "tg_archaic",
    "tg_personal_armor",
    "tg_gear",
    "tg_sidearm",
    "tg_invade",
    "tg_quick_tech",
    "tg_full_tech",
    "tg_free_action",
    "tg_range",
    "tg_modded",
    "tg_resistance",
    "tg_exotic",
    "tg_recharge",
    "tg_unlimited",
    "tg_indestructible",
    "tg_invulnerable",
    "tg_invisible",
    "tg_resistall",
    "tg_set_max_uses",
    "tg_set_damage_type",
    "tg_set_damage_value",
    "tg_no_cascade",

    "tg_laser",
)
ALL_FILES = (
    "core_bonuses",
    "frames",
    "manufacturers",
    "mods",
    "pilot_gear",
    "systems",
    "tags",
    "talents",
    "weapons",
    "lcp_manifest"
)

def corrected(v):
    if isinstance(v, str):
        v = v.replace("\u2019", "'")
        v = v.replace("\u201C", "<<")
        v = v.replace("\u201D", ">>")
    if isinstance(v, dict):
        for k, v2 in v.items():
            v[k] = corrected(v2)
    if isinstance(v, list):
        for i, v2 in enumerate(v):
            v[i] = corrected(v2)
    return v


def uncorrected(v):
    if isinstance(v, str):
        pass
    if isinstance(v, dict):
        for k, v2 in v.items():
            v[k] = uncorrected(v2)
    if isinstance(v, list):
        for i, v2 in enumerate(v):
            v[i] = uncorrected(v2)
    return v


def keys_ignored(v):
    if isinstance(v, dict):
        for k in IGNORE_KEYS:
            if k in v:
                del v[k]
    if isinstance(v, list):
        for i, v2 in enumerate(v):
            v[i] = keys_ignored(v2)
    return v


def check_tags(v):
    if isinstance(v, dict):
        for k, v2 in v.items():
            if k == "id" and isinstance(v2, str) and v2.startswith("tg_"):
                if v2 not in ACCEPTABLE_TAGS:
                    print(f"Unacceptable tag: '{v2}'")
            check_tags(v2)
    if isinstance(v, list):
        for i, v2 in enumerate(v):
            check_tags(v2)


def test_all():
    import dictdiffer
    for folder in ("editable_content", "editable_content_Buona_Sera_ONRYO"):
        for file in ALL_FILES:
            print("Test", file)
            file_path_yaml = os.path.join(folder, file + ".yaml")
            if not os.path.exists(file_path_yaml):
                print(f"File does not exist '{file_path_yaml}'")
                return
            with open(file_path_yaml, "r") as f:
                data = yaml.full_load(f)

            data = uncorrected(data)
            file_path_json = os.path.join("content", file + ".json")
            with open(file_path_json, "r") as f:
                data2 = json.load(f)
                for i in dictdiffer.diff(data, data2):
                    print(i, "\n")


class Module:
    def __init__(self, p_name, p_json_folder, p_yaml_folder) -> None:
        self.name = p_name
        self.json_folder = p_json_folder
        self.yaml_folder = p_yaml_folder

    def yaml2json(self, domain: str, apply_reverse_corrections: bool=False):
        folder_path = os.path.join(self.yaml_folder, domain)
        file_list = []
        single_file = False
        if os.path.exists(folder_path + ".yaml"):
            # Single file
            file_list = [folder_path + ".yaml"]
            single_file = True
        elif os.path.exists(folder_path):
            for fp in os.listdir(folder_path):
                # Ignore subfolders
                if os.path.isfile(os.path.join(folder_path, fp)):
                    file_list.append(os.path.join(folder_path, fp))
        else:
            print(f"Folder or File does not exist '{folder_path}'")
            return
        
        final_data = []
        for fp in file_list:
            #TODO: ignore '# IS AUTOGEN' and actually read all in
            with open(fp, "r") as f:
                if f.readline().startswith("# IS AUTOGEN"):
                    continue
                f.seek(0)
                data = yaml.full_load(f)

            if apply_reverse_corrections:
                data = uncorrected(data)

            check_tags(data)
            data = keys_ignored(data)
            final_data.append(data)

        if single_file:
            final_data = final_data[0]

        file_path_json = os.path.join(self.json_folder, domain + ".json")
        with open(file_path_json, "w") as f:
            json.dump(final_data, f, indent="  ")


    def json2yaml(self, domain: str):
        file_path_json = os.path.join(self.json_folder, domain + ".json")
        if not os.path.exists(file_path_json):
            print(f"File does not exist '{file_path_json}'")
            return
        with open(file_path_json, "r") as f:
            data = json.load(f)

        data = corrected(data)

        if isinstance(data, list) and len(data) > 0 and "name" in data[0]:
            dir_path = os.path.join(self.yaml_folder, domain)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

            for item in data:
                identifier = item["name"].upper()
                del item["name"]
                file_path_yaml = os.path.join(dir_path, identifier + ".yaml")
                item["PROGRESS_gameplay"] = True
                item["PROGRESS_flavour"] = False
                item["PROGRESS_artw"] = False
                item["PROGRESS_playtest"] = False
                with open(file_path_yaml, "w") as f:
                    yaml.dump(item, f)
        else:
            file_path_yaml = os.path.join(self.yaml_folder, domain + ".yaml")
            with open(file_path_yaml, "w") as f:
                yaml.dump(data, f)


    def json2yamlall(self):
        for file in ALL_FILES:
            self.json2yaml(file)


    def yaml2jsonall(self):
        for file in ALL_FILES:
            self.yaml2json(file)

    def zip_all(self):
        with zipfile.ZipFile(self.name + ".lcp", mode="w") as archive:
            for file in ALL_FILES:
                file_path_json = os.path.join(self.json_folder, file + ".json")
                if os.path.exists(file_path_json):
                    archive.write(file_path_json, file + ".json")

    def build_lcp(self):
        self.yaml2jsonall()
        self.zip_all()
        #os.system("typst compile --font-path ./fonts lcp2pdf.typ Manual.pdf")


def main(argv):
    if argv[0] == "1":
        mod = Module("rosergaard-pillars", "content", "editable_content")
    elif argv[0] == "2":
        mod = Module("rosergaard-Buona-Sera-ONRYO", "content_Buona_Sera_ONRYO", "editable_content_Buona_Sera_ONRYO")
    else:
        return

    try:
        opts, args = getopt.getopt(argv[1:], "tbzyjY:J:", ["test", "build", "2yaml", "2json", "single2yaml=", "single2json="])
    except:
      print('build_manager.py -t -b -z -y -j -Y <file> -J <file>')
      sys.exit(2)

    if len(opts) == 0:
        mod.build_lcp()

    for opt, arg in opts:
        if opt == '-t':
            test_all()
        elif opt == '-z':
            mod.zip_all()
        elif opt == '-b':
            mod.build_lcp()
        elif opt == '-j':
            mod.yaml2jsonall()
        elif opt == '-y':
            mod.json2yamlall()
        elif opt == '-J':
            mod.yaml2json(arg)
        elif opt == '-Y':
            mod.json2yaml(arg)



if __name__ == "__main__":    
    main(sys.argv[1:])