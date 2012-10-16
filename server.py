#!/usr/bin/env python
# version 2.1

import os
import engineOil

engineOilObj =  engineOil.engineOil()

if engineOilObj.folder == "saturday": 
    engineOilObj.setType("weekly")
    engineOilObj.runBackup

print  engineOilObj.folder
