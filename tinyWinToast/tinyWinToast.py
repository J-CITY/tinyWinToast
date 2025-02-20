# Docks:
# https://github.com/GitHub30/toast-notification-examples
# https://learn.microsoft.com/en-us/windows/apps/design/shell/tiles-and-notifications/adaptive-interactive-toasts?tabs=xml

import datetime
from xml.dom import minidom
import os
import subprocess
import io

TEXT_ALIGN_LEFT = "left"
TEXT_ALIGN_RIGHT = "right"

TEXT_STYLE_CAPTION_SUBTLE = "captionSubtle"
TEXT_STYLE_BASE = "base" 

CROP_NONE = "none"
CROP_CIRCLE = "circle"

DURATION_SHORT = "short"
DURATION_LONG = "long"

DEFAULT_APP_ID = "{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\\v1.0\powershell.exe"

ACTION_TYPE_PROTOCOL = "protocol"
ACTION_TYPE_BACKGROUND = "background"
ACTION_TYPE_FOREGROUND = "foreground"
ACTION_TYPE_SYSTEM = "system"

SCENARIO_DEFAULT = "default"
SCENARIO_ALARM = "alarm"
SCENARIO_REMINDER = "reminder"
SCENARIO_INCOMING_CALL = "incomingCall"

INPUT_TEXT = "text"
INPUT_SELECTION = "selection"

ACTION_INPUT = "input"
ACTION_BUTTON = "button"

class Config:
	def __init__(self):
		# for dynamic toast update need set tag and group
		self.TAG = ""
		self.GROUP = ""

		#Application id
		self.APP_ID = DEFAULT_APP_ID

		# foreground | background | protocol | system
		# ACTION_TYPE_PROTOCOL
		# ACTION_TYPE_BACKGROUND
		# ACTION_TYPE_FOREGROUND
		# ACTION_TYPE_SYSTEM
		self.ACTION_TYPE = ACTION_TYPE_PROTOCOL

		self.ACTION_ARGUMENT = ""

		# - default | alarm | reminder | incomingCall"
		# SCENARIO_DEFAULT 
		# SCENARIO_ALARM 
		# SCENARIO_REMINDER 
		# SCENARIO_INCOMING_CALL 
		self.SCENARIO = SCENARIO_DEFAULT

		# short - 5sec - DURATION_SHORT
		# long - 25 sec - DURATION_SHORT
		self.DURATION = DURATION_SHORT

		self.BASE_URI = ""

		# [0] - TITLE
		# [1] - MESSAGE
		# [2]... other message
		self.TEXTS = []

		self.ICO_IMAGE = ()

		self.HERO_IMAGE = ()

		self.IMAGE = []

		# in ISO 8601
		self.TIME = ""

		# true to set current time
		self.SET_CUT_TIME = False

		self.PROGRESS = []

		self.HEADER = None

		self.TEXTS_GROUP_LEFT = []
		self.TEXTS_GROUP_RIGHT = []

		self._WITH_ACTIONS = False

		self.ACTIONS = []

		self.AUDIO = None

		self.USE_ACTIONS_CALLBACK = None

class Audio:
	def __init__(self, isSilent=False, src="", isLoop=False):
		"""Add audio to toast

		:isSilent: true for mute toast sound
		:src: audio source
		:isLoop: if you want loop
		"""
		self.isSilent = isSilent
		self.src = src
		self.isLoop = isLoop

class Progress:
	def __init__(self, title="", value="", valueStringOverride="", status=""):
		"""Progress for toast

		:title: progress title
		:value: value of progress bar (0.0 - 1.0)
		:valueStringOverride: value string info
		:status: status
		"""
		self.title = title
		self.value = value
		self.valueStringOverride = valueStringOverride
		self.status = status

class Header:
	def __init__(self, id="", title="", arguments=""):
		"""Set header if you want group toast

		:id: id of your toast group
		:title: header name
		:arguments: action
		"""
		self.id= id
		self.title= title
		self.arguments= arguments

