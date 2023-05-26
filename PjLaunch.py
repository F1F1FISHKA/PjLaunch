import eel, json, os, minecraft_launcher_lib,subprocess,uuid,shutil,threading,sys





banner = '''                                                                               
 _|_|_|    _|  _|                                                _|        _|  
 _|    _|      _|          _|_|_|  _|    _|  _|_|_|      _|_|_|  _|_|_|    _|  
 _|_|_|    _|  _|        _|    _|  _|    _|  _|    _|  _|        _|    _|  _|  
 _|        _|  _|        _|    _|  _|    _|  _|    _|  _|        _|    _|      
 _|        _|  _|_|_|_|    _|_|_|    _|_|_|  _|    _|    _|_|_|  _|    _|  _|  
           _|                                                                  
         _|                       Debug console    '''


print(f"{banner}\n\n                  v0.2")
print("\n\nПосле закрытия этого окна лаунчер не будет отвечать")


## MINCRAFT SETTINGS
minecraft_directory = "../Minecraft"
confi_dir = "../config"
ui_dir = "UI"



current_max = 0

###  make launcher_profiles.json :
try:
    with open(f"{minecraft_directory}/launcher_profiles.json","w")as f:
        data = {"clientToken": "47963e9c-f137-41c1-b7a4-2d9588278cde","profiles": {}}
        json.dump(data, f, ensure_ascii=False, indent=4)
except FileNotFoundError:
    try:
        os.mkdir(minecraft_directory)
    except OSError:
        raise Exception('Неудалось создать директорию Minecraft')

def set_status(status: str):
    print(status)
    eel.instalationStatus(status)


def set_progress(progress: int):
    if current_max != 0:
        print(f"{progress}/{current_max}")
        eel.instalationProgress(f"{progress}/{current_max}")


def set_max(new_max: int):
    global current_max
    current_max = new_max



def getAvailbleVersions():
    releases=[]
    snapshots=[]
    forge=[]
    fabric = minecraft_launcher_lib.fabric.get_stable_minecraft_versions()
    with open(f"{confi_dir}/available_versions.json", "w", encoding="UTF-8") as f:
        latest_versions = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory=minecraft_directory)
        json.dump(latest_versions, f, ensure_ascii=False, indent=4)

    with open(f"{confi_dir}/available_versions.json", encoding="UTF-8") as f:
        data = json.load(f)
        for i in range(len(data)):
            if data[i]["type"] == "release":
                releases.append(data[i]["id"])
            elif data[i]["type"] == "snapshot":
                snapshots.append(data[i]["id"])
    with open(f"{confi_dir}/available_versions.json", encoding="UTF-8") as f:
        data = json.load(f)
        for i in range(len(releases)):
            if minecraft_launcher_lib.forge.find_forge_version(releases[i]) != None:
                forge.append(minecraft_launcher_lib.forge.find_forge_version(releases[i]))

    

    with open(f'{confi_dir}/releases.json', 'w') as f:  
        json.dump(releases, f, ensure_ascii=False, indent=4)
    with open(f'{confi_dir}/snapshots.json', 'w') as f: 
        json.dump(snapshots, f, ensure_ascii=False, indent=4)     
    with open(f'{confi_dir}/forge.json', 'w') as f: 
        json.dump(forge, f, ensure_ascii=False, indent=4) 
    with open(f'{confi_dir}/fabric.json', 'w') as f: 
        json.dump(fabric, f, ensure_ascii=False, indent=4)


eel.init("UI")

getAvailbleVersions()

@eel.expose
def updInstalledVers():
    with open(f"{confi_dir}/installedversions.json","w") as f:
        json.dump(minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory=minecraft_directory), f, ensure_ascii=False, indent=4)

@eel.expose
def verInstalledUpd():
    with open(f"{confi_dir}/installedversions.json",encoding='utf8') as file:
        installedVers  = json.load(file)
        eel.verSelectAdd("None","Выберете версию")
    for i in range(len(installedVers)):
        eel.verSelectAdd(installedVers[i]["id"],installedVers[i]["id"])
        

@eel.expose
def accSave(name):
    with open(f"{confi_dir}/accaunts.json",'r+') as file:
        file_data = json.load(file)
        file_data[name] = str(uuid.uuid4())
        file.seek(0)
        json.dump(file_data, file, indent = 4)

@eel.expose
def accRemove(name):
    with open(f"{confi_dir}/accaunts.json",'r+') as file:
        try:
            file_data = json.load(file)
            accaunts = file_data['accaunts']
            accaunts.remove(name)
            print(file_data)
            file.seek(0)
            json.dump(file_data, file)
            file.truncate()
        except ValueError:
            eel.err(f"Неудалось удалить {name}")
@eel.expose
def accUpdate():
     with open(f"{confi_dir}/accaunts.json",encoding='utf8') as file:
        file_data = json.load(file)
        accaunts = list(file_data.keys())
        for i in range(len(accaunts)):
            eel.accAdd(accaunts[i])
@eel.expose
def startGame(name,id):
    with open(f"{confi_dir}/accaunts.json",encoding='utf8') as file:
        file_data = json.load(file)
        accaunts = list(file_data.keys())
    options = minecraft_launcher_lib.utils.generate_test_options()
    options["username"] = name
    options["uuid"] = file_data[name]
    print(options)
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(id, minecraft_directory, options)
    subprocess.Popen(minecraft_command, shell=True, stdout=subprocess.PIPE).stdout.read()
    
@eel.expose
def end():
    pass

@eel.expose
def releaseAdd():
    with open(f"{confi_dir}/releases.json") as f:
        data = json.load(f)
        for i in range(len(data)):
            eel.releaseAdd(data[i])
@eel.expose
def fabricAdd():
    with open(f"{confi_dir}/fabric.json") as f:
        data = json.load(f)
        for i in range(len(data)):
            eel.fabricAdd(data[i])

@eel.expose
def forgeAdd():
    with open(f"{confi_dir}/forge.json") as f:
        data = json.load(f)
        for i in range(len(data)):
            eel.forgeAdd(data[i])

@eel.expose
def snapshotAdd():
    with open(f"{confi_dir}/snapshots.json") as f:
        data = json.load(f)
        for i in range(len(data)):
            eel.snapshotAdd(data[i])

callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}



@eel.expose
def installVer(id):
    eel.msg(f"Установка {id}")
    minecraft_launcher_lib.install.install_minecraft_version(id, minecraft_directory,callback=callback)
    eel.success("Установленно!")
    print(f"Installed {id}!")
    eel.update()
@eel.expose
def fabricInstall(id):
    eel.msg(f"Установка Fabric {id}")
    minecraft_launcher_lib.fabric.install_fabric(id,minecraft_directory,callback=callback)
    eel.update()
@eel.expose
def forgeInstall(id):
    eel.msg(f"Установка Forge {id}")
    minecraft_launcher_lib.forge.install_forge_version(id,minecraft_directory,callback=callback)
    eel.update()

@eel.expose
def removeVer(id):
    eel.msg("Удаление "+id)
    try:
        shutil.rmtree(f"{minecraft_directory}//versions//{id}")
        eel.update() 
        eel.success("Удалено!")
        print(f"Removed {id}!")
    except FileNotFoundError:
        eel.err(f"Версия {id} не найдена")
        print(f"Version {id} not found!")

    

eel.start("index.html")
