import keyboard as keyboard
import my_setup as mySetup
import my_excel_handler as myExcelHandler

def save_coordinates_of_die_home_point_and_msa600_elevation(dieIndex, myVerifiedWaferMap: myExcelHandler.VerifiedWaferMap):
    print("Press T if Coordinates and Focus are OK or F to finish saving coordinates")

    while True:
        try:
            if keyboard.is_pressed('t'):
                print('saving coordinates & focus elevation')
                chuckCoordinates = mySetup.myPav.get_chuck_coordinates()
                probeCoordinates = mySetup.myPav.get_probe_coordinates()  #MSA Attached to "Probe station"
                x = float(chuckCoordinates[0])
                y = float(chuckCoordinates[1])
                msa600_elevation = float(probeCoordinates[3])           #MSA Attached to "Probe station"
                #save coordinates
                print('index: ' +str(dieIndex))
                myVerifiedWaferMap.save_die_coordinates(index= dieIndex, coordinates=[x,y])
                myVerifiedWaferMap.save_msa600_elevation(index= dieIndex, elevation = msa600_elevation)
                
                break
            elif keyboard.is_pressed('i'):
                print('ignored die')
                #save coordinates
                print('index: ' +str(dieIndex))
                myVerifiedWaferMap.save_die_coordinates(index= dieIndex, coordinates=["IGNORED","IGNORED"])
                break
        except:
            break