class Button:
	def __init__(self, content="", arguments="", activationType=ACTION_TYPE_FOREGROUND, pendingUpdate=False, inputId="", imageUri=""):
		"""Add button to toast

		:content: button text
		:arguments: button action
		:activationType: /background/foreground
		:pendingUpdate: if True then toast wait update
		:inputId: set id of input box (if you need)
		:imageUri: set image for button
		"""
		self.content = content
		self.arguments = arguments
		self.activationType = activationType
		self.pendingUpdate = pendingUpdate
		self.inputId = inputId
		self.imageUri = imageUri


class Input:
	def __init__(self, inputId="", intype=INPUT_TEXT, placeHolderContent="", selections = [], defaultInput=""):
		"""Add input to toast

		:inputId: input id
		:intype: type /text/selection
		:placeHolderContent: input himt if type is text
		:selections: list of selections (id, content)
		:defaultInput: default selection id if type is selection
		"""
		self.inputId = inputId
		self.intype = intype
		self.placeHolderContent = placeHolderContent
		self.selections = selections
		self.defaultInput = defaultInput

	def addSelection(self, id, content):
		self.selections.append(id, content)

def ToastInit():
	"""Load PoshWinRT.dll for button callback"""
	script = '''Invoke-WebRequest https://github.com/GitHub30/PoshWinRT/releases/download/1.2/PoshWinRT.dll -OutFile PoshWinRT.dll'''
	path = os.path.dirname(os.path.realpath(__file__)) + "\\"
	text_file = open(path + "script.ps1", "w")
	text_file.write(script)
	text_file.close()
	subprocess.run(["PowerShell", "-ExecutionPolicy", "Bypass", "-File", path + "script.ps1"])
	os.remove(path + "script.ps1")
