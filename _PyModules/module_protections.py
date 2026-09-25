import os, sys
# PSSE
import psse34 
import psspy, redirect
redirect.psse2py()

import pandas as pd


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def fun_calculateOperationTime(df_Characteristic, row_values):

    char_value = int(row_values[4])
    
    matched_row = df_Characteristic[df_Characteristic.iloc[:, 0] == char_value]

    a1 = matched_row.iloc[0, 1] 
    a2 = matched_row.iloc[0, 2] 
    a3 = matched_row.iloc[0, 3]

    t_ops = []
    for ii in range(1, 5):

        t_op = (row_values[5] * a1) / ((row_values[2*ii+6]**a2) - a3)
        t_ops.append(t_op)
   
    return t_ops


def get_sheets_with_data(str_datafile):

    xls = pd.ExcelFile(str_datafile)
        
    Relay_Model_dict = []

    for sheet in xls.sheet_names:

        df = pd.read_excel(xls, sheet_name=sheet, header=0)
        if not df.empty:
            Relay_Model_dict.append(sheet)

    filtered_Relay_Model_dict = [Model_name for Model_name in Relay_Model_dict if 'CHR' not in Model_name]
    Relay_Model_dict = filtered_Relay_Model_dict

    return Relay_Model_dict


def add_Line_Relay_Model(str_lineprotectiondevicesdatafile, Line_Relay_Model_dict, SbaseMVA):

    xls = pd.ExcelFile(str_lineprotectiondevicesdatafile)

    for idmodel in Line_Relay_Model_dict:

        if idmodel == r"""CIROS1""":
            
            df_lineprotectiondata = pd.read_excel(str_lineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_lineprotectiondata.iterrows():
                from_bus = int(row.iloc[0])
                to_bus = int(row.iloc[1])
                ierr, cmpval = psspy.brndt2(from_bus,to_bus,'1','RX')  # Extracting the line impedance

                psspy.add_relay_model(from_bus,to_bus,idprotection,1,idmodel,12,[0,0,0,0,0,0,0,0,0,0,0,0],["","","","","","","","","","","",""],16,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
                psspy.add_relay_model(to_bus,from_bus,idprotection,1,idmodel,12,[0,0,0,0,0,0,0,0,0,0,0,0],["","","","","","","","","","","",""],16,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])

        elif idmodel == r"""DISTR1""":

            df_lineprotectiondata = pd.read_excel(str_lineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_lineprotectiondata.iterrows():
                from_bus = int(row.iloc[0])
                to_bus = int(row.iloc[1])
                psspy.add_relay_model(from_bus,to_bus,idprotection,1,idmodel,11,[0,0,0,0,0,0,0,0,0,0,0],["","","","","","","","","","",""],24,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
                psspy.add_relay_model(to_bus,from_bus,idprotection,1,idmodel,11,[0,0,0,0,0,0,0,0,0,0,0],["","","","","","","","","","",""],24,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])

        elif idmodel == r"""DPDTR1""":

            df_lineprotectiondata = pd.read_excel(str_lineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_lineprotectiondata.iterrows():
                from_bus = int(row.iloc[0])
                to_bus = int(row.iloc[1])
                psspy.add_relay_model(from_bus,to_bus,idprotection,1,idmodel,4,[0,0,0,0],["","","",""],5,[0.0,0.0,0.0,0.0,0.0])
                psspy.add_relay_model(to_bus,from_bus,idprotection,1,idmodel,4,[0,0,0,0],["","","",""],5,[0.0,0.0,0.0,0.0,0.0])

        elif idmodel == r"""RXR1""":

            df_lineprotectiondata = pd.read_excel(str_lineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_lineprotectiondata.iterrows():
                from_bus = int(row.iloc[0])
                to_bus = int(row.iloc[1])
                psspy.add_relay_model(from_bus,to_bus,idprotection,1,idmodel,10,[0,0,0,0,0,0,0,0,0,0],["","","","","","","","","",""],37,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
                psspy.add_relay_model(to_bus,from_bus,idprotection,1,idmodel,10,[0,0,0,0,0,0,0,0,0,0],["","","","","","","","","",""],37,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])

        elif idmodel == r"""SCGAP2""":

            df_lineprotectiondata = pd.read_excel(str_lineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_lineprotectiondata.iterrows():
                from_bus = int(row.iloc[0])
                to_bus = int(row.iloc[1])
                psspy.add_relay_model(from_bus,to_bus,idprotection,1,idmodel,14,[0,0,0,0,0,0,0,0,0,0,0,0,0,0],["","","","","","","","","","","","","",""],6,[0.0,0.0,0.0,0.0,0.0,0.0])
                psspy.add_relay_model(to_bus,from_bus,idprotection,1,idmodel,14,[0,0,0,0,0,0,0,0,0,0,0,0,0,0],["","","","","","","","","","","","","",""],6,[0.0,0.0,0.0,0.0,0.0,0.0])

        elif idmodel == r"""SLLP1""":

            df_lineprotectiondata = pd.read_excel(str_lineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_lineprotectiondata.iterrows():
                from_bus = int(row.iloc[0])
                to_bus = int(row.iloc[1])
                psspy.add_relay_model(from_bus,to_bus,idprotection,1,idmodel,10,[0,0,0,0,0,0,0,0,0,0],["","","","","","","","","",""],14,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
                psspy.add_relay_model(to_bus,from_bus,idprotection,1,idmodel,10,[0,0,0,0,0,0,0,0,0,0],["","","","","","","","","",""],14,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])

        elif idmodel == r"""SLNOS1""":
            
            df_lineprotectiondata = pd.read_excel(str_lineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_lineprotectiondata.iterrows():
                from_bus = int(row.iloc[0])
                to_bus = int(row.iloc[1])
                psspy.add_relay_model(from_bus,to_bus,idprotection,1,idmodel,12,[0,0,0,0,0,0,0,0,0,0,0,0],["","","","","","","","","","","",""],16,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
                psspy.add_relay_model(to_bus,from_bus,idprotection,1,idmodel,12,[0,0,0,0,0,0,0,0,0,0,0,0],["","","","","","","","","","","",""],16,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])

        elif idmodel == r"""SLYPN1""":

            df_lineprotectiondata = pd.read_excel(str_lineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_lineprotectiondata.iterrows():
                from_bus = int(row.iloc[0])
                to_bus = int(row.iloc[1])
                psspy.add_relay_model(from_bus,to_bus,idprotection,1,idmodel,4,[0,0,0,0],["","","",""],33,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
                psspy.add_relay_model(to_bus,from_bus,idprotection,1,idmodel,4,[0,0,0,0],["","","",""],33,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])

        elif idmodel == r"""TIOCR1""":
            
            df_lineprotectiondata = pd.read_excel(str_lineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            df_Characteristic = pd.read_excel(str_lineprotectiondevicesdatafile, sheet_name="TIOCR1-CHR", header=0)
            for index, row in df_lineprotectiondata.iterrows():
                from_bus = int(row.iloc[0])
                to_bus = int(row.iloc[1])
                ierr, rval = psspy.brndat(from_bus,to_bus,'1','RATEA')  # Extracting the line rating
                row_values = row.tolist()
                
                if row.iloc[4] == 6:

                    t_ops = [row.iloc[9], row.iloc[11], row.iloc[13], row.iloc[15]]

                else:

                    t_ops = fun_calculateOperationTime(df_Characteristic, row_values)
                
                psspy.add_relay_model(from_bus,to_bus,r"""{}""".format(int(row.iloc[2])),int(row.iloc[3]),idmodel,12,[1,0,0,from_bus,to_bus,row.iloc[2],0,0,0,0,0,0],["","","","","","","","","","","",""],14,[(rval/SbaseMVA)*row.iloc[6],row.iloc[7],row.iloc[8],t_ops[0],row.iloc[10],t_ops[1],row.iloc[12],t_ops[2],row.iloc[14],t_ops[3],row.iloc[16],row.iloc[17],row.iloc[18],row.iloc[19]])
                psspy.add_relay_model(to_bus,from_bus,r"""{}""".format(int(row.iloc[2])),int(row.iloc[3]),idmodel,12,[1,0,0,to_bus,from_bus,row.iloc[2],0,0,0,0,0,0],["","","","","","","","","","","",""],14,[(rval/SbaseMVA)*row.iloc[6],row.iloc[7],row.iloc[8],t_ops[0],row.iloc[10],t_ops[1],row.iloc[12],t_ops[2],row.iloc[14],t_ops[3],row.iloc[16],row.iloc[17],row.iloc[18],row.iloc[19]])

        else:
            
            print('No Line Relay Model has been inputted')


def add_Load_Relay_Model(str_loadprotectiondevicesdatafile, Load_Relay_Model_dict, suffixes_load_Relay):

    xls = pd.ExcelFile(str_loadprotectiondevicesdatafile)

    for idmodel in Load_Relay_Model_dict:
        
        if idmodel == r"""DLSHxx""":
            
            df_loadprotectiondata = pd.read_excel(str_loadprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_loadprotectiondata.iterrows():
                bus_No = int(row.iloc[0])

                if row.iloc[2] in suffixes_load_Relay:
                    suffixes_index = suffixes_load_Relay.index(row.iloc[2])
                else:
                        print "Error: '{}' not found in the load relay suffix list!".format(row.iloc[2])

                idmodel = idmodel.replace("xx", row.iloc[2])   
                psspy.add_load_model(bus_No,r"""{}""".format(int(row.iloc[1])),suffixes_index,2,idmodel,0,[],[],13, row.iloc[3:16].tolist())

        elif idmodel == r"""LDS3xx""":

            df_loadprotectiondata = pd.read_excel(str_loadprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_loadprotectiondata.iterrows():
                bus_No = int(row.iloc[0])

                if row.iloc[2] in suffixes_load_Relay:
                    suffixes_index = suffixes_load_Relay.index(row.iloc[2])
                else:
                        print "Error: '{}' not found in the load relay suffix list!".format(row.iloc[2])

                idmodel = idmodel.replace("xx", row.iloc[2])
                psspy.add_load_model(bus_No,r"""{}""".format(int(row.iloc[1])),suffixes_index,2,idmodel,3,[0,0,0],["","",""],21, row.iloc[3:24].tolist())

        elif idmodel == r"""LDSHxx""":

            df_loadprotectiondata = pd.read_excel(str_loadprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_loadprotectiondata.iterrows():
                bus_No = int(row.iloc[0])

                if row.iloc[2] in suffixes_load_Relay:
                    suffixes_index = suffixes_load_Relay.index(row.iloc[2])
                else:
                        print "Error: '{}' not found in the load relay suffix list!".format(row.iloc[2])

                idmodel = idmodel.replace("xx", row.iloc[2])
                psspy.add_load_model(bus_No,r"""{}""".format(int(row.iloc[1])),suffixes_index,2,idmodel,0,[],[],10, row.iloc[3:13].tolist())

        elif idmodel == r"""LDSTxx""":

            df_loadprotectiondata = pd.read_excel(str_loadprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_loadprotectiondata.iterrows():
                bus_No = int(row.iloc[0])

                if row.iloc[2] in suffixes_load_Relay:
                    suffixes_index = suffixes_load_Relay.index(row.iloc[2])
                else:
                        print "Error: '{}' not found in the load relay suffix list!".format(row.iloc[2])

                idmodel = idmodel.replace("xx", row.iloc[2])
                psspy.add_load_model(bus_No,r"""{}""".format(int(row.iloc[1])),suffixes_index,2,idmodel,0,[],[],12, row.iloc[3:15].tolist())

        elif idmodel == r"""LVS3xx""":

            df_loadprotectiondata = pd.read_excel(str_loadprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_loadprotectiondata.iterrows():
                bus_No = int(row.iloc[0])

                if row.iloc[2] in suffixes_load_Relay:
                    suffixes_index = suffixes_load_Relay.index(row.iloc[2])
                else:
                        print "Error: '{}' not found in the load relay suffix list!".format(row.iloc[2])

                idmodel = idmodel.replace("xx", row.iloc[2])
                psspy.add_load_model(bus_No,r"""{}""".format(int(row.iloc[1])),suffixes_index,2,idmodel,7,[0,0,0,0,0,0,0],["","","","","","",""],22, row.iloc[3:25].tolist())
                
        elif idmodel == r"""LVSHxx""":

            df_loadprotectiondata = pd.read_excel(str_loadprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_loadprotectiondata.iterrows():
                bus_No = int(row.iloc[0])

                if row.iloc[2] in suffixes_load_Relay:
                    suffixes_index = suffixes_load_Relay.index(row.iloc[2])
                else:
                        print "Error: '{}' not found in the load relay suffix list!".format(row.iloc[2])

                idmodel = idmodel.replace("xx", row.iloc[2])
                psspy.add_load_model(bus_No,r"""{}""".format(int(row.iloc[1])),suffixes_index,2,idmodel,1,[0],[""],10, row.iloc[3:13].tolist())

        elif idmodel == r"""UVUFxxU1""":

            df_loadprotectiondata = pd.read_excel(str_loadprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_loadprotectiondata.iterrows():
                bus_No = int(row.iloc[0])

                if row.iloc[2] in suffixes_load_Relay:
                    suffixes_index = suffixes_load_Relay.index(row.iloc[2])
                else:
                        print "Error: '{}' not found in the load relay suffix list!".format(row.iloc[2])

                idmodel = idmodel.replace("xx", row.iloc[2])
                psspy.add_load_model(bus_No,r"""{}""".format(int(row.iloc[1])),suffixes_index,2,idmodel,1,[0],[""],10, row.iloc[3:23].tolist())
        
        else:
            
            print('No Load Relay Model has been inputted')


def add_Machine_Relay_Model(str_machineprotectiondevicesdatafile, Machine_Relay_Model_dict):

    xls = pd.ExcelFile(str_machineprotectiondevicesdatafile)

    all_Machine_USRMDL_type = []
    
    for idmodel in Machine_Relay_Model_dict:
        
        if idmodel == r"""LOEXR1T""":
            
            df_machineprotectiondata = pd.read_excel(str_machineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_machineprotectiondata.iterrows():
                bus_No = int(row.iloc[0])

                psspy.add_cctmcnp_model(bus_No,idprotection,idmodel,0,[],[],14,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])

        elif idmodel == r"""MCREPWU1""":
            
            df_machineprotectiondata = pd.read_excel(str_machineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_machineprotectiondata.iterrows():
                bus_No = int(row.iloc[0])

                new_MCREPWU1_Relay = "{} 'USRMDL' {} '{}' 405 2 4 8 1 4 ".format(bus_No, idprotection, idmodel) + " ".join(map(str, row.iloc[2:6].tolist())) + ", " + " ".join(map(str, row.iloc[6:17].tolist())) + " /"
                all_Machine_USRMDL_type.append(new_MCREPWU1_Relay)
                       
        elif idmodel == r"""NRCGP3U""":

            df_machineprotectiondata = pd.read_excel(str_machineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_machineprotectiondata.iterrows():
                bus_No = int(row.iloc[0])

                new_NRCGP3U_Relay = "{} 'USRMDL' {} '{}' 405 2 10 26 0 3 ".format(bus_No, idprotection, idmodel) + " ".join(map(str, row.iloc[2:12].tolist())) + ", " + " ".join(map(str, row.iloc[12:37].tolist())) + " /"
                all_Machine_USRMDL_type.append(new_NRCGP3U_Relay)
                
        elif idmodel == r"""VPERHZU1""":

            df_machineprotectiondata = pd.read_excel(str_machineprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_machineprotectiondata.iterrows():
                bus_No = int(row.iloc[0])

                new_VPERHZU1_Relay = "{} 'USRMDL' {} '{}' 405 2 18 13 2 6 ".format(bus_No, idprotection, idmodel) + " ".join(map(str, row.iloc[2:5].tolist())) + ", " + " ".join(map(str, row.iloc[5:17].tolist())) + " /"
                all_Machine_USRMDL_type.append(new_VPERHZU1_Relay)
   
        else:
            
            print('No Machine Relay Model has been inputted')

    return all_Machine_USRMDL_type


def add_Miscellaneous_Relay_Model(str_miscellaneousprotectiondevicesdatafile, Miscellaneous_Relay_Model_dict):

    xls = pd.ExcelFile(str_miscellaneousprotectiondevicesdatafile)
    
    for idmodel in Miscellaneous_Relay_Model_dict:

        if idmodel == r"""FRQxxxx""":

            df_miscellaneousprotectiondata = pd.read_excel(str_miscellaneousprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_miscellaneousprotectiondata.iterrows():

                idmodel = idmodel.replace("xxxx", row.iloc[0])
                psspy.add_cctmsco_model(idmodel,index+1,3,[int(row.iloc[5]),int(row.iloc[6]),row.iloc[7]],["","",""],4,[float(val) for val in row.iloc[1:5].tolist()])

            index_Miscellaneous_Relay_Model = index + 1 # Since we need sequential numbering for this type of relay, it starts from 1 and continues numbering up to the last relay of this type (FRQxxxx and VTGxxxx).
    
        elif idmodel == r"""VTGxxxx""":

            df_miscellaneousprotectiondata = pd.read_excel(str_miscellaneousprotectiondevicesdatafile, sheet_name=idmodel, header=0)
            for index, row in df_miscellaneousprotectiondata.iterrows():
                
                idmodel = idmodel.replace("xxxx", row.iloc[0])
                psspy.add_cctmsco_model(idmodel,index_Miscellaneous_Relay_Model + index+1,3,[int(row.iloc[5]),int(row.iloc[6]),row.iloc[7]],["","",""],4,[float(val) for val in row.iloc[1:5].tolist()])
            
        else:
            
            print('No Miscellaneous Relay Model has been inputted')
