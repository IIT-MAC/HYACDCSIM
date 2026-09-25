import os, sys
import pandas as pd
# PSSE
import psse34 
import psspy, redirect
redirect.psse2py()
# Hybrid AC/DC protection settings
from _PyModules import module_protection

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# User-defined input
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# file name and paths
str_savfile = r"IEEE_14_39.sav" # case study file - static data
str_dyrfile = r"IEEE_14_39.dyr" # case study file - dynamic data
str_pathinputfiles = r"C:\Users\lsigrist\OneDrive - Universidad Pontificia Comillas\PSSE\Tools\HYACDCSIM\Input\IEEE_14_39" # Path
str_lineprotection = r"Line_Relay_Data.xlsx" # Path to the input line protection devices data Excel file
str_loadprotection = r"Load_Relay_Data.xlsx" # Path to the input load protection devices data Excel file
str_machineprotection = r"Machine_Relay_Data.xlsx" # Path to the input machine protection devices data Excel file
str_miscellaneousprotection = r"Miscellaneous_Relay_Data.xlsx" # Path to the input miscellaneous protection devices data Excel file

# protection devices data paths
str_path4dynamics = str_pathinputfiles # 
str_pathlineprotection = os.path.join(str_pathinputfiles, str_lineprotection) # Path to the input line protection devices data Excel file
str_pathloadprotection = os.path.join(str_pathinputfiles, str_loadprotection) # Path to the input load protection devices data Excel file
str_pathmachineprotection = os.path.join(str_pathinputfiles, str_machineprotection) # Path to the input machine protection devices data Excel file
str_pathmiscellaneousprotection = os.path.join(str_pathinputfiles, str_miscellaneousprotection) # Path to the input miscellaneous protection devices data Excel file

# sys.path.append(str_pathinputfiles)
# sys.path.append(str_path4dynamics)

# initialize PSS/e
psspy.psseinit(200000) # set max bus number when starting PSS/e

str_pathsavfileorig = os.path.join(str_pathinputfiles,str_savfile)  # case study file - static data
str_pathdyrfileorig = os.path.join(str_pathinputfiles,str_dyrfile)  # case study file - dynamic data
str_pathsavfileprotection = str_pathsavfileorig[:-4] + r"_included_protection_devices.sav" 
str_pathrawfileprotection = str_pathsavfileprotection[:-4] + r".raw"
str_pathdyrfileprotection = str_pathdyrfileorig[:-4] + r"_included_protection_devices.dyr" 

# open PSS/e file
psspy.case(str_savfileorig)
SbaseMVA = psspy.sysmva()
psspy.dyre_new([1,1,1,1],str_dyrfileorig,"","","")

# Line_Relay_Model 
Line_Relay_Model_dict = module_protection.get_sheets_with_data(str_pathlineprotection)
module_protection.add_Line_Relay_Model(str_pathlineprotection, Line_Relay_Model_dict, SbaseMVA)

# Load_Relay_Model
suffixes_load_Relay = ["BL", "OW", "ZN", "AR", "AL"]
Load_Relay_Model_dict = module_protection.get_sheets_with_data(str_pathloadprotection)
module_protection.add_Load_Relay_Model(str_pathloadprotection, Load_Relay_Model_dict, suffixes_load_Relay)

# Machine_Relay_Model
Machine_Relay_Model_dict = module_protection.get_sheets_with_data(str_pathmachineprotection)
all_Machine_USRMDL_type = module_protection.add_Machine_Relay_Model(str_pathmachineprotection, Machine_Relay_Model_dict)

# Miscellaneous_Relay_Model
Miscellaneous_Relay_Model_dict = module_protection.get_sheets_with_data(str_pathmiscellaneousprotection)
module_protection.add_Miscellaneous_Relay_Model(str_pathmiscellaneousprotection, Miscellaneous_Relay_Model_dict)

psspy.save(str_pathsavfileprotection)                                       # save modified file .sav
psspy.rawd_2(0,1,[1,1,1,0,0,0,0],0,str_pathrawfileprotection)               # save modified file .raw
psspy.dyda(0,1,[2,1,0],0,str_pathdyrfileprotection)  

# For adding USRMDL models (If there are any, please pay attention to all_xxxxxxxxx_USRMDL_type)
with open(str_pathdyrfileprotection, "a") as file:
    file.write("\n".join(all_Machine_USRMDL_type) + "\n")


# Only for sorting dynamic file!!!
psspy.case(str_pathsavfileprotection)
psspy.dyre_new([1,1,1,1],str_pathdyrfileprotection,"","","")
psspy.dyda(0,1,[2,1,0],0,str_pathdyrfileprotection)
