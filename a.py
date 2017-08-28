import ROOT
from DataFormats.FWLite import Handle, Events
import math
from filesqun import fileInputNames
#from files_in_PS1p8e34 import fileInputNames
#from files_in_PS1p6e34 import fileInputNames


#list of input files
filesInput = fileInputNames



#auxiliary functions


def checkTriggerIndex(name,index, names):
    if not 'firstTriggerError' in globals():
        global firstTriggerError
        firstTriggerError = True
    if index>=names.size():
        if firstTriggerError:
            for tr in names: print tr
            print
            print name," not found!"
            print
            firstTriggerError = False
            return False
        else:
            return False
    else:
        return True




#Dataset
#from Menu_HLT import groupMap as triggersGroupMap
#from Menu_HLT import datasetMap as  triggersDatasetMap
#from maps_Phlegyas_V16_STEAM_v2 import groupMap as triggersGroupMap
#from maps_Phlegyas_V16_STEAM_v2 import datasetMap as  triggersDatasetMap
from maps_steam_Minotaur_V4 import groupMap   as  triggersGroupMap
from maps_steam_Minotaur_V4 import datasetMap as  triggersDatasetMap



triggerList = []
primaryDatasetList = []
primaryDatasetCounts = {}
datasets = {}

groupList = []
groupCounts = {}
groupCountsShared = {}
groupCountsPure = {}
groups = {}

# Fill triggerList and groupList and primaryDatasetList
#also removing the version number from the trigger
for trigger in triggersDatasetMap.keys():
    #if trigger[:-1] in triggersToRemove: continue
    triggerKey = trigger.rstrip("0123456789")
    datasets.update({str(triggerKey):triggersDatasetMap[trigger]})
    groups.update({str(triggerKey):triggersGroupMap[trigger]})
    if not (trigger in triggerList) : triggerList.append(trigger)
    for dataset in triggersDatasetMap[trigger]:
        if not dataset in primaryDatasetList: primaryDatasetCounts.update({str(dataset):0}) 
        if not dataset in primaryDatasetList: primaryDatasetList.append(dataset)
    for group in triggersGroupMap[trigger]:
        if not group in groupList: groupCounts.update({str(group):0}) 
        if not group in groupList: groupCountsShared.update({str(group):0}) 
        if not group in groupList: groupCountsPure.update({str(group):0}) 
        if not group in groupList: groupList.append(group)





#Handles and labels
triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults::MYHLT")


#Looping over the inputfiles
n = 0
nPassed = 0

#List of triggers
myPaths = []
myPassedEvents = []

nLS = 0


for inputfile in filesInput:

    events = Events (inputfile)

    #Looping over events in inputfile

    runAndLsList = []
    for event in events: 
        #if n == 100000: break
        #taking trigger informations: names, bits and products
        event.getByLabel(triggerBitLabel, triggerBits)
        names = event.object().triggerNames(triggerBits.product())    
        runnbr = event.object().id().run()
        runls = event.object().id().luminosityBlock()
        if runls > 50 or runls < 11: continue  #31-253
        runstr = str((runnbr,runls))
        if not runstr in runAndLsList:
            nLS = nLS +1
            runAndLsList.append(runstr)

        if n<1:
            for name in names.triggerNames():
                #prin tname
                name = str(name)
                if name.startswith("HLT_"):
                    if  not("Beamspot" in name) and not("NoBPTX" in name) and not(name.startswith("HLT_ZeroBias")) and not(name.startswith("HLT_Physics")):
                    #if not(name.startswith("HLT_ZeroBias")) and not(name.startswith("HLT_Physics")) and not("Beamspot" in name):
                        myPaths.append(name)
        #inizialize the number of passed events
            for i in range(len(myPaths)):
                myPassedEvents.append(0)

        iPath = 0       

        #here we initialize the counter per dataset to avoid counting a DS twice
        kPassedEvent = False
        datasetsCountsBool = primaryDatasetCounts.fromkeys(primaryDatasetCounts.keys(),False)
        groupCountsBool = groupCounts.fromkeys(groupCounts.keys(),False)
        myGroupFired = []

        for triggerName in myPaths:
            index = names.triggerIndex(triggerName)
            if checkTriggerIndex(triggerName,index,names.triggerNames()):
                #checking if the event has been accepted by a given trigger
                if triggerBits.product().accept(index):
                    myPassedEvents[iPath]=myPassedEvents[iPath]+1 
                    #we loop over the dictionary keys to see if the paths is in that key, and in case we increase the counter
                    triggerKey = triggerName.rstrip("0123456789")
                    if triggerKey in datasets.keys():
                        for dataset in datasets[triggerKey]:
                            if datasetsCountsBool[dataset] == False :
                                datasetsCountsBool[dataset] = True
                                primaryDatasetCounts[dataset] = primaryDatasetCounts[dataset] + 1
                    if triggerKey in groups.keys():
                        for group in groups[triggerKey]:
                            if group not in myGroupFired: 
                                myGroupFired.append(group)
                                groupCounts[group] = groupCounts[group] + 1

                        



                    if kPassedEvent == False:
                        nPassed = nPassed + 1
                        kPassedEvent = True

            iPath = iPath+1        

        if len(myGroupFired) == 1:
            groupCountsPure[group] = groupCountsPure[group] + 1            

        for group in myGroupFired:
            groupCountsShared[group] = groupCountsShared[group] + 1./len(myGroupFired)

            
        n = n+1




