# coding=utf-8

############################################################################
############### 4-digit Motor Task & Resting-state EEG #####################
###################### Written by Tiziano Suran ############################
############################################################################

from psychopy import visual, data, core, event, gui, parallel
import random
import datetime #library to get the current date
import pyglet
import csv
import itertools
import os
import numpy as np
import pyxid


try:
    parallel.setPortAddress(888) #address for parallel port on many machines = 888
except:
    pass

# get demographics
def demographics():
    global subj, age, gender
    myDlg = gui.Dlg(title="Info")
    myDlg.addField(u'Code:')
    myDlg.addField(u'Age:')
    myDlg.addField(u'Sex:', choices=[u"F", u"M"])
    myDlg.show()  # show dialog and wait for OK or Cancel
    if myDlg.OK:  # or if ok_data is not None
        try:
            subj = str(myDlg.data[0])
            age = str(myDlg.data[1])
            gender = str(myDlg.data[2])
            return subj, age, gender
        except ValueError:
            demographics()
    else:
        print(u'user cancelled')

demographics()
subj = int(subj)
age = age
gender = gender
print subj, age, gender

#--------------------------------------------------------------------------#
#------------------------------Parameters----------------------------------#
#--------------------------------------------------------------------------#
win = visual.Window([1200,800], fullscr = 0, units = 'pix', color='gray', screen = 0) #set the window's size and whether you want the FULLSCREEN
clock = core.Clock() #set the clock
clock4 = core.Clock()
tmpData = str(datetime.datetime.now())[0:10] #get the current date
tmpOra = str(datetime.datetime.now())[11:19]
tmpOra = tmpOra.replace(":","-")

# general stimuli
fix = visual.TextStim(win,text="+",units = "pix", height = 88,pos=(0,5), font = "lucida sans typewriter", color = 'black', alignHoriz='center', alignVert='center')
rest_fix = visual.TextStim(win,text="x",units = "pix", height = 88,pos=(0,5), font = "lucida sans typewriter", color = 'black', alignHoriz='center', alignVert='center')

pause = visual.TextStim(win, font = "lucida sans typewriter",
text=u"The break is over.\n\nPress a number to continue",
    units = "pix", height = 30,pos=(0,0), color = 'black', alignHoriz='center', alignVert='center')


#task parameters
restTime = 120 #resting-state time in seconds put 120 (2 min)
fixFrames = 42 #700 ms
tgtFrames = 6 #100 ms
blankFrames = 12 #200 ms
maxRest0 = 300 # max initial rest
maxTime = 10
numtrials = 40 # number of trials (max = 40)

# triggers
restingTrig = [41,42,43,44,45,46,47,48,49,50]

#create save folder
if not os.path.exists("Results"):
    os.makedirs("Results")

#------------CREATE STIMULI
digits = ['1','2','3','4']
stimuli = []

for n in range(5):
    random.shuffle(digits)
    temp = list(digits)
    stimuli.append(temp)



### define functions
def MotorTask(stim):
    global resp,RT, blockCounter

    random.shuffle(stim)
    tgt = visual.TextStim(win, font = "lucida sans typewriter", text = "target", units = "pix", height = 50,pos=(0,0), color = 'black', alignHoriz='center', alignVert='center')
    core.wait(1)
#task
    trialcounter=0
    for i in stim:
        tgt.setText("%s%s%s%s"%(i[0],i[1],i[2],i[3]))
        tetracounter=0
        trialcounter+=1
        RT4 = []
        acc4=[]

        win.flip()
        core.wait(float(random.randrange(1500,2500,100))/1000.0) #-random jitter 1500-2500 ms by 100 ms
        
        event.clearEvents()

        clock.reset()
        clock4.reset()
        tgt.setAutoDraw(1)
        while 1:
            win.flip()
            if clock.getTime()>=2:
                tgt.setAutoDraw(0)
            resp = event.getKeys(keyList=['1','2','3','4'])
            if resp != []:
                RT0 = clock4.getTime()
                RT = ('%.4f' % RT0).replace('.',',')
                RT4.append(RT)
                if resp[0] == i[tetracounter]:
#                    tgt.setAutoDraw(0)
                    acc = 1
                    print "correct", RT
                    win.flip()
                else:
#                    tgt.setAutoDraw(0)
                    acc = 0
                    print "error",RT
                    win.flip()
                acc4.append(acc)
                clock4.reset()
                tetracounter += 1
                print tetracounter
                event.clearEvents()
            if tetracounter == 4:
                tgt.setAutoDraw(0)
                win.flip()
                break
            if event.getKeys(keyList=['escape']):
                data_frame.close()
                try:
                    parallel.setData(0)
                except:
                    pass
                core.quit()
            if clock.getTime() >=maxTime:#    remove if not pretesting
                resp = ['X']
                tgt.setAutoDraw(0)
                if len(RT4)<4:
                    for el in range(4-len(RT4)):
                        RT4.append(0)
                        acc4.append('miss')
                #print acc,RT
                win.flip()
                break

        for n in range(4):
            data_frame.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"%
            (tmpData,tmpOra,subj,age,gender,i[n],(n+1),trialcounter,RT4[n],acc4[n],"bo",blockCounter))
        win.flip()
    
