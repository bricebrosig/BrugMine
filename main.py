"""
Brug Mine
a program that simulates all the dice rolls that would happen for the downtime activity
of running a mining operation.

You roll a d20 per mine (right now that is fixed at 1) to determine the amount of veins found.
then roll a d100 for each vein to determine the mineral that was found.
then roll the correpsonding quantity modifier dice associated with that to know how much you found.

The program then prints what was found, the amount of gold that is worth, and then the split that will happen
according to the business plan.
"""

from random import random, randint
import pandas as pd
import argparse

# @incomplete have this interface with the google sheet rather than the file on disk
# @incomplete add saving of the total that aoife has to disk and include the partitioning accoriding to the business plan
# @incomplete could be cool to have this run on a flask app so that it could be used without the command line
# @incomplete the ability to more robustly handle different sheet configuratoins would be pretty sweet - allow the user
#             to specify where in the sheet their table is, and how long it is
# @incomplete allow for multiple mines to be rolled for


# === for pretty printing ===
font_norm = '\033[00m'
font_bold = '\033[1m'
font_pink = '\033[95m'
font_blue = '\033[94m'
font_gray = '\033[90m'
font_green = '\033[0;32m'
font_green_bold = '\033[1m\033[0;32m'
font_ul = '\033[4m'
font_ul_pink = font_ul + font_pink
font_blue_underline = font_blue + font_ul
business_plan = {
    'aoife': .5,
    'ops': .35,
    'employees': .15
}

def main(file="data.csv"):
    try:
        data_file = open(file, "r")
    except OSError:
        print(f"Error opening %s file. Check that it is in working directory. Exiting..." % file)
        exit(1)

    df_data = pd.read_csv(data_file, skiprows=[0,1,2,3,4] + [i for i in range(20, 47)], header=None)
    d100_map = [None] * 101  # maps the d100 rol to a mineral name
    quant_mod_dict = {}  # maps mineral name to the quantity modifier dice
    price_per_pound_dict = {}  # maps mineral name to price per pound
    
    print(font_bold, font_pink, "validated data", font_norm)
    print(df_data)
    
    for _, row in df_data.iterrows():
        row = list(row)
        mineral_name = row[0]
        s_range: str = row[2]
        roll_range = s_range.split('-')
        
        if len(roll_range) == 1:
            d100_map[int(roll_range[0])] = mineral_name
        else:
            for index in range(int(roll_range[0]), int(roll_range[1]) + 1):
                d100_map[index] = mineral_name
                
        quant_mod_dict[mineral_name] = int(row[3][1:])
        price_per_pound_dict[mineral_name] = int(row[4][:-2])

    veins_found = randint(1, 20)
    total_gold = 0
    print(font_bold, font_pink, "Mining results", font_norm)
    print(f"%15s%15s%15s" % ('mineral', 'quantity', 'gold'))
    for i in range(veins_found):
        # roll d100 and check that against the table
        find_ore = randint(1, 100)
        mineral_found = d100_map[find_ore]
        quant_roll = randint(1, quant_mod_dict[mineral_found])
        eq_gold_amount = price_per_pound_dict[mineral_found] * quant_roll
        total_gold = total_gold + eq_gold_amount
        print(f"%15s%15d%15d" % (mineral_found, quant_roll, eq_gold_amount))
    
    print(font_green_bold, 'total gold: ', font_norm, total_gold)
    print(font_green_bold, 'aoife:      ', font_norm, total_gold * business_plan['aoife'])
    print(font_green_bold, 'operations: ', font_norm, total_gold * business_plan['ops'])
    print(font_green_bold, 'employees:  ', font_norm, total_gold * business_plan['employees'])
    
    data_file.close()

    
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-d", "--data", metavar="file", type=str, default="data.csv", required=False, help="csv file containing the information about the brug mine")
    args = arg_parser.parse_args()    
    main(args.data)