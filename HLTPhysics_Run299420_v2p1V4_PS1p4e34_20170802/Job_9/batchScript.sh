#!/bin/bash
#BSUB -q 8nm
echo 'environment:'
echo
env
ulimit -v 5000000
echo 'copying job dir to worker'
cd $LS_SUBCWD
eval `scramv1 ru -sh`
#cmsenv
cd -
cp -rf $LS_SUBCWD .
ls
cd `find . -type d | grep /`
echo 'running'
cmsRun run_cfg.py
echo
echo 'sending the job directory back'
cp hlt.root /eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/xulyu/HLTPhysics_Run299420_v2p1V4_PS1p4e34_20170802/hlt_9.root
