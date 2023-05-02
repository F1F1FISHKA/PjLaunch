let version= "None";
let accaunt= "None";
let installversion= "None";
let fabricInstallVersion = "None";
let forgeInstallVersion = "None";

eel.updInstalledVers()
eel.verInstalledUpd()
eel.accUpdate()
eel.releaseAdd()
eel.snapshotAdd()
eel.fabricAdd()
eel.forgeAdd()
function verSelect() {
	var sel=document.getElementById('verSelect').selectedIndex;
	var options=document.getElementById('verSelect').options;
	version = options[sel].value;
  }
function gameStart(){
	if (version == "None"){
		alertify.error('Выберете версию')
	}
	else if (accaunt == "None"){
		alertify.error('Выберете Аккаунт')
	}
	else{
		
		alertify.success("Запуск Minecraft "+version+"\n");
		eel.startGame(accaunt,version)
		eel.end()
	}
}
eel.expose(verSelectAdd);
function verSelectAdd(val,text){
	var x = document.getElementById("verSelect");
	var option = document.createElement("option");
	option.value = val;
	console.log("Loaded version: "+option.value);
	option.text = text;
	x.add(option);
	return 'OK';
}
eel.expose(accAdd);
function accAdd(nick){
	var x = document.getElementById("accaunts");
	var option = document.createElement("option");
	option.value = nick;
	console.log("Added accaunt: "+option.value);
	option.text = nick;
	x.add(option);
}
function AccountAdd(){
	var val = document.getElementById('accName').value;
    if (val == ""){
		alertify.error("Введите никнейм")
	}else if (val.length > 16){
		alertify.error("Длинна никнейма больше 16")
	}else {
		alertify.success("Никнейм сохранён!\nвсе пробелы будут заменены на '_'");
		accAdd(val)
		document.getElementById('accName').value = "";
		eel.accSave(val)
	}
}
function accauntSelect(){
	var sel=document.getElementById('accaunts').selectedIndex;
	var options=document.getElementById('accaunts').options;
	accaunt = options[sel].value;
}
function AccountRemove(){
	let option = document.querySelector("option[value="+accaunt+"]");
	if (option) {
    	option.remove()
		eel.accRemove(accaunt)
	}
}
eel.expose(err)
function err(error){
	alertify.error(error)

}
eel.expose(msg)
function msg(msg){
	alertify.message(msg)
}

eel.expose(success)
function success(msg){
	alertify.success(msg)
}

eel.expose(releaseAdd);
function releaseAdd(id){
	var x = document.getElementById("releasesSelect");
	var option = document.createElement("option");
	option.value = id;
	option.text = id;
	x.add(option);
}
eel.expose(snapshotAdd);
function snapshotAdd(id){
	var x = document.getElementById("snapshotSelect");
	var option = document.createElement("option");
	option.value = id;
	option.text = id;
	x.add(option);
}

eel.expose(fabricAdd)
function fabricAdd(id){
	var x = document.getElementById("fabricSelect");
	var option = document.createElement("option");
	option.value = id;
	option.text = id;
	x.add(option);
}


eel.expose(forgeAdd)
function forgeAdd(id){
	var x = document.getElementById("forgeSelect");
	var option = document.createElement("option");
	option.value = id;
	option.text = id;
	x.add(option);
}


function releasesSelect() {
	var sel=document.getElementById('releasesSelect').selectedIndex;
	var options=document.getElementById('releasesSelect').options;
	installversion = options[sel].value;
  }
function snaphotsSelect() {
	var sel=document.getElementById('snapshotSelect').selectedIndex;
	var options=document.getElementById('snapshotSelect').options;
	installversion = options[sel].value;
  }
function verInstall(){
	if (installversion == "None"){
		err("Выберете версию, которую хотите установить")
	}else{
		eel.installVer(installversion)	
}
}

function fabricSelect(){
	var sel=document.getElementById('fabricSelect').selectedIndex;
	var options=document.getElementById('fabricSelect').options;
	fabricInstallVersion = options[sel].value;
}

function forgeSelect(){
	var sel=document.getElementById('forgeSelect').selectedIndex;
	var options=document.getElementById('forgeSelect').options;
	forgeInstallVersion = options[sel].value;
}

function verRemove(){
	if (version != 'None'){eel.removeVer(version)}
	else{err("Выберете установленную версию, которую хотите удалить")}
}
eel.expose(instalationProgress)
function instalationProgress(progress){
	document.getElementById('installProgress').innerText = progress
}
eel.expose(instalationStatus)
function instalationStatus(status){
	document.getElementById('installStatus').innerText = status
}
eel.expose(update)
function update(){
	location.reload()
}
function fabricInstall(){
	if (fabricInstallVersion != "None"){
		eel.fabricInstall(fabricInstallVersion)
	}else{
		err("Выберете версию Fabric")
	}
}
function forgeInstall(){
	if (forgeInstallVersion != "None"){
		eel.forgeInstall(forgeInstallVersion)
	}else{
		err("Выберете версию Forge")
	}
}