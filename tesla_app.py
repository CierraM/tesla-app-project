import requests
import sys
import json
import time



BaseURL = "https://owner-api.teslamotors.com/"

def main():
    # read bearer key from a separate file.
    f = open("bearerKey.txt", "r")
    key = (f.read())

    #set up headers
    global headers
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    
    getVehicle = "api/1/vehicles"
    

    #get the correct vehicle. Error handling.
    try:
        r = requests.get(BaseURL + getVehicle, headers=headers)
        
    except Exception as ex:
        print(ex)

    global id
    id = r.json()["response"][0]["id"]

    wake()

    #choose between state and command. If command, choose which option. Put in a loop. Provide exit option also.
    root_choices = [display_state, commands, exit, "View Car State", "Execute a command", "exit"]

    choices = ["[1] View Car State",
                "[2] Commands",
                "[3] Exit"]
    choice = choose(choices)
    try:
        root_choices[int(choice)-1]()
    except TypeError: # This is to nullify the passing of too many parameters into exit()
        exit()


# Lists off choices and returns the user's choice. Make sure it is a number. Confirm choice. Error handling.
def choose(choices, *addReturn):
    print()
    if addReturn:
        print(f"Please choose (1-{len(choices) + 1}):")
        choices.append(f'[{len(choices) + 1}] Return to home menu') # add return option
    while True:
        #print off options and get input
        print()
        print(f"Please choose (1-{len(choices)}):")
        i = 0
        while (i < len(choices)):
            print(choices[i])
            i += 1
            
        choice = input()
        
        #check for invalid input (ex. not a number, not in the correct range)
        if ((choice.isnumeric())):
            if ((int(choice)) > 0 and (int(choice)) <= len(choices)):

                #confirm with user that they have selected the right thing.
                confirmation = input(f'You would like to {choices[int(choice)-1]}. Is that correct? (y/n)')
                if confirmation.lower() == "y":
                    if "Return to home menu" in choices[int(choice) - 1]:
                        
                        main()
                    return choice
                else:
                    print("Please try again.")
                    continue
            else:
                print(f'{choice} is not an option.')
                continue

    
#wake the car up. Use a loop so further commands cannot be executed until car is awake.
def wake():
    print('Welcome to the Tesla Computer App.')
    print('Please wait a moment while your Tesla wakes up.')
    try:
        r = requests.post(f'{BaseURL}/api/1/vehicles/{id}/wake_up', headers=headers)
    except Exception as ex:
        print(f'Exception in wake(): {ex}')



    i = 0

    while i == 0:
        if r.json()["response"]["state"] == "online":
            i += 1
            return


# Choose a command. Return URL for it. 
def commands():
    commandURLs = [
        #0 "honk" : 
        f'/api/1/vehicles/{id}/command/honk_horn',
        #1 "lights" : 
        f'/api/1/vehicles/{id}/command/flash_lights',
        #2 "unlockDoor" : 
        f'/api/1/vehicles/{id}/command/door_unlock',
        #3 "lockDoor" : 
        f'/api/1/vehicles/{id}/command/door_lock',
        #4 "trunk" : 
        f'/api/1/vehicles/{id}/command/actuate_trunk', # Can't get this to work, so it is not in use right now
        #5 "ventWindows" : 
        f'/api/1/vehicles/{id}/command/window_control', #parameters required
        #6 "openChargePort" : 
        f'/api/1/vehicles/{id}/command/charge_port_door_open',
        #7 "setChargeLimit" : 
        f'/api/1/vehicles/{id}/command/set_charge_limit', #parameters required
        #8 "setTemp" : 
        f'/api/1/vehicles/{id}/command/set_temps', #parameters required *Note: include conversion from fahr to cels for this.
        #9 turn on climate control
        f'/api/1/vehicles/{id}/command/auto_conditioning_start',
        #10 turn off climate control
        f'/api/1/vehicles/{id}/command/auto_conditioning_stop',
        #11 close charge port door
        f'/api/1/vehicles/{id}/command/charge_port_door_close'
    ]

    commands = [
        "[1] Honk horn", 
        "[2] Flash lights",
        "[3] Lock/unlock door", 
        "[4] Vent windows",
        "[5] Open/close charge port",
        "[6] Set charge limit",
        "[7] Set temperature",
        "[8] Turn on/off climate control" 
        
    ]


    

    command = choose(commands, True)
    
    command = int(command)
    # Shift numbers around so that command will line up with url index
    if command == 1:
        urlCommand = 0

    elif command == 2:
        urlCommand = 1

    elif command == 3: #Is it locked?
        if check_state(command) == True:
            urlCommand = 2 #unlock door
        else:
            urlCommand = 3 #lock door

    elif command == 4:
        urlCommand = 5

    elif command == 5:
        if check_state(command) == True:
            urlCommand = 11 #close door
        else:
            urlCommand = 6 #open door

    elif command == 6:
        urlCommand = 7
    
    elif command == 7:
        urlCommand = 8

    elif command == 8:
        urlCommand = 8

    elif command == 8: #Is climate on?
        if check_state(command) == True:
            urlCommand = 10 # turn off climate
        else: 
            urlCommand = 9 # turn on climate

    else:
        print("There was some problem and the command could not be found.")
        main()


    #Choose the correct url from the list, depending on what the user selected.
    url = commandURLs[int(urlCommand)]

    
    #set parameters for the options that require parameters

    if command == 4:
        params = {"lat": "0", "lon": "0", "command": "vent"}

    elif command == 6:
        while True:
            choice = int(input("Please set the charge limit (50-100)%"))
            if choice > 50 and choice <= 100:
                params = {"percent":choice}
                break
            else:
                print("Please choose a number between 50 and 100")

    elif command == 7:
        choice = fahr_to_cels(input("What would you like to set the temperature to?"))
        
        params = {"driver_temp":choice,"passenger_temp":choice}

    #If params are required, use them, if not, don't.
    try:
        
        
        executeCommand(url, command, params)
        
    except UnboundLocalError:
        executeCommand(url, command)
    
    
    print()
    returnToMain()
    

