# TinyWinToast

:email: Tiny library to show windows toast

# Description
I want use notification in my console player, but I want more powerful toast then in [win10toast](https://github.com/jithurjacob/Windows-10-Toast-Notifications "win10toast"),
so I write this lib.

# Installation

...

# Examples:

See source code to get more information

Simple start:

To create simple toast:

```python
getToast("Title", "Message", 'C:/Users/333da/Desktop/wintoast/0.jpg', crop="circle", duration="short", appId="MyApp", isMute=True).show()
```

Or you can create toast object

0# Simple toast

```python
toast = Toast()
toast.setTitle("TITLE", maxLines=2)
toast.setMessage("MESSAGE", maxLines=2)
toast.setIcon('image.png', crop="none")
toast.show()
```

![Imgur](https://github.com/J-CITY/TinyWinToast/blob/master/screens/0.png)

1# More text and circle crop

```python
toast = Toast()
toast.setTitle("TITLE", maxLines=1)
toast.setMessage("MESSAGE", maxLines=1)
toast.addText("MORE TEXT", maxLines=1)
toast.setIcon('image.png', crop="circle")
toast.show()
```

![Imgur](https://github.com/J-CITY/TinyWinToast/blob/master/screens/1.png)

2# Add hero image

```python
toast = Toast()
toast.setTitle("TITLE", maxLines=1)
toast.setMessage("MESSAGE", maxLines=1)
toast.addText("MORE TEXT", maxLines=1)
toast.setIcon('C:/Users/333da/Desktop/wintoast/0.jpg', crop="circle")
toast.setHeroImage("C:/Users/333da/Desktop/wintoast/1.jpg")
toast.show()
```

![Imgur](https://github.com/J-CITY/TinyWinToast/blob/master/screens/2.png)

3# Add image

```python
toast = Toast()
toast.setTitle("TITLE", maxLines=1)
toast.setMessage("MESSAGE", maxLines=1)
toast.addText("MORE TEXT", maxLines=1)
toast.setIcon('C:/Users/333da/Desktop/wintoast/0.jpg', crop="circle")
toast.setImage("C:/Users/333da/Desktop/wintoast/1.jpg")
toast.show()
```

![Imgur](https://github.com/J-CITY/TinyWinToast/blob/master/screens/3.png)

4# More images

```python
toast = Toast()
toast.setTitle("TITLE", maxLines=1)
toast.setMessage("MESSAGE", maxLines=1)
toast.addText("MORE TEXT", maxLines=1)
toast.setIcon('C:/Users/333da/Desktop/wintoast/0.jpg', crop="circle")
toast.addImage("C:/Users/333da/Desktop/wintoast/1.jpg")
toast.addImage("C:/Users/333da/Desktop/wintoast/1.jpg")
toast.addImage("C:/Users/333da/Desktop/wintoast/1.jpg")
toast.addImage("C:/Users/333da/Desktop/wintoast/1.jpg")
toast.show()
```

![Imgur](https://github.com/J-CITY/TinyWinToast/blob/master/screens/4.png)

5# Text attribute

```python
toast = Toast()
toast.setTitle("TITLE", maxLines=1)
toast.setMessage("MESSAGE", maxLines=1)
toast.addText("from email", placement="attribution", maxLines=1)
toast.setIcon('C:/Users/333da/Desktop/wintoast/0.jpg', crop="circle")
toast.show()
```

![Imgur](https://github.com/J-CITY/TinyWinToast/blob/master/screens/5.png)

6# Toast time 

```python
toast = Toast()
toast.setTitle("TITLE", maxLines=1)
toast.setMessage("MESSAGE", maxLines=1)
toast.setTime("2019-07-13T18:49:37.00Z")
toast.setIcon('C:/Users/333da/Desktop/wintoast/0.jpg', crop="circle")
toast.show()
```

![Imgur](https://github.com/J-CITY/TinyWinToast/blob/master/screens/6.png)

7# Add group text

```python
toast = Toast()
toast.setTitle("TITLE", maxLines=1)
toast.setMessage("MESSAGE", maxLines=1)
toast.addGroupText("Message", maxLines=1, style="base", align="left")
toast.addGroupText("Message", maxLines=1, style="captionSubtle", align="left")
toast.addGroupText("Message", maxLines=1, style="base", align="right")
toast.setIcon('C:/Users/333da/Desktop/wintoast/0.jpg', crop="circle")
toast.show()
```

![Imgur](https://github.com/J-CITY/TinyWinToast/blob/master/screens/7.png)

8# Toast progress

```python
toast = Toast()
toast.setTitle("TITLE", maxLines=1)
toast.setMessage("MESSAGE", maxLines=1)
toast.addProgress(Progress(title="Title", value="0.6", valueStringOverride="15/20", status="Save..."))
toast.setIcon('C:/Users/333da/Desktop/wintoast/0.jpg', crop="circle")
toast.show()
```

![Imgur](https://github.com/J-CITY/TinyWinToast/blob/master/screens/8.png)

Update toast data

```puthon
toast = Toast()
toast.setTitle("TITLE", maxLines=1)
toast.setMessage("MESSAGE", maxLines=1)
toast.setTag("mytag")
toast.setGroup("mygroup")
toast.setProgress(Progress(title="Title", value="0.2", valueStringOverride="15/20", status="Save..."))
toast.setIcon('C:/Users/333da/Desktop/wintoast/0.jpg', crop="circle")
toast.show()

time.sleep(6)

toast.setProgress(Progress(title="Title", value="0.9", valueStringOverride="19/20", status="Save..."))
d = {'progressValue': "0.9", 'progressValueString': "19/20"}
#toast.show() # if you wand update all toast
toast.update(200, d)
```

9# Buttons and inputs

```python
toast = Toast()
toast.setTitle("TITLE", maxLines=1)
toast.setMessage("MESSAGE", maxLines=1)
toast.addInput(Input(inputId="111", intype="text", placeHolderContent="Input text..."))
toast.addInput(Input(inputId="112", intype="selection", selections = [("1","Yes"), ("2","No"), ("3","Maybe")], defaultInput="1"))
toast.addButton(Button(content="Play", activationType="background", arguments="dismiss", pendingUpdate=False))
toast.addButton(Button(content="Pause", activationType="background", arguments="http://www.google.com", pendingUpdate=False))
toast.setIcon('C:/Users/333da/Desktop/wintoast/0.jpg', crop="circle")
toast.show()
```

![Imgur](https://github.com/J-CITY/TinyWinToast/blob/master/screens/9.png)

Also, you can load toast from script, or xml

```python
toast.showFromXml("APP_ID", "XML_STRING")
toast.startFromScript(path_to_script.ps1)
toast.updateFromScript(path_to_script.ps1)
```

Also you can creage Config() and set some params
```python
config = Config()
config.APP_ID = "myApp"
config.DURATION = DURATION_LONG
...
toast = Toast(config)
```

or 

```python
config = Config()
config.APP_ID = "myApp"
config.DURATION = DURATION_LONG
...
toast = Toast()
toast.setConfig(config)
```