import yaml, json
import os, sys
import zipfile
import getopt

ALL_FILES = (
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


def test_all():
    import dictdiffer
    for file in ALL_FILES:
        print("Test", file)
        file_path_yaml = os.path.join("content_yaml", file + ".yaml")
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



def yaml2json(file: str, apply_reverse_corrections: bool=False):
    file_path_yaml = os.path.join("content_yaml", file + ".yaml")
    if not os.path.exists(file_path_yaml):
        print(f"File does not exist '{file_path_yaml}'")
        return
    with open(file_path_yaml, "r") as f:
        data = yaml.full_load(f)

    if apply_reverse_corrections:
        data = uncorrected(data)

    file_path_json = os.path.join("content", file + ".json")
    with open(file_path_json, "w") as f:
        json.dump(data, f, indent="  ")


def json2yaml(file: str):
    file_path_json = os.path.join("content", file + ".json")
    if not os.path.exists(file_path_json):
        print(f"File does not exist '{file_path_json}'")
        return
    with open(file_path_json, "r") as f:
        data = json.load(f)

    data = corrected(data)

    file_path_yaml = os.path.join("content_yaml", file + ".yaml")
    with open(file_path_yaml, "w") as f:
        yaml.dump(data, f)


def json2yamlall():
    for file in ALL_FILES:
        json2yaml(file)


def yaml2jsonall():
    for file in ALL_FILES:
        yaml2json(file)


def zip_all():
    with zipfile.ZipFile("kiergergaard-pillars.lcp", mode="w") as archive:
        for file in ALL_FILES:
            file_path_json = os.path.join("content", file + ".json")
            archive.write(file_path_json, file + ".json")


def build_lcp():
    yaml2jsonall()
    zip_all()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "tbyjY:J:", ["test", "build", "2yaml", "2json", "single2yaml=", "single2json="])
    except:
      print('build_manager.py -t -b -y -j -Y <file> -J <file>')
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-t':
            test_all()
        elif opt == '-l':
            build_lcp()
        elif opt == '-j':
            yaml2jsonall()
        elif opt == '-y':
            json2yamlall()
        elif opt == '-J':
            yaml2json(arg)
        elif opt == '-Y':
            json2yaml(arg)


if __name__ == "__main__":
    main(sys.argv[1:])