# function for executing commands.
def executeCommand(url, command, *params):

    try:                #Just making sure if no parameters are passed in, the function still works.
        parameters = json.dumps(params[0])
    except:
        parameters = ""
    try:
        r = requests.post(f'{BaseURL}{url}', headers=headers, data=parameters)
        
        if r.status_code == 200:
            jsonData = r.json()
            response = (jsonData["response"]["result"])
            if response:
                print("Success")
                print_command_status(command)
            else:
                print("Command Unsuccesful")

    except Exception as ex:
        print(f'Error: {ex}')
        returnToMain()
    
#This function is to check where something is at before deciding which command to use.
def check_state(command):
    url= f'{BaseURL}/api/1/vehicles/{id}/vehicle_data'

    if command == 3: #check is door locked
        url= f'{BaseURL}/api/1/vehicles/{id}/vehicle_data'
        try: 
            r = requests.get(url, headers=headers)
            data = r.json()
            if data["response"]["vehicle_state"]["locked"]:
                return True
            else:
                return False
        except Exception as ex:
            print(ex)
            
    elif command == 5:
        url= f'{BaseURL}/api/1/vehicles/{id}/vehicle_data'
        try: 
            r = requests.get(url, headers=headers)
            data = r.json()
            if data["response"]["charge_state"]["charge_port_door_open"]:
                return True
            else:
                return False
        except Exception as ex:
            print(ex)
            

    elif command == 8: # check is climate control on
        
        url= f'{BaseURL}/api/1/vehicles/{id}/data_request/climate_state'
        try: 
            r = requests.get(url, headers=headers)
            data = r.json()
            if data["response"]["is_climate_on"]:
                return True
            else:
                return False
        except Exception as ex:
            print(ex)
        
    else:
        print("check_state received the wrong number")
        return


#This function will take the executed command and relay back pertinent info to the user.
#command is a number 1-8 correlating to one of the commands. 
def print_command_status(command):
    url= f'{BaseURL}/api/1/vehicles/{id}/vehicle_data'
    for second in range(2): # This is to give the program some time to update before printing message
        command = int(command)
        time.sleep(1)   
        try: 
            r = requests.get(url, headers=headers)
            data = r.json()
        except Exception as ex:
            print(ex)    
        second += 1

    if command == 1: #honk
        message = "The horn has been honked."

    elif command == 2: #lights
        message = "The lights have been flashed"

    elif command == 3:
        
        if check_state(3):
            message = "The car is locked."
        else:
            message = "The car is unlocked."

    elif command == 4:#vent windows
        if data["response"]["vehicle_state"]["fd_window"] == 0:
            message = "The windows are closed."
        else:
            message = "The windows are vented or open."

    elif command == 5:#open charge port
        if data["response"]["charge_state"]["charge_port_door_open"]:
            message = "The charge port door is open."
        else:
            message = "The charge port door is closed."
    elif command == 6:#set charge limit
        message = f'The charge limit is set to {data["response"]["charge_state"]["charge_limit_soc"]}%.'

    elif command == 7:#set temp  
        message = f'The climate control is set to {cels_to_fahr(data["response"]["climate_state"]["driver_temp_setting"])}.\nThe current temperature inside the car is {cels_to_fahr(data["response"]["climate_state"]["inside_temp"])}.'

    elif command == 8:#turn on climate control
        if data["response"]["climate_state"]["is_climate_on"]:
            message = "Climate control is on."
        else:
            message = "Climate control is off"
    else:
        message = "Unable to display confirmation message."
        
    print(message)





# display car state information
def display_state():

    # Code to make it do things:
    # Put the url extensions in a list with all the things I want it to do.
    # display name, location, current speed, temperature, battery level, charge state,

    url= f'{BaseURL}/api/1/vehicles/{id}/vehicle_data'
    try: 
        r = requests.get(url, headers=headers)
        
    except Exception as ex:
        print(ex)

    data = {
        "Display Name": r.json()["response"]["display_name"],
        "Current Location": f'{r.json()["response"]["drive_state"]["latitude"]}, {r.json()["response"]["drive_state"]["longitude"]}', 
        "Speed": r.json()["response"]["drive_state"]["speed"], 
        "Current Temperature": cels_to_fahr(r.json()["response"]["climate_state"]["inside_temp"]), 
        "Battery Level": f'{r.json()["response"]["charge_state"]["battery_level"]}%', 
        "Charge State": r.json()["response"]["charge_state"]["charging_state"]
    }
    cleanPrint("Car State:", data)
    leave = input("Return to main menu? (y/n)")
    if leave.lower() == "n":
        exit()
    else:
        main()


def returnToMain():
    leave = input("Return to commands? (y/n)")
    if leave.lower() == "n":
        exit()
    else:
        commands()
    
#Prints a dictionary in a user friendly way, leaving some space before and after
def cleanPrint(header, dict):
    print()
    print(header)
    for key, value in dict.items():    
        print("{}: {}".format(key, value))
    print()

#converts celsius to fahrenheit, adds degrees sign
def cels_to_fahr(cels):
    fahr = round((float(cels) * (9/5) + 32), 1)
    fahr = str(fahr) + "°F"
    return fahr

#take user input of fahr, remove any non-numbers, output cels
def fahr_to_cels(fahr):
    for char in range(len(fahr)):
        if not fahr[char].isdigit():
            fahr.replace(fahr[char], "")

    cels = (float(fahr) -32) * (5/9)
    return cels

main()
