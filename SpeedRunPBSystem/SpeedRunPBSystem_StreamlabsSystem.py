#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json 
import pickle
import codecs

ScriptName = "Speed Run PB Script"
Website = "https://github.com/justinmmott/Streamlab-Scripts"
Description = "!pb (Game Name) will show pb for that specific game !npb (Game Name) (Time) to set a new pb"
Creator = "Bulg0gi"
Version = "1.0"

configFile = "config.json"
settings = {}
path = os.path.dirname(__file__)

def Init():
	global settings

	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
			init_pb(settings)
	except:
		settings = {
			"liveOnly": False,
			"getCommand": "!pb",
			"setCommand": "!npb",
			"getPermission": "Everyone",
			"setPermission": "Moderator",
			"useCooldown": True,
			"useCooldownMessages": False,
			"cooldown": 20,
			"onCooldown": "$user, $command is still on cooldown for $cd minutes!",
			"userCooldown": 120,
			"onUserCooldown": "$user, $command is still on user cooldown for $cd minutes!",
			"InitializePBs": "smb1 4:55 celeste 27:55"
		}
		init_pb(settings)


def Execute(data):

	if data.IsChatMessage() and data.GetParam(0).lower() == settings["getCommand"] and Parent.HasPermission(data.User, settings["getPermission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):

		outputMessage = ""

		if data.GetParamCount() == 2:
			gameName = str(data.GetParam(1).lower())
			pbs = load_pb()
			outputMessage = Parent.GetChannelName() + "'s PB in " + gameName + " is " + pbs[gameName]
		else:
			outputMessage = "Use the format !pb (Game Title) ex: !pb SMB1"
		
		Parent.SendStreamMessage(outputMessage)

	elif data.IsChatMessage() and data.GetParam(0).lower() == settings["setCommand"] and Parent.HasPermission(data.User, settings["setPermission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):

		outputMessage = "Please use the format !npb GameTitle PBTime"

		if data.GetParamCount() == 3:
			gameName = str(data.GetParam(1).lower())
			pb = load_pb();
			pb[gameName] = str(data.GetParam(2))
			save_pb(pb)
			outputMessage = "Congrats on the new PB! Your PB for " + gameName + " is " + pb[gameName]

		Parent.SendStreamMessage(outputMessage)
	return



def load_pb():
	with open(os.path.join(path, os.path.join("obj", "pb.pkl")), 'rb') as f:
		return pickle.load(f)

def save_pb(obj):
	with open(os.path.join(path, os.path.join("obj", "pb.pkl")), 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
	return


def ReloadSettings(jsonData):
	Init()
	return

def Tick():
	return

def init_pb(settings):	
	dict = {}
	pbs = settings["InitializePBs"].split()
	for i in (0, len(pbs)/2):
		if i % 2 == 0:
			dict[pbs[i]] = pbs[i+1]
	with open(os.path.join(path, os.path.join("obj", "pb.pkl")), 'wb') as f:
		pickle.dump(dict, f, pickle.HIGHEST_PROTOCOL)
	return
