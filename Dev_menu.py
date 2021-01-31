
##################################################################################################################
"""
The Dev_menu script is used to initiate all economic analysis, trading simulations,
and economic model parameters evaluations and optimisations.

Dev menu-based runs used the class based setting system, settings can be adjusted in the PhyTrade settings/class based settings folder
"""

# Built-in/Generic Imports
import json

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Data_Collection_preparation.Fetch_parameter_set_labels_df import fetch_parameter_set_labels_df
from PhyTrade.Tools.Colours_and_Fonts import cf
from PhyTrade.Tools.RUN_protocols import RUN_protocols

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################

# --> Set settings mode to 0 to use class based settings
with open(r"Settings\settings_mode.json",
          'w') as fout:
    json.dump(0, fout, indent=4)

print(cf["bold"] + cf["cyan"] + "\n-- Welcome to the PhyTrade Economic analyser and modeling tool --" + cf["reset"])
print("\nSelect the wanted run process:")
print(cf["bold"] + "\n> == Model training and optimisation == <" + cf["reset"])
print(cf["green"] + "1 - RUN EVOA Optimiser" + cf["reset"])
print(cf["green"] + "2 - GEN EVOA Metalabels" + cf["reset"])

print(cf["bold"] + "\n> == Model and parameter evaluation == <" + cf["reset"])
print(cf["green"] + "3 - RUN Model" + cf["reset"])

print(cf["bold"] + "\n> == Trading simulations == <" + cf["reset"])

print(cf["green"] + "4 - RUN Single ticker trading simulation" + cf["reset"])
print(cf["green"] + "5 - RUN Multi ticker trading simulation" + cf["reset"])

print(cf["bold"] + "\n> == Run protocols == <" + cf["reset"])
print(cf["green"] + "6 - RUN/define Protocol" + cf["red"] + "(In development)" + cf["reset"])

print("\n-------------------------------------------------------------------------")
print("Parameter sets available:")
fetch_parameter_set_labels_df()

print("\n" + cf["red"] + "0 - Exit" + cf["reset"])

run = True
while run is True:
    selection = int(input("\nSelection: "))
    # selection = 1
    settings = SETTINGS()
    print("\n")

    # --> Run a single process
    if type(selection) == int and selection != 6 and selection != 0:
        RUN_protocols([selection])

    # --> Run a protocol
    elif selection == 6:
        available_tasks = ["--> EVOA Optimiser",
                           "--> EVOA Metalabeling",
                           "--> Economic analysis",
                           "--> Single ticker trade simulation",
                           "--> Multi ticker trade simulation"]

        predefined_protocols = [[1, 2, 4], [1, 2, 5], [1, 3]]

        print("----------------------------------------")
        print(cf["bold"] + "Available processes: 6" + cf["reset"])
        print("EVOA Optimiser                        (1)")
        print("EVOA Metalabeling                     (2)")
        print("Economic analysis                     (3)")
        print("Single ticker trade simulation        (4)")
        print("Multi ticker trade simulation         (5)")

        print(cf["bold"] + "\nGenerate new protocol    - 1")
        print("Predefined protocol      - 2" + cf["reset"])

        protocol_selection = int(input("\nSelection: "))

        print("\n----------------------------------------")
        if protocol_selection == 1:
            print(cf["bold"] + "\nEnter each task individually and validate with enter. Enter 0 once Protocol is finished." + cf["reset"])
            task_sequence = []
            task = None

            while task != 0:
                task = int(input("\nEnter task: "))
                while task > len(available_tasks):
                    print(cf["red"] + "Incorrect task key, (max key:" + str(len(available_tasks)) + ")" + cf["reset"])
                    task = int(input("\nEnter task: "))

                if task == 0:
                    break
                task_sequence.append(task)

                # --> Print current protocol sequence defined
                print(cf["bold"] + "\n---- Current Protocol process sequence: ----" + cf["reset"])
                for i in task_sequence:
                    print(available_tasks[i-1])

            # --> Print final protocol
            print("\n------------------------")
            print(cf["bold"] + "RUN Protocol:\n" + cf["reset"])
            for i in task_sequence:
                print(available_tasks[i - 1])

            confirmation = str(input("\nEnter 'True' to confirm run and initiate protocol or 'False' to redefine: "))

            if confirmation == "True":
                RUN_protocols(task_sequence)
            else:
                print(cf["bold"] + cf["red"] + "Protocol initiation Aborted" + cf["reset"])

        else:
            for i, protocol in enumerate(predefined_protocols):
                print("\nProtocol " + str(i+1) + ":")
                for task in protocol:
                    print(available_tasks[task - 1])

            protocol_reference = int(input("\nEnter pre-defined Protocol reference: "))
            RUN_protocols(predefined_protocols[protocol_reference-1])

    elif selection == 0:
        import sys
        sys.exit()

    else:
        print("Invalid selection")


