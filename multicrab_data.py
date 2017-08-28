name = 'HLTPhysics_Run299420_v2p1V4_PS1p4e34_20170802_V3'
steam_dir = 'xulyu/'
#running_options = []
runATCAF = False

eventsPerJob = 5000
nevents = -1 
mask = 'json_299420_LS11to50.txt'
#mask = '/afs/cern.ch/work/t/tosi/public/STEAM/json/2e34_v1p0p2_cleaned_PU44to47.json'
#'/afs/cern.ch/work/d/dbeghin/Work/Rates/2017_runs_and_MC/2017jun/RateEstimate_HLTPhysics_2017jun13/comparison_json.json'
#'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/DCSOnly/json_DCSONLY.txt'

# Name of input datasets
dataset = {
'HLTPhysics1' : '/ParkingHLTPhysics1/Run2017C-v1/RAW',
'HLTPhysics2' : '/ParkingHLTPhysics2/Run2017C-v1/RAW',
'HLTPhysics3' : '/ParkingHLTPhysics3/Run2017C-v1/RAW',
'HLTPhysics4' : '/ParkingHLTPhysics4/Run2017C-v1/RAW',
'HLTPhysics5' : '/ParkingHLTPhysics5/Run2017C-v1/RAW',
'HLTPhysics6' : '/ParkingHLTPhysics6/Run2017C-v1/RAW',
'HLTPhysics7' : '/ParkingHLTPhysics7/Run2017C-v1/RAW',
'HLTPhysics8' : '/ParkingHLTPhysics8/Run2017C-v1/RAW',
}

# Input datasets to process
listOfSamples = [
'HLTPhysics1',
'HLTPhysics2',
'HLTPhysics3',
'HLTPhysics4',
'HLTPhysics5',
'HLTPhysics6',
'HLTPhysics7',
'HLTPhysics8',
]

if __name__ == '__main__':

   from CRABClient.UserUtilities import config
   config = config()

   from CRABAPI.RawCommand import crabCommand
   from multiprocessing import Process

   def submit(config):
       res = crabCommand('submit', config = config)

   config.General.workArea = 'crab_'+name
   config.General.transferLogs = True

   config.JobType.pluginName = 'Analysis'
   config.JobType.psetName = 'hlt_Minotaur_v2p1V4_PS1p4e34.py'
   config.JobType.maxMemoryMB = 3000
   config.JobType.numCores = 4
   #config.JobType.inputFiles = ['/afs/cern.ch/user/s/sdonato/AFSwork/public/genJetPtHatPU/0.txt']                                                                                
   config.JobType.outputFiles = ['hlt.root']
   #config.JobType.pyCfgParams = running_options

   config.Data.inputDBS = 'global'
   config.Data.splitting = 'EventAwareLumiBased'
   config.Data.publication = False
   config.Data.totalUnits = nevents
   config.Data.outLFNDirBase = '/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/' + steam_dir + '/' + name + '/'

   config.Site.storageSite = 'T2_CH_CERN'
   #config.Site.blacklist = ['T2_BR_SPRACE', 'T2_US_Wisconsin', 'T1_RU_JINR', 'T2_RU_JINR', 'T2_EE_Estonia']                                                                      
   if runATCAF :
      config.Site.whitelist = ['T3_CH_CERN_CAF']
      config.Site.ignoreGlobalBlacklist = True
      config.Data.ignoreLocality = True

   for sample in listOfSamples:

      config.General.requestName = sample
      config.Data.inputDataset = dataset[sample]
      config.Data.unitsPerJob = eventsPerJob#[sample]
      config.Data.outputDatasetTag = name+'_'+sample
      config.Data.lumiMask = mask                                                                                                                                                
      p = Process(target=submit, args=(config,))
      p.start()
      p.join()