class Toast:
	def __init__(self, config=None):
		"""Init

		:config: toast config
		"""
		if config is None:
			self.config = Config()
		else:
			self.config = config

	def setConfig(self, config):
		"""Set toast config

		:config: toast config
		"""
		self.config = config

	def getConfig(self):
		"""Get toast config"""
		return self.config

	def setAppID(self, appid):
		"""Set application ID

		"appid" application ID (string)
		"""
		self.config.APP_ID = appid

	def setTag(self, tag):
		"""Set toast tag (if you want grout yout notifications)

		:tag: toast tag
		"""
		self.config.TAG = tag
	
	def setGroup(self, group):
		"""Set toast group (if you want grout yout notifications)

		:group: toast group
		"""
		self.config.GROUP = group

	def setTime(self, time):
		"""Set toast time

		:time: toast time in ISO 8601 format
		"""
		self.config.TIME = time

	def setCurTime(self):
		"""Set toast current time"""
		self.config.SET_CUT_TIME = True

	def setTitle(self, title, maxLines=1):
		"""Set title

		:title: toast title
		:maxLines: max title lines
		"""
		if len(self.config.TEXTS) > 0:
			self.config.TEXTS[0] = (title, maxLines, "", "", False)
		else:
			self.config.TEXTS.append((title, maxLines, "", "", False))

	def setMessage(self, msg, maxLines=1):
		"""Set message

		:msg: toast message
		:maxLines: max message lines
		"""
		if len(self.config.TEXTS) > 1:
			self.config.TEXTS[1] = (msg, maxLines, "", "", False)
		elif len(self.config.TEXTS) == 0:
			self.config.TEXTS.append(("", 1, ""))
			self.config.TEXTS.append((msg, maxLines, "", "", False))
		else:
			self.config.TEXTS.append((msg, maxLines, "", "", False))

	def addText(self, msg, maxLines=1, placement="", style=TEXT_STYLE_BASE, wrap=False):
		"""Add message to toast

		:msg: message
		:maxLines: max text lines
		:placement: set attribute to text /attribution
		:style: style /captionSubtle/base
		:wrap: wrap text
		"""
		if len(self.config.TEXTS) == 0:
			self.config.TEXTS.append(("", 1, ""))
			self.config.TEXTS.append((msg, maxLines, placement, style, wrap))
		else:
			self.config.TEXTS.append((msg, maxLines, placement, style, wrap))

	def addGroupText(self, msg, maxLines=1, placement="", style=TEXT_STYLE_BASE, wrap=False, align=TEXT_ALIGN_LEFT):
		"""Add text in footer
		
		:msg: message
		:maxLines: max text lines
		:placement: set attribute to text /attribution
		:style: style /captionSubtle/base
		:wrap: wrap text
		:align: /left/right
		"""
		if align == "left":
			if len(self.config.TEXTS_GROUP_LEFT) == 0:
				self.config.TEXTS_GROUP_LEFT.append(("", 1, "", "captionSubtle", False))
				self.config.TEXTS_GROUP_LEFT.append((msg, maxLines, placement, style, wrap))
			else:
				self.config.TEXTS_GROUP_LEFT.append((msg, maxLines, placement, style, wrap))
		else:
			if len(self.config.TEXTS_GROUP_RIGHT) == 0:
				self.config.TEXTS_GROUP_RIGHT.append(("", 1, "", "captionSubtle", False))
				self.config.TEXTS_GROUP_RIGHT.append((msg, maxLines, placement, style, wrap))
			else:
				self.config.TEXTS_GROUP_RIGHT.append((msg, maxLines, placement, style, wrap))

	def setIcon(self, src, crop=CROP_NONE):
		"""Set toast logo

		:src: path or url to image
		:crop: image crop /none/circle
		"""
		self.config.ICO_IMAGE = ("appLogoOverride", src, crop)

	def setHeroImage(self, src):
		"""Set hero image

		:src: path or url to image
		"""
		self.config.HERO_IMAGE = ("hero", src)

	def setImage(self, src):
		"""Set image

		:src: path or url to image
		"""
		self.config.IMAGE = [src]

	def addImage(self, src):
		"""Set image

		:src: path or url to image
		"""
		self.config.IMAGE.append(src)

	def setDuration(self, duration="short"):
		self.config.DURATION = duration

	def addHeader(self, header):
		"""Add toast header

		:header: Head object
		"""
		self.config.HEADER = header

	def addProgress(self, progress):
		"""Add progress data"""
		self.config.PROGRESS.append(progress)

	def setProgress(self, progress):
		"""Set progers data and clear old data"""
		self.config.PROGRESS = [progress]

	def addButton(self, button):
		"""Add button to toast

		:button: Button object
		"""
		self.config._WITH_ACTIONS = True
		self.config.ACTIONS.append(("button", button))

	def addInput(self, input):
		"""Add input to toast

		:input: Input object
		"""
		self.config._WITH_ACTIONS = True
		self.config.ACTIONS.append(("input", input))

	def setAudio(self, audio):
		"""Set toast sound

		"audio": audio object
		"""
		self.config.AUDIO = audio

	def __genXML(self):
		"""Generate xml"""
		head = """
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$APP_ID = '{0}'""".format(self.config.APP_ID)
		if self.config.TAG != "":
			head += "\n$tag = '{0}'\n".format(self.config.TAG)
		
		if self.config.GROUP != "":
			head += "\n$group = '{0}'\n".format(self.config.GROUP)
		head += '\n$template = @"\n'


		doc = minidom.Document()
		toast = doc.createElement('toast')
		doc.appendChild(toast)
		toast.setAttribute("activationType", self.config.ACTION_TYPE)
		toast.setAttribute("launch", self.config.ACTION_ARGUMENT)
		toast.setAttribute("duration", self.config.DURATION)
		toast.setAttribute("scenario", self.config.SCENARIO)
		if self.config.TIME != '':
			toast.setAttribute("displayTimestamp", self.config.TIME)
		elif self.config.SET_CUT_TIME:
			self.config.TIME = str(datetime.datetime.now())
			self.config.TIME = self.config.TIME.replace(' ', 'T')
			import re
			self.config.TIME = re.sub(r"\.\d+", ".00Z", self.config.TIME)
			toast.setAttribute("displayTimestamp", self.config.TIME)

		if not self.config.HEADER is None:
			header = doc.createElement('header')
			header.setAttribute("id", self.config.HEADER.id)
			header.setAttribute("title", self.config.HEADER.title)
			header.setAttribute("arguments", self.config.HEADER.arguments)
			toast.appendChild(header)

		visual = doc.createElement('visual')
		toast.appendChild(visual)

		binding = doc.createElement('binding')
		visual.appendChild(binding)
		binding.setAttribute("template", "ToastGeneric")

		for txt in self.config.TEXTS:
			text = doc.createElement('text')
			data = doc.createTextNode(txt[0])
			text.appendChild(data)
			text.setAttribute("hint-maxLines", str(txt[1]))
			if txt[2] != '':
				text.setAttribute("placement", str(txt[2]))
			if txt[3] != '':
				text.setAttribute("hint-style", str(txt[3]))
			if txt[4]:
				text.setAttribute("hint-wrap", "true")
			binding.appendChild(text)
		
		if self.config.ICO_IMAGE != ():
			image = doc.createElement('image')
			image.setAttribute("placement", self.config.ICO_IMAGE[0])
			image.setAttribute("hint-crop", self.config.ICO_IMAGE[2])
			image.setAttribute("src", self.config.ICO_IMAGE[1])
			binding.appendChild(image)

		if self.config.HERO_IMAGE != ():
			image = doc.createElement('image')
			image.setAttribute("placement", self.config.HERO_IMAGE[0])
			image.setAttribute("src", self.config.HERO_IMAGE[1])
			binding.appendChild(image)

		if self.config.IMAGE != []:
			for im in self.config.IMAGE:
				image = doc.createElement('image')
				image.setAttribute("src", im)
				binding.appendChild(image)


		for p in self.config.PROGRESS:
			progress = doc.createElement('progress')
			progress.setAttribute("title", p.title)
			progress.setAttribute("value", p.value)
			progress.setAttribute("valueStringOverride", p.valueStringOverride)
			progress.setAttribute("status", p.status)
			binding.appendChild(progress)

		if self.config.TEXTS_GROUP_LEFT != [] or self.config.TEXTS_GROUP_RIGHT != []:
			group = doc.createElement('group')
			binding.appendChild(group)

			subgroup1 = doc.createElement('subgroup')
			subgroup2 = doc.createElement('subgroup')
			group.appendChild(subgroup1)
			group.appendChild(subgroup2)
			for txt in self.config.TEXTS_GROUP_LEFT:
				text = doc.createElement('text')
				data = doc.createTextNode(txt[0])
				text.appendChild(data)
				text.setAttribute("hint-maxLines", str(txt[1]))
				if txt[2] != '':
					text.setAttribute("placement", str(txt[2]))
				if txt[3] != '':
					text.setAttribute("hint-style", str(txt[3]))
				if txt[4]:
					text.setAttribute("hint-wrap", "true")
				subgroup1.appendChild(text)

			for txt in self.config.TEXTS_GROUP_RIGHT:
				text = doc.createElement('text')
				data = doc.createTextNode(txt[0])
				text.appendChild(data)
				text.setAttribute("hint-maxLines", str(txt[1]))
				if txt[2] != '':
					text.setAttribute("placement", str(txt[2]))
				if txt[3] != '':
					text.setAttribute("hint-style", str(txt[3]))
				if txt[4]:
					text.setAttribute("hint-wrap", "true")
				text.setAttribute("hint-align", "right")
				subgroup2.appendChild(text)

		# actions
		if self.config._WITH_ACTIONS:
			actions = doc.createElement('actions')
			toast.appendChild(actions)

			def sortF(val):
				return val[0] 
			self.config.ACTIONS.sort(key=sortF, reverse=True)

			for a in self.config.ACTIONS:
				t = a[0]

				b = a[1]

				if a[0] == ACTION_BUTTON:
					action = doc.createElement("action")
					action.setAttribute("content", b.content)
					action.setAttribute("arguments", b.arguments)
					action.setAttribute("activationType", b.activationType)
					if b.imageUri != "":
						action.setAttribute("imageUri", b.imageUri)
					if b.inputId != "":
						action.setAttribute("hint-inputId", b.inputId)
					if b.pendingUpdate:
						action.setAttribute("afterActivationBehavior", "pendingUpdate")
					if b.inputId != "":
						action.setAttribute("hint-inputId", b.inputId)
					actions.appendChild(action)
				else:
					input = doc.createElement("input")
					input.setAttribute("id", b.inputId)
					input.setAttribute("type", b.intype)
					if b.placeHolderContent != "" and b.intype == "text":
						input.setAttribute("placeHolderContent", b.placeHolderContent)
					if b.defaultInput != "" and b.intype == "selection":
						input.setAttribute("defaultInput", b.defaultInput)
					
					if b.intype == 'selection':
						for s in b.selections:
							selection = doc.createElement("selection")
							selection.setAttribute("id", s[0])
							selection.setAttribute("content", s[1])
							input.appendChild(selection)
					actions.appendChild(input)
			

		if not self.config.AUDIO is None:
			audio = doc.createElement('audio')
			if self.config.AUDIO.isSilent:
				audio.setAttribute("silent", "true")
			else:
				audio.setAttribute("src", self.config.AUDIO.src)
				if self.config.AUDIO.loop:
					audio.setAttribute("loop", "true")
			toast.appendChild(audio)

		tail = '''"@
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = New-Object Windows.UI.Notifications.ToastNotification $xml
'''
		if self.config.USE_ACTIONS_CALLBACK:
			tail += '''
function WrapToastEvent {
  param($target, $eventName)

  Add-Type -Path PoshWinRT.dll
  $wrapper = new-object "PoshWinRT.EventWrapper[Windows.UI.Notifications.ToastNotification,System.Object]"
  $wrapper.Register($target, $eventName)
}

Register-ObjectEvent -InputObject (WrapToastEvent $toast 'Activated') -EventName FireEvent -Action {
  $setStr = "["
  foreach ($h in $args[1].Result.userinput) {
    $setStr = $setStr + "$($h),"
  }
  $setStr = $setStr + "]"
  $formattedString = "TOAST_DATA:arguments:{0};textBox:{1};" -f $args[1].Result.Arguments, $setStr
  Write-Output $formattedString | Out-File -FilePath ./Output;
}
'''
		if self.config.TAG != "":
			tail += "$toast.Tag = $tag\n"
		if self.config.GROUP != "":
			tail += "$toast.Group = $group\n"
		tail += '''
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($APP_ID)'''
	
		tail += '.Show($toast)'
		#TODO: try remove this hack
		if self.config.USE_ACTIONS_CALLBACK:
			tail += '\nStart-Sleep -Seconds 15'
		toaststr = head + '\n' + doc.toprettyxml(indent="	").split("\n",1)[1] + '\n' + tail

		#print(toaststr)
		return toaststr

	def generateScript(self):
		"""Generate ps1 script"""
		return self.__genXML()

	def show(self):
		"""Show toast"""
		toaststr = self.__genXML()
		path = os.path.dirname(os.path.realpath(__file__)) + "\\"
		text_file = open(path + "toast.ps1", "w")
		text_file.write(toaststr)
		text_file.close()
		#if self.config.USE_ACTIONS_CALLBACK:
		#	self.process = subprocess.Popen(["PowerShell", "-ExecutionPolicy", "Bypass", "-File", path + "toast.ps1"], stdout=subprocess.PIPE)
		#else:
		subprocess.run(["PowerShell", "-ExecutionPolicy", "Bypass", "-File", path + "toast.ps1"])
		#os.remove(path + "toast.ps1")

	#TODO: add file watch
	def getEventListenerOutput(self):
		with open('./Output', 'r') as file:
			return file.read()

		#if self.process is None:
		#	return ""
		#result = []
		#for line in io.TextIOWrapper(self.process.stdout, encoding="utf-8"):
		#	print(line)
		#	if (line.startswith("TOAST_DATA:")):
		#		result.append(line)
		#return result
	
	#def killListener(self):
	#	if self.process is None:
	#		return
	#	self.process.kill()
	#	self.process = None

	def update(self, sequenceId, data):
		"""Update toast"""
		toaststr = """
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$APP_ID = '{0}'""".format(self.config.APP_ID)
		toaststr+= """
$sequenceId = {0}
		""".format(sequenceId)
		toaststr+= """
$tag = '{0}'
		""".format(self.config.TAG)
		toaststr+= """
$group = '{0}'
		""".format(self.config.GROUP)
		toaststr+='''

$data = New-Object Windows.UI.Notifications.NotificationData
$data.SequenceNumber = $sequenceId

$DataDictionary = New-Object 'system.collections.generic.dictionary[string,string]'
'''

		for key, val in data.items():
			toaststr += "$DataDictionary.Add('{0}', '{1}')\n".format(key, val)

		toaststr += '''

$ToastData = [Windows.UI.Notifications.NotificationData]::new($DataDictionary)


[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($APP_ID)'''
		toaststr += ".Update($ToastData, $tag, $group)"
		path = os.path.dirname(os.path.realpath(__file__)) + "\\"
		text_file = open(path + "toast.ps1", "w")
		text_file.write(toaststr)
		text_file.close()
		subprocess.run(["PowerShell", "-ExecutionPolicy", "Bypass", "-File", path + "toast.ps1"])
		os.remove(path + "toast.ps1")

	def showFromXml(self, appId, xml):
		"""Show toast from xml
		
		:appId: application id
		:xml: xml string
		"""
		toaststr = """
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$APP_ID = '{0}'
$template = @"
{1}
"@
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = New-Object Windows.UI.Notifications.ToastNotification $xml
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($APP_ID).Show($toast)""".format(appId, xml)
		path = os.path.dirname(os.path.realpath(__file__)) + "\\"
		text_file = open("toast.ps1", "w")
		text_file.write(toaststr)
		text_file.close()

		subprocess.run(["PowerShell", "-ExecutionPolicy", "Bypass", "-File", path + "toast.ps1"])
		os.remove(path + "toast.ps1")

	def startFromScript(self, scriptPath):
		"""Start toast from script
		
		:scriptPath: script.ps1 path
		"""
		subprocess.run(["PowerShell", "-ExecutionPolicy", "Bypass", "-File", scriptPath])

	def updateFromScript(self, scriptPath):
		"""Update toast from script
		
		:scriptPath: script.ps1 path
		"""
		subprocess.run(["PowerShell", "-ExecutionPolicy", "Bypass", "-File", scriptPath])

	def clearToasts(self):
		"""Clear toast from app with APP_ID"""

		script = """
$APP_ID = '{0}'
[Windows.UI.Notifications.ToastNotificationManager]::History.Clear($APP_ID)
""".format(self.config.APP_ID)
		path = os.path.dirname(os.path.realpath(__file__)) + "\\"
		text_file = open(path + "script.ps1", "w")
		text_file.write(script)
		text_file.close()
		subprocess.run(["PowerShell", "-ExecutionPolicy", "Bypass", "-File", path + "script.ps1"])
		os.remove(path + "script.ps1")


