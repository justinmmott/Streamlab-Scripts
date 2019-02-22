#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json 
import pickle

ScriptName = "Speed Run PB Script"
Website = "https://github.com/justinmmott/Streamlab-Scripts"
Description = "!pb {argument} will show pb for that specific game"
Creator = "Bulg0gi"
Version = "1.0"

def Init():
	global settings

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": False,
			"getCommand": "!pb",
			"setCommand": "!npb",
			"getPermission": "Everyone",
			"setPermission": "Moderator"
			"useCooldown": True,
			"useCooldownMessages": False,
			"cooldown": 20,
			"onCooldown": "$user, $command is still on cooldown for $cd minutes!",
			"userCooldown": 300,
			"onUserCooldown": "$user, $command is still on user cooldown for $cd minutes!",
		}

def Execute(data):

	if data.IsChatMessage() and data.GetParam(0).lower() == settings["getCommand"] and 
	Parent.HasPermission(data.User, settings["getPermission"], "") and 
	((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):

		outputMessage = ""

		if data.GetParamCount() == 2:
			gameName = str(data.GetParam(1))
		elif data.GetParamCount() == 1:
			gameName = "$mygame"
		else:
			outputMessage = "Use the format !pb (Game Title) ex: !pb SMB1"
		pbs = load_pb();
		outputMessage = pbs[gameName]
		Parent.SendStreamMessage(outputMessage)

	elif data.IsChatMessage() and data.GetParam(0).lower() == setings["setCommand"] and
	Parent.HasPermission(data.User, settings["setPermission"]) and 
	((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):

		outputMessage = ""

		if data.GetParamCount() == 3:
			gameName = str(data.GetParam(1))
		pb = load_pb();
		pb[gameName] = str(data.GetParam(2))
		save_pb(pb)
		outputMessage = "Congrats on the new PB! Your PB for " + gameName + " is " + pb[gameName]

		Parent.SendStreamMessage(outputMessage)
	return



def load_pb():
	with open('obj/' + "pb" + '.pkl', 'rb') as f:
		return pickle.load(f)

def save_pb(obj):
	with open('obj/' + "pb" + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def Tick():
	return