def RestState():
    global data_frame, restTime, blockCounter, restingTrig

    data_frame = open(data_frame.name,"a")
    data_frame.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"%
    (tmpData,tmpOra,subj,age,gender,"REST","REST","REST","REST","REST",restingTrig[blockCounter-1],blockCounter))
    
    rest_state_intro = visual.TextStim(win, font = "lucida sans typewriter", text = u"The break will now start.\n\
    \nContact the experimenter.", units = "pix", height = 30,pos=(0,0), color = 'black', alignHoriz='center', alignVert='center')
    rest_state_intro.draw()
    win.flip()
    event.waitKeys(keyList=['return'])

    rest_state_intro.setText(u"The break will start in a couple of seconds.\n\
    \nRelax and stare at the 'X' at the center of the screen.")
    rest_state_intro.draw()
    win.flip()
    core.wait(10)
    event.clearEvents()
    
    rest_fix = visual.TextStim(win,text="x",units = "pix", height = 88,pos=(0,5), font = "lucida sans typewriter", color = 'black', alignHoriz='center', alignVert='center')
    rest_fix.draw()
    try:
        parallel.setData(restingTrig[blockCounter-1]) #trigger rest_state-------------------------------------------RM
    except:
        pass
    
    win.flip()
    clock.reset()
    while 1:
        if clock.getTime() >= restTime:
            core.wait(0.1)
            try:
                parallel.setData(40)
            except:
                pass
            core.wait(0.2)
            try:
                parallel.setData(0)
            except:
                pass
            break
        if event.getKeys(keyList=['return']):
            try:
                parallel.setData(40)
            except:
                pass
            core.wait(0.2)
            try:
                parallel.setData(0)
            except:
                pass
            break
        if event.getKeys(keyList=['escape']):
            data_frame.close()
            try:
                parallel.setData(0)
            except:
                pass
            core.quit()


def istruzioni(win, testo, continueButtons=['1','2','3','4'], waitResp=1, col='black'):
    istruzioni = visual.TextStim(win, text = testo, units = "pix", font = "lucida sans typewriter", height = 23, color = col, alignHoriz='center', alignVert='center', wrapWidth = 700)
    if len(continueButtons)==1:
        spazio = visual.TextStim(win, text = "Press %s to continue"%("SPACE" if continueButtons[0]=="space" else continueButtons[0].upper()), units = "pix", height = 28, font = "lucida sans typewriter",
        color = col, alignHoriz='center', pos=(0,-320))
    elif len(continueButtons)>=2:
        spazio = visual.TextStim(win, text = "Press a number to continue", units = "pix", height = 22, font = "lucida sans typewriter",
        color = col, alignHoriz='center', pos=(0,-320))
    istruzioni.draw()
    spazio.draw()
    win.flip()
    core.wait(waitResp)
    event.clearEvents()
    return event.waitKeys(keyList = continueButtons) #wait button press


#----------EVENTS---------#
#create save file
data_frame = open("Results/%s_%s_Motor_Task_Subj_%s.csv"%(tmpData,tmpOra,subj),"a")
data_frame.write("date;time;Subject;Age;Gender;Target;Trial4;TrialNum;RT;accuracy;Hand;blockCounter\n")


# resting state 0
event.Mouse(visible=0)
try:
    parallel.setData(0)
except:
    pass
fix.draw()
win.flip()
event.waitKeys(keyList=['return'])
try:
    parallel.setData(1)
except:
    pass
event.clearEvents()
clock.reset()

while 1:
    rest_fix.draw()
    win.flip()
    if clock.getTime() >= maxRest0:
        try:
            parallel.setData(0)
        except:
            pass
        break
    if event.getKeys(keyList=['escape']):
        try:
            parallel.setData(0)
        except:
            pass
        win.close()
        core.quit()
    if event.getKeys(keyList=['return']):
        try:
            parallel.setData(0)
        except:
            pass
        break
core.wait(0.1)


#ISTRUZIONI PRATICA
try:
    parallel.setData(31)
except:
    pass

istruzioni(win,
u"You will see 4-digit numbers, with each digit going from 1 to 4. \
\n\
Your task is to digit each number as fast as possible using your left hand, even after the number disappears.\n\
Index = 1; Middle = 2; Ring = 3; Pinky = 4\n\
\n\
The practice will now start.")

#core.wait(float(random.randrange(500,1500,100))/1000) #-random wait jitter 800-1200 ms by 100 ms
try:
    parallel.setData(30)
except:
    pass
core.wait(0.2)
try:
    parallel.setData(0)
except:
    pass

blockCounter=0
MotorTask(stimuli[:numtrials])

try:
    parallel.setData(31)
except:
    pass
#ISTRUZIONI TASK
istruzioni(win,
u"The practice is over.\n\n\
IMPORTANT:\n\
-digit the number as fast as possible, even after its disappearance.\n\
-during the occasional breaks, you will have to relax and stare at an 'x'.\n\n\
The main task will start now.")
try:
    parallel.setData(30)
except:
    pass
core.wait(0.1)
try:
    parallel.setData(0)
except:
    pass


#MAIN TASK
for counter in range(len(restingTrig)):
    blockCounter += 1
    random.shuffle(stimuli)
    core.wait(0.2)
    fix.draw()
    win.flip()
    core.wait(0.5)
    win.flip()
    MotorTask(stimuli[:numtrials])
    RestState()
    core.wait(0.1)
    if blockCounter !=10:
        pause.draw()  #end of resting-state
        win.flip()
        event.waitKeys(keyList=['1','2','3','4'])
        core.wait(0.1)


#BYE
data_frame.close()
endInstr = visual.TextStim(win, font = "lucida sans typewriter", text = u"The experiment is over. Contact the experimenter.",
units = "pix", height = 30,pos=(0,0), color = 'black', alignHoriz='center', alignVert='center')
endInstr.draw()
win.flip()
event.waitKeys(keyList=['return'])
win.close()
core.quit()