def getToast(title, message, icon="", iconCrop=CROP_NONE, duration=DURATION_SHORT, appId="", isMute=True):
	"""Create simple toast

	:title: toast title
	:message: toast message
	:icon: path or url to icon
	:iconCrop: crop icon /none/circle
	:duration: duration /short/long
	"""
	toast = Toast()
	if appId != "":
		toast.setAppID(appId)
	toast.setTitle(title, maxLines=1)
	toast.setMessage(message, maxLines=1)
	if icon != "":
		toast.setIcon(icon, crop=iconCrop)
	toast.setDuration(duration)
	if isMute:
		toast.setAudio(Audio(True))
	return toast

#toast = Toast()
#toast.setTitle("TITLE", maxLines=1)
#toast.setMessage("MESSAGE", maxLines=1)
##toast.setTag("mytag")
##toast.setGroup("mygroup")
##toast.addInput(Input(inputId="111", intype="text", placeHolderContent="Input text..."))
##toast.addInput(Input(inputId="112", intype="selection", selections = [("1","Yes"), ("2","No"), ("3","Maybe")], defaultInput="1"))
##toast.addButton(Button(content="Play", activationType="background", arguments="dismiss", pendingUpdate=False))
#toast.addButton(Button(content="Pause", activationType="protocol", arguments='''runas.exe /savecred /user:333danich333@mail.ru "C:/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/Uplay.exe"''', pendingUpdate=False))
#toast.addButton(Button(content="HTTP", activationType="protocol", arguments="https://www.google.com/", pendingUpdate=False))
#toast.setIcon('C:/Users/333da/Desktop/wintoast/0.jpg', crop="circle")
#toast.show()


#getToast("Title", "Message", 'C:/Users/333da/Desktop/wintoast/0.jpg', "circle", "short").show()