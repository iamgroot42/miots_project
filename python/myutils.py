"""
  Based on https://github.com/LauraWartschinski/VulnerabilityDetection
"""

import builtins
import keyword
import os
from PIL import Image
from PIL import ImageDraw
from termcolor import colored


def findComments(sourcecode):
  """
    Finds all comments in the source code.
  """
  commentareas = []

  inacomment = False
  commentstart = -1
  commentend = -1

  for pos, sc in enumerate(sourcecode):
    if sc == "#":
      if not inacomment:
        commentstart = pos 
        inacomment = True

    if sc == "\n":
      if inacomment:
        commentend = pos
        inacomment = False

    if commentstart >= 0 and commentend >= 0:
      t = [commentstart, commentend]
      commentareas.append(t)
      commentstart = -1
      commentend = -1

  return commentareas


def findposition(badpart,sourcecode):
  splitchars = ["\t", "\n", " ", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  pos = 0
  matchindex = 0
  inacomment = False
  bigcomment = False
  bigcomment2 = False
  startfound = -1
  endfound = -1
  position = []
  end = False
  last = 0
  
  while "#" in badpart:
    f = badpart.find("#")
    badpart = badpart[:f]

  b = badpart.lstrip()
  if len(b) < 1:
    return[-1,-1]


  while(not end):

    if not inacomment:
      last = pos-1
    
    if pos >= len(sourcecode):
      end = True
      break
    
    if sourcecode[pos] == "\n":
      inacomment = False
      
    if sourcecode[pos] == "\n" and (sourcecode[pos-1] == "\n" or sourcecode[last] == " "):
      pos = pos +1
      continue
      
    if sourcecode[pos] == " " and (sourcecode[pos-1] == " " or sourcecode[last] == "\n"):
     # print("one further")
      pos = pos +1
      continue
      
    if sourcecode[pos] == "#":
      
      inacomment = True
      
    # if (False):
      
    #                   print("---------------------------------")
    #                   string1 = ""
    #                   string2 = ""
    #                   for i in range(0,pos):
    #                     string1 = string1 + sourcecode[i]

    #                   for i in range(pos+1,len(sourcecode)):
    #                     string2 = string2 + sourcecode[i]
                        
    #                   print(string1 + "[" + sourcecode[pos] + "]" + string2)
    #                   print("---------------------------------")


    #                   string1 = ""
    #                   string2 = ""
                      
    #                   for i in range(0,matchindex):
    #                     string1 = string1 + badpart[i]

    #                   for i in range(matchindex+1,len(badpart)):
    #                     string2 = string2 + badpart[i]
                        
    #                   print(string1 + "[" + badpart[matchindex] + "]" + string2)
  
    #                   print("---------------------------------")
                

    if not inacomment: # and not bigcomment and not bigcomment2:
      a = sourcecode[pos]
      if a == "\n":
        a = " "
      b = badpart[matchindex]
      
      c = ""
      if matchindex > 0:
        c = badpart[matchindex-1]
      
      d = ""
      if matchindex < len(badpart)-2:
        d = badpart[matchindex+1]
        
      if (a != b) and (a == " " or a == "\n") and ((b in splitchars) or (c in splitchars)):
        pos = pos+1
        continue
      
      if (a != b) and (b == " " or b == "\n"):
        #print("here")
        if (c in splitchars or d in splitchars):
          #print("here2")
          if (matchindex < len(badpart)-1):
            matchindex = matchindex + 1
            continue
        
      if a == b:
          if matchindex == 0:
            startfound = pos
          matchindex = matchindex + 1
          
      else:
          #print("\n>>no match" )
          matchindex = 0
          startfound = -1
        
      if matchindex == len(badpart):
        endfound = pos
        break
        
    if pos == len(sourcecode):
      end = True
    pos = pos + 1
  
  position.append(startfound)
  position.append(endfound)
  
  if endfound < 0:
    startfound = -1
    
  if endfound < 0 and startfound < 0: #and not "#" in badpart and not '"""' in badpart and not "'''" in badpart:
    # print(sourcecode)
    # print(":::::::::::")
    # print(badpart)
    # print("-----------------")
    return[-1,-1]
  return position


def findpositions(badparts, sourcecode):
  positions = []

  for bad in badparts:

    if "#" in bad:
      find = bad.find("#")
      bad = bad[:find]

    place = findposition(bad,sourcecode)
    if place != [-1,-1]:
      positions.append(place)

  return positions
  

def nextsplit(sourcecode,focus):
  splitchars = [" ","\t","\n", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  for pos in range(focus+1, len(sourcecode)):
      if sourcecode[pos] in splitchars:
        return pos
  return -1

def previoussplit(sourcecode,focus):
  splitchars = [" ","\t","\n", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  pos = focus-1
  while(pos >= 0):
      if sourcecode[pos] in splitchars:
        return pos
      pos = pos-1
  return -1


def getcontextPos(sourcecode,focus,fulllength):

  startcontext = focus
  endcontext = focus
  if focus > len(sourcecode)-1:
    return None

  start = True
  
  while not len(sourcecode[startcontext:endcontext]) > fulllength:
    
    if previoussplit(sourcecode,startcontext) == -1 and nextsplit(sourcecode,endcontext) == -1:
      return None
    
    if start:
      if previoussplit(sourcecode,startcontext) > -1:
        startcontext = previoussplit(sourcecode,startcontext)
      #print("new start: " + str(startcontext))
      start = False
    else:
      if nextsplit(sourcecode,endcontext) > -1:
        endcontext = nextsplit(sourcecode,endcontext)
      start = True

  return [startcontext,endcontext]

def getcontext(sourcecode,focus,fulllength):
  
  startcontext = focus
  endcontext = focus
  if focus > len(sourcecode)-1:
    return None

  start = True
  while not len(sourcecode[startcontext:endcontext]) > fulllength:
    
    if previoussplit(sourcecode,startcontext) == -1 and nextsplit(sourcecode,endcontext) == -1:
      return None
    
    if start:
      if previoussplit(sourcecode,startcontext) > -1:
        startcontext = previoussplit(sourcecode,startcontext)
      start = False
    else:
      if nextsplit(sourcecode,endcontext) > -1:
        endcontext = nextsplit(sourcecode,endcontext)
      start = True

  return sourcecode[startcontext:endcontext]
  

def getblocks(sourcecode, badpositions, step, fulllength):
      blocks = []
       
      focus = 0
      lastfocus = 0
      while (True):
        if focus > len(sourcecode):
          break
        
        focusarea = sourcecode[lastfocus:focus]
                
        if not (focusarea == "\n"):
              
            middle = lastfocus+round(0.5*(focus-lastfocus))              
            context = getcontextPos(sourcecode,middle,fulllength)
            #print([lastfocus,focus,len(sourcecode)])
            
            
            if context is not None:
              
              
                
              vulnerablePos = False
              for bad in badpositions:
                    
                  if (context[0] > bad[0] and context[0] <= bad[1]) or (context[1] > bad[0] and context[1] <= bad[1]) or (context[0] <= bad[0] and context[1] >= bad[1]):
                    vulnerablePos = True
            
                  
              q = -1
              if vulnerablePos:
                q = 0
              else:
                q = 1
              
              
              singleblock = []
              singleblock.append(sourcecode[context[0]:context[1]])
              singleblock.append(q)
                
              already = False
              for b in blocks:
                if b[0] == singleblock[0]:
                #  print("already.")
                  already = True
                  
              if not already:
                blocks.append(singleblock)


        if ("\n" in sourcecode[focus+1:focus+7]):
          lastfocus = focus
          focus = focus + sourcecode[focus+1:focus+7].find("\n")+1
        else:
          if nextsplit(sourcecode,focus+step) > -1:
            lastfocus = focus
            focus = nextsplit(sourcecode,focus+step)
          else:
            if focus < len(sourcecode):
              lastfocus = focus
              focus = len(sourcecode)
            else:
              break

      
      return blocks


def getBadpart(change):
  """
    Extract good/bad examples from code diff
  """

  removal = False
  lines = change.split("\n")
  for l in lines:
    if len(l) > 0 and l[0] == "-":
      removal = True

  if not removal:
    return None

  badexamples = []
  goodexamples = []

  for line in lines:
    line = line.lstrip()
    if len(line.replace(" ","")) > 1:
        if line[0] == "-":
          if not "#" in line[1:].lstrip()[:3] and not "import os" in line:
            badexamples.append(line[1:])
        if line[0] == "+":
          if not "#" in line[1:].lstrip()[:3] and not "import os" in line:
            goodexamples.append(line[1:])

  if len(badexamples) == 0:
    return None

  return [badexamples, goodexamples]
    

def getTokens(change):
  """
    Get tokens from code string
  """
  tokens = []

  replacements = [
      (" .", "."),
      (" ,", ","),
      (" )", ")"),
      (" (", "("),
      (" ]", "]"),
      (" [", "["),
      (" {", "{"),
      (" }", "}"),
      (" :", ":"),
      ("- ", "-"),
      ("+ ", "+"),
      (" =", "="),
      ("= ", "=")
  ]

  for before, after in replacements:
    change = change.replace(before, after)

  splitchars = [" ","\t","\n", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  start = 0
  end = 0
  for i in range(0, len(change)):
    if change[i] in splitchars:
      if i > start:
        start = start+1
        end = i
        if start == 1:
          token = change[:end]
        else:
          token = change[start:end]
        if len(token) > 0:
          tokens.append(token)
        tokens.append(change[i])
        start = i
  return(tokens)


def _removeDoubleSeperators(tokenlist):
  """
    Remove double seperators from list of tokens
  """
  last = ""
  newtokens = []
  for token in tokenlist:
    if token == "\n":
      token = " "
    if len(token) > 0:
      if not ((last == " ") and (token == " ")):
        newtokens.append(token)

      last = token
        
  return(newtokens)
  

def removeDoubleSeperatorsString(string):
  """
    Remove double seperators from string (untokenized)
  """
  return ("".join(_removeDoubleSeperators(getTokens(string))))


def isEmpty(code):
  """
    Check if code is empty
  """
  token = getTokens(stripComments(code))
  for t in token:
    if (t != "\n" and t != " "):
      return False
  return True


def is_builtin(name):
    return name in builtins.__dict__


def is_keyword(name):
      return name in keyword.kwlist


def removeTripleN(tokenlist):
    secondlast = ""
    last = ""
    newtokens = []
    for token in tokenlist:
      if len(token) > 0:
        
        if ((secondlast == "\n") and (last == "\n") and (token == "\n")):
          #print("too many \\n.")
          o = 1 #noop
        else:
          newtokens.append(token)
          
        
        thirdlast = secondlast
        secondlast = last
        last = token
        
    return(newtokens)


def getgoodblocks(sourcecode,goodpositions,fullength):
  blocks = []
  if (len(goodpositions) > 0):
    for g in goodpositions:
     # print("g " + str(g))
      if g != []:
        focus = g[0]
        while (True):
          if focus >= g[1]:
            break
          
          context = getcontext(sourcecode, focus, fullength)
          
          if context is not None:
            singleblock = []
            singleblock.append(context)
            singleblock.append(1)
              
            already = False
            for b in blocks:
              if b[0] == singleblock[0]:
              #  print("already.")
                already = True
                  
            if not already:
              blocks.append(singleblock)
              
            if nextsplit(sourcecode,focus+15) > -1:
              focus = nextsplit(sourcecode,focus+15)
            else:
              break

  return blocks


def stripComments(code):
  """
    Remove comments from code
  """

  withoutComments = ""
  lines = code.split("\n")
  withoutComments = ""
  for c in lines:
    if "#" in c:
      position = c.find("#")
      c = c[:position]
    withoutComments = withoutComments + c + "\n"

  return withoutComments


def getblocksVisual(mode,sourcecode, badpositions,commentareas, fulllength,step, nr,w2v_model,model,threshold,name):

      word_vectors = w2v_model.wv
      
      ypos = 0
      xpos = 0
      
      lines = (sourcecode.count("\n"))
      #print("lines: " + str(lines))
      img = Image.new('RGBA', (2000, 11*(lines+1)))
      color = "white"
      
      blocks = []
       
      focus = 0
      lastfocus = 0
      
      string = ""
      
      trueP = False
      falseP = False
      
      while (True):
        if focus > len(sourcecode):
          break
        
        
        
        comment = False
        for com in commentareas:
          
          if (focus >= com[0] and focus <= com[1] and lastfocus >= com[0] and lastfocus < com[1]):
                focus = com[1]
                #print("within")
                comment = True
          if (focus > com[0] and focus <= com[1] and  lastfocus < com[0]):
              focus = com[0]
              #print("before")
              comment = False                   
          elif (lastfocus >= com[0] and lastfocus < com[1] and focus > com[1]):
              focus = com[1]
              #print("up to the end")
              comment = True
      
        #print([lastfocus,focus,comment, "["+sourcecode[lastfocus:focus]+"]"])
        focusarea = sourcecode[lastfocus:focus]
     
        if(focusarea == "\n"):
          string = string + "\n"
          
        else:
          if comment:
              color = "grey"
              string = string + colored(focusarea,'grey')
          else:
              
              
              middle = lastfocus+round(0.5*(focus-lastfocus))              
              context = getcontextPos(sourcecode,middle,fulllength)
              
              
              if context is not None:
              
                vulnerablePos = False
                for bad in badpositions:
                    if (context[0] > bad[0] and context[0] <= bad[1]) or (context[1] > bad[0] and context[1] <= bad[1]) or (context[0] <= bad[0] and context[1] >= bad[1]):
                      vulnerablePos = True
                      
                predictionWasMade = False
                text = sourcecode[context[0]:context[1]].replace("\n", " ")
                token = getTokens(text)
                if (len(token) > 1):                  
                  vectorlist = []                  
                  for t in token:
                    if t in word_vectors.vocab and t != " ":
                      vector = w2v_model[t]
                      vectorlist.append(vector.tolist())   
                      
                  if len(vectorlist) > 0:
                      p = predict(vectorlist,model)
                      if p >= 0:
                        predictionWasMade = True
                        
                      #  print(p)
                        if vulnerablePos:
                          if p > 0.5:
                            color = "royalblue"
                            string = string + colored(focusarea,'cyan')
                          else:
                            string = string + colored(focusarea,'magenta')
                            color = "violet"
                            
                        else:
                          
                        
                          if p > threshold[0]:
                            color = "darkred"
                          elif p >  threshold[1]:
                            color = "red"
                          elif p >  threshold[2]:
                            color = "darkorange"
                          elif p >  threshold[3]:
                            color = "orange"
                          elif p >  threshold[4]:
                            color = "gold"
                          elif p >  threshold[5]:
                            color = "yellow"
                          elif p >  threshold[6]:
                            color = "GreenYellow"
                          elif p >  threshold[7]:
                            color = "LimeGreen"
                          elif p >  threshold[8]:
                            color = "Green"
                          else:
                            color = "DarkGreen"
                
                          if p > 0.8:
                            string = string + colored(focusarea,'red')
                          elif p > 0.5:
                            string = string + colored(focusarea,'yellow')
                          else:
                            string = string + colored(focusarea,'green')
                            
                if not predictionWasMade:
                  string = string + focusarea
              else:
                string = string + focusarea
                
        
        
            
        try:
          if len(focusarea) > 0:
            d = ImageDraw.Draw(img)
            if focusarea[0] == "\n":
              ypos = ypos + 11
              xpos = 0
              d.text((xpos, ypos), focusarea[1:], fill=color)
              xpos = xpos + d.textsize(focusarea)[0]
            else:
              d.text((xpos, ypos), focusarea, fill=color)
              xpos = xpos + d.textsize(focusarea)[0]

        except Exception as e:
          print(e)

        if ("\n" in sourcecode[focus+1:focus+7]):
          lastfocus = focus
          focus = focus + sourcecode[focus+1:focus+7].find("\n")+1
        else:
          if nextsplit(sourcecode,focus+step) > -1:
            lastfocus = focus
            focus = nextsplit(sourcecode,focus+step)
          else:
            if focus < len(sourcecode):
              lastfocus = focus
              focus = len(sourcecode)
            else:
              break
      
      for i in range(1,100):
        if not os.path.isfile('demo_' + mode + "_" + str(i) +"_"+ name + '.png'):
                img.save('demo_' + mode + "_" + str(i) + "_" + name + '.png')    
                print("saved png.")
                break
      return blocks


def getIdentifiers(mode, nr):
  if mode == "sql":
    if nr == "1":
      rep = "instacart/lore"
      com = "a0a5fd945a8bf128d4b9fb6a3ebc6306f82fa4d0"
      myfile = "/lore/io/connection.py"

  result = []
  result.append(rep)
  result.append(com)
  result.append(myfile)
  return result


def getFromDataset(identifying,data):
  
  result = []
  rep = identifying[0]
  com = identifying[1]
  myfile = identifying[2]
  #print("\n")
  #print("getting from dataset: " + rep + "/commit/" + com + " " + myfile)
  repfound = False
  comfound = False
  filefound = False
  for r in data:
        if  "https://github.com/"+rep ==r:
         #   print("  found repository.")
            repfound = True
            for c in data[r]:
              if c == com:
          #      print("    found commit.")
                comfound = True
                if "files" in data[r][c]:
                    for f in data[r][c]["files"].keys():
                      if myfile == f:  
                          filefound = True
           #               print("      found file")
                          if "source" in data[r][c]["files"][f]:                          
                              allbadparts = []
                              sourcecode = data[r][c]["files"][f]["source"]
                              sourcefull = data[r][c]["files"][f]["sourceWithComments"]
                              
                              
                              for change in data[r][c]["files"][f]["changes"]:
                                badparts = change["badparts"]
                                
                                if (len(badparts) < 20):
                                  for bad in badparts:
                                    pos = findposition(bad,sourcecode)
                                    if not -1 in pos:
                                      allbadparts.append(bad)
                                      
                                                                  
                              result.append(sourcefull)
                              result.append(allbadparts)
                              
                              if not repfound:
                                print("Rep found " + str(repfound))
                              elif not comfound:
                                print("Com found " + str(comfound))
                              elif not filefound:
                                print("File found " + str(filefound))
                              return(result)
                        

  if not repfound:
    print("Rep found " + str(repfound))
  elif not comfound:
    print("Com found " + str(comfound))
  elif not filefound:
    print("File found " + str(filefound))
  return []


def get_filename_from_url(url):
  """
    Filename corresponding to a PR link
  """
  prefix = "https://github.com/"
  url = url.replace(prefix, "")
  url = url.replace("/", "_")
  return url
