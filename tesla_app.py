import requests
import sys


BaseURL = "https://owner-api.teslamotors.com/"

def test(): #try getting a response from the API

    bearerKey = "dd5a5ffe7915426d5730c6f6223cc827939759a9bb5e0e14a82cb36e7d60b411" #input('Please input the bearer key.')

    headers = {
        "Authorization": f"Bearer {bearerKey}"
    }
    
    
    
    getVehicle = "api/1/vehicles"
    r = requests.get(BaseURL + getVehicle, headers=headers)
    print(r.json())

    id = r.json()["response"][0]["id"]
    print(id)


def main():
    #Start Request. Make sure it goes through correctly. Error handling.
    key = "dd5a5ffe7915426d5730c6f6223cc827939759a9bb5e0e14a82cb36e7d60b411" #input('Please input the bearer key.')

    headers = {"Authorization": f"Bearer {key}"}

    
    getVehicle = "api/1/vehicles"
    

    #get the correct vehicle. Error handling.
    try:
        r = requests.get(BaseURL + getVehicle, headers=headers)
        
    except Exception as ex:
        print(ex)

    id = r.json()["response"][0]["id"]

    wake(id, headers)

    #choose between state and command. If command, choose which option. Put in a loop. Provide exit option also.
    root_choices = [display_state, commands, exit, "View Car State", "Execute a command", "exit"]

    choices = ["[1] View Car State",
                "[2] Commands",
                "[3] Exit"]
    choice = choose(choices)
    try:
        root_choices[int(choice)-1](id, headers)
    except TypeError: # This is to nullify the passing of too many parameters into exit()
        exit()


# Lists off choices and returns the user's choice. Make sure it is a number. Confirm choice. Error handling.
def choose(choices, *addReturn):
    print()
    while True:
        #print off options and get input
        if addReturn:
            print(f"Please choose (1-{len(choices) + 1}):")
            choices.append(f'[{len(choices) + 1}] Return to home menu') # add return option
        else:
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
def wake(id, headers):
    print('Welcome to the Tesla Computer App.')
    print('Please wait a moment while your Tesla wakes up.')
    try:
        r = requests.post(f'{BaseURL}/api/1/vehicles/{id}/wake_up', headers=headers)
    except Exception as ex:
        print(f'status code {r.status_code}')
        print(f'Exception in wake(): {ex}')



    i = 0

    while i == 0:
        if r.json()["response"]["state"] == "online":
            i += 1
            return


# Choose a command. Return URL for it. 
def commands(id, headers):
    commandURLs = [
        #0 "honk" : 
        f'/api/1/vehicles/{id}/command/honk_horn',
        #1 "lights" : 
        f'/api/1/vehicles/{id}/command/flash_lights',
        #2 "toggleValetMode" : 
        f'/api/1/vehicles/{id}/command/set_valet_mode',
        #3 "unlockDoor" : 
        f'/api/1/vehicles/{id}/command/door_unlock',
        #4 "lockDoor" : 
        f'/api/1/vehicles/{id}/command/door_lock',
        #5 "trunk" : 
        f'/api/1/vehicles/{id}/command/actuate_trunk', # Note: Look at documentation to understand parameters.
        #6 "ventWindows" : 
        f'/api/1/vehicles/{id}/command/window_control', #parameters required
        #7 "openChargePort" : 
        f'/api/1/vehicles/{id}/command/charge_port_door_open',
        #8 "setChargeLimit" : 
        f'/api/1/vehicles/{id}/command/set_charge_limit', #parameters required
        #9 "setTemp" : 
        f'/api/1/vehicles/{id}/command/set_temps', #parameters required *Note: include conversion from fahr to cels for this.
        #10 "toggleMedia" : 
        f'/api/1/vehicles/{id}/command/media_toggle_playback',
        #11 "nextTrack" : 
        f'/api/1/vehicles/{id}/command/media_next_track',
        #12 "previousTrack" : 
        f'/api/1/vehicles/{id}/command/media_prev_track',
        #13 "volUp" : 
        f'/api/1/vehicles/{id}/command/media_volume_up',
        #14 "volDown" : 
        f'/api/1/vehicles/{id}/command/media_volume_down'
    ]

    commands = [
        "[1] Honk horn",
        "[2] Flash lights",
        "[3] Turn on/off valet mode",
        "[4] Lock/unlock door",
        "[5] Open trunk/frunk",
        "[6] Vent windows",
        "[7] Open charge port",
        "[8] Set charge limit",
        "[9] Set temperature",
        "[10] See Media commands"
    ]

    media = [
        "[1] Turn media on/off",
        "[2] Skip track",
        "[3] Previous track",
        "[4] Volume up",
        "[5] Volume down"
    ]
    
    command = choose(commands, True)

    #Pull up media controls if media is selected
    if command == "10":
        command = choose(media, True) + 9

    #Choose the correct url from the list, depending on what the user selected.
    url = commandURLs[int(command)-1]
    
    #set parameters for the options that require parameters

    if command == 5:
        choices = [
        "[1] Open trunk",
        "[2] Open frunk"
        ]
        choice = choose(choices, True)
        if choice == 1:
            params = {"which_trunk":"trunk"}
        elif choice == 2:
            params = {"which_trunk":"frunk"}

    elif command == 6:
        params = {"command":"vent"}

    elif command == 8:
        choice = input("Please set the charge limit (50-100)%")
        params = {"percent":choice}
    elif command == 9:
        choice = fahr_to_cels(input("What would you like to set the temperature to?"))
        params = {"driver_temp":choice,"passenger_temp":choice}

    #If params are required, use them, if not, don't.
    try:
        executeCommand(url, headers, params)
    except UnboundLocalError:
        executeCommand(url, headers, command)


    

# function for executing commands.
def executeCommand(url, headers, *params, command):

    try:
        r = requests.post(f'{BaseURL}{url}', headers=headers, params=params)
        
        if r.status_code == 200:
            print("Success")

    except Exception as ex:
        print(f'Error: {ex}')
        print("Command Unsuccesful")
        main()

    print_command_status(command)


#This function will take the executed command and relay back pertinent info to the user.
def print_command_status(command):
    statusDict = {
        
    }


# display car state information
def display_state(id, headers):

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




#Prints a dictionary in a user friendly way, leaving some space before and after
def cleanPrint(header, dict):
    print()
    print(header)
    for key, value in dict.items():
        
        print("{}: {}".format(key, value))
    print()

#converts celsius to fahrenheit, adds degrees sign
def cels_to_fahr(cels):
    fahr = round((float(cels) * 1.8 + 32), 1)
    fahr = str(fahr) + "°F"
    return fahr

#take user input of fahr, remove any non-numbers, output cels
def fahr_to_cels(fahr):
    for char in range(len(fahr)):
        if not fahr[char].isdigit():
            fahr.replace(fahr[char], "")

    cels = round((float(fahr) -32) * (5/9))
    return cels

main()