#Printing output

print nLS, n, nPassed
#for run 296786
#scalingFactor = round((3352./23.31)*250*(55./46)*(2544./973.)/float(n) ,2)

#for run 297219
#scalingFactor  = round((7*75*107)/float(n) ,2)

#for run 297674
#scalingFactor = round((8.6*75*107)/float(n) ,2)
#scalingFactor = 2544./51. * 55./39.7 * 8./23.31
#127.8*8*(2544./51.)*(55./39.69)

#for run 299420
##scalingFactor =  LHC Fill /nCollidingBunches *  ?/? * ?/LumiSegmentNr
#SF = ( #bunches(expected) / #bunches(in processed data) ) x ( PU(expected) / PU(in processed data) ) x ( PS(HLT_Physics_partX_v) / T(duration of a single LS = 23.31 seconds) )
#SF2 = ( Lumi(expected) / Lumi(in processed data) ) x ( PS(HLT_Physics_partX_v) / T(duration of a single LS = 23.31 seconds) )
#scalingFactor = 2544./2543 * 44./? * 7/23.31
#scalingFactor = 2448./2543 * 44./39.31 * 360/23.31
# SF2 = 1.6e34/1.4827e34*360/23.31
#scalingFactor = 1.6e34/1.27e34*360/23.31
#scalingFactor = 1.8e34/1.27e34*360/23.31
scalingFactor =  360/23.31
scalingFactor = scalingFactor*1./nLS

totalRate = float(nPassed)*scalingFactor


path_file = open('output.path.csv', 'w')

path_file.write("Path, Counts, Rate (Hz)\n")
path_file.write("Total Rate (Hz) , , " + str(totalRate))
path_file.write('\n')
for i in range(len(myPaths)):
    print myPaths[i], myPassedEvents[i], myPassedEvents[i]*scalingFactor                                                                                                         
    path_file.write('{}, {}, {}'.format(myPaths[i], myPassedEvents[i], round(myPassedEvents[i]*scalingFactor, 2)))
    path_file.write('\n')

dataset_file = open('output.dataset.csv', 'w')

dataset_file.write("Dataset, Counts, Rate (Hz)\n")
for key in primaryDatasetCounts.keys():
    dataset_file.write(str(key) + ", " + str(primaryDatasetCounts[key]) +", " + str(round(primaryDatasetCounts[key]*scalingFactor, 2)))
    dataset_file.write('\n')


group_file = open('output.group.csv','w')
group_file.write('Groups, Counts, Rate (Hz)\n')
for key in groupCounts.keys():
    group_file.write(str(key) + ", " + str(groupCounts[key]) +", " + str(round(groupCounts[key]*scalingFactor, 2)))
    group_file.write('\n')

group_exclusive_file = open('output.group_exclusive.csv', 'w')
group_exclusive_file.write('Groups Pure, Counts, Rate (Hz)\n')
for key in groupCountsPure.keys():
    group_exclusive_file.write(str(key) + ", " + str(groupCountsPure[key]) +", " + str(round(groupCountsPure[key]*scalingFactor, 2)))
    group_exclusive_file.write('\n')
group_exclusive_file.write('Groups Shared, Counts, Rate (Hz)\n')
for key in groupCountsShared.keys():
    group_exclusive_file.write(str(key) + ", " + str(groupCountsShared[key]) +", " + str(round(groupCountsShared[key]*scalingFactor, 2)))
    group_exclusive_file.write('\n')


'''
print "Path, Counts, Rate (Hz)"
for i in range(len(myPaths)):
    #print myPaths[i], myPassedEvents[i], myPassedEvents[i]*scalingFactor
    print '{}, {}, {}'.format(myPaths[i], myPassedEvents[i], myPassedEvents[i]*scalingFactor) 

print "Total Rate (Hz) ",",",",",float(totalRate)


print "Dataset, Counts, Rate (Hz)"
for key in primaryDatasetCounts.keys():
    print key,",", primaryDatasetCounts[key] ,",",float(primaryDatasetCounts[key]*scalingFactor)


print "Groups, Counts, Rate (Hz)"
for key in groupCounts.keys():
    print key,",", groupCounts[key] ,",",float(groupCounts[key]*scalingFactor)

print "Groups Pure, Counts, Rate (Hz)"
for key in groupCountsPure.keys():
    print key,",", groupCountsPure[key] ,",",round(float(groupCountsPure[key]*scalingFactor),2)

print "Groups Shared, Counts, Rate (Hz)"
for key in groupCountsShared.keys():
    print key,",", round(groupCountsShared[key],2) ,",",round(float(groupCountsShared[key]*scalingFactor),2)

'''


    





                          


