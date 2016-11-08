#Sanjith Venkatesh 20038520
#Project 3
#User Interface Module:
#A module that reads the input and constructs the objects that will generate the program's output.
#This is the only module that should have an if __name__ == '__main__' block to make it executable; this module is executed to run this program.

from connection import Connection
from outputs import OutputGenerator

class UserInterface:
    
    # Assumption: user knows how to properly input information. Number of locations must be at least 2.
    # Takes in inputs for both locations and outputs depending on parameter
    # and returns lists of locations or outputs   
    def collect_inputs(self, inorout: str):

        while True:
            num_of_inputs = int(input(""))
            if num_of_inputs >0 and type(num_of_inputs) == int:
                if inorout == "location":
                    if num_of_inputs >= 2:
                        break
                else:
                    if num_of_inputs <= 5:
                        break
            else:
                print("Invalid number or type")
        input_list = []
        for num in range(num_of_inputs):
            add = str(input())
            input_list.append(add)
        return input_list
            
        
    # Makes use of the Connection module to retrieve data from mapquest.
    # The data should be in JSON format
    def send_and_receive_data(self, locs: [list]):
        #Sends and receives json data from MapQuest server
        c = Connection()
        url = c.build_url_for_request(locs,outputs)
        json_list = c.get_info(url)
        return json_list

    # Prints the output in the correct format from the supplied JSON data
    # by invoking the appropriate output generators
    def printOutputs(self, json_list, outputs):
        o = OutputGenerator()
        outputGens = o.getOutputGens(outputs) #returns a list of generator classes for getting info
        for gen in outputGens:
            print()
            outputlists = gen.printdata(json_list) #returns list of data ready to be printed out
            for output in outputlists:
                print(output)

# Main driver script
if __name__ == '__main__':
    x = UserInterface()
    locs = x.collect_inputs("location")
    outputs = x.collect_inputs("output")
    json_list = x.send_and_receive_data(locs)
    if json_list == None: #Checks if json text returns a statuscode of 0. If statuscode is not 0, then it prints out Invalid inputs. 
        print("Invalid inputs")
    else:
        x.printOutputs(json_list, outputs)

    print()
    print("Directions Courtesy of MapQuest; Map Data Copyright OpenStreetMap Contributors")

    
