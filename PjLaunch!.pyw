import eel, json, os, minecraft_launcher_lib,shutil,subprocess

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
minecraft_directory = "Minecraft"

def getAvailbleVersions():
    releases=[]
    snapshots=[]
    with open("config/available_versions.json", "w", encoding="UTF-8") as f:
        latest_versions = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory=minecraft_directory)
        json.dump(latest_versions, f, ensure_ascii=False, indent=4)

    with open("config/available_versions.json", encoding="UTF-8") as f:
        data = json.load(f)
        for i in range(len(data)):
            if data[i]["type"] == "release":
                releases.append(data[i]["id"])
            elif data[i]["type"] == "snapshot":
                snapshots.append(data[i]["id"])

    with open('config/releases.json', 'w') as f:  
        json.dump(releases, f, ensure_ascii=False, indent=4)
    with open('config/snapshots.json', 'w') as f: 

        json.dump(snapshots, f, ensure_ascii=False, indent=4)   


eel.init("UI")

getAvailbleVersions()

@eel.expose
def updInstalledVers():
    with open("config/installedversions.json","w") as f:
        json.dump(minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory=minecraft_directory), f, ensure_ascii=False, indent=4)

@eel.expose
def verInstalledUpd():
    with open("config/installedversions.json",encoding='utf8') as file:
        installedVers  = json.load(file)
        eel.verSelectAdd("None","Выберете версию")
    for i in range(len(installedVers)):
        eel.verSelectAdd(installedVers[i]["id"],installedVers[i]["id"])
        

@eel.expose
def accSave(name):
    with open("config/accaunts.json",'r+') as file:
        file_data = json.load(file)
        file_data["accaunts"].append(name)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

@eel.expose
def accRemove(name):
    with open("config/accaunts.json",'r+') as file:
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
     with open("config/accaunts.json",encoding='utf8') as file:
        file_data = json.load(file)
        accaunts = file_data['accaunts']
        for i in range(len(accaunts)):
            eel.accAdd(accaunts[i])
@eel.expose
def startGame(name,id):
    options = minecraft_launcher_lib.utils.generate_test_options()
    options["username"] = name
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(id, minecraft_directory, options)
    subprocess.call(minecraft_command)
    
@eel.expose
def end():
    pass

@eel.expose
def releaseAdd():
    with open("config/releases.json") as f:
        data = json.load(f)
        for i in range(len(data)):
            eel.releaseAdd(data[i])

@eel.expose
def snapshotAdd():
    with open("config/snapshots.json") as f:
        data = json.load(f)
        for i in range(len(data)):
            eel.snapshotAdd(data[i])
@eel.expose
def installVer(id):
    eel.msg(f"Установка {id}")
    minecraft_launcher_lib.install.install_minecraft_version(id, minecraft_directory)
    eel.success("Установленно!")
    print(f"Installed {id}!")

@eel.expose
def removeVer(id):
    eel.msg("Удаление "+id)
    try:
        shutil.rmtree(f"{minecraft_directory}//versions//{id}")
        eel.succsess("Удалено!")
        print(f"Removed {id}!")
    except FileNotFoundError:
        eel.err(f"Версия {id} не найдена")
        print(f"Version {id} not found!")

    
 
eel.start("index.html" ,size=(830, 750))