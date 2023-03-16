import my_setup as mySetup
import my_excel_handler as myExcelHandler


def save_coordinates_and_msa600_elevation_semi_auto(dieIndex, myVerifiedWaferMap: myExcelHandler.VerifiedWaferMap):
    textInput = input("Enter 't' if Coordinates and Focus are OK or 'i' to ignore the die: ")

    if(textInput == 't'):
        print('saving coordinates & focus elevation')
        chuckCoordinates = mySetup.myPav.get_chuck_coordinates()
        probeCoordinates = mySetup.myPav.get_probe_coordinates_relative_to_home()  #MSA Attached to "Probe station"
        x = float(chuckCoordinates[0])
        y = float(chuckCoordinates[1])
        msa600_elevation = float(probeCoordinates[3])           #MSA Attached to "Probe station"
        #save coordinates
        print('index: ' +str(dieIndex))
        myVerifiedWaferMap.save_die_coordinates(index= dieIndex, coordinates=[x,y])
        myVerifiedWaferMap.save_msa600_elevation(index= dieIndex, elevation = msa600_elevation)
    elif(textInput == 'i'):
        print('ignored die')
        #save coordinates
        print('index: ' +str(dieIndex))
        myVerifiedWaferMap.save_die_coordinates(index= dieIndex, coordinates=["IGNORED","IGNORED"])

def save_chuck_position_and_msa600_elevation_manual(myVerifiedWaferMap: myExcelHandler.VerifiedWaferMap):
    textInput = input("Enter 't' if Coordinates and Focus are OK or 'f' to finish: ")

    if(textInput == 't'):
        dieIndex = input("Enter the name (index) for the die you are taking the coordinates of and press enter: ")
        print('saving coordinates & focus elevation')
        chuckCoordinates = mySetup.myPav.get_chuck_coordinates()
        probeCoordinates = mySetup.myPav.get_probe_coordinates_relative_to_home()
        thetaPosition= mySetup.myPav.get_theta_position()
        
        x = float(chuckCoordinates[0])
        y = float(chuckCoordinates[1])
        msa600_elevation = float(probeCoordinates[3])        
        print('index: ' +str(dieIndex))
        myVerifiedWaferMap.save_die_coordinates(index= dieIndex, coordinates=[x,y])
        myVerifiedWaferMap.save_msa600_elevation(index= dieIndex, elevation = msa600_elevation)
        myVerifiedWaferMap.save_theta_position(index = dieIndex, thetaPosition = thetaPosition)
        
        return False
    elif(textInput == 'f'):
        return True

def anotate_die_ignored(dieIndex, myVerifiedWaferMap: myExcelHandler.VerifiedWaferMap):
    myVerifiedWaferMap.save_die_ignored(index= dieIndex)

def get_and_save_coordinates_of_center_of_chuck(myVerifiedWaferMap: myExcelHandler.VerifiedWaferMap):
    chuckCoordinates = mySetup.myPav.get_chuck_coordinates()
    myVerifiedWaferMap.save_center_coordinates(coordinates=chuckCoordinates)
    x = float(chuckCoordinates[0])
    y = float(chuckCoordinates[1])
    return [x,y]

