import csv
import os

script_dir = os.path.dirname(os.path.abspath(__file__)) #sets the working directory to the directory that the script is currently located
os.chdir(script_dir)

#create a new file output directory 'analysis' in the script directory if it does not exist
file_output_dir = os.path.join(script_dir, 'analysis')
if not os.path.exists(file_output_dir):
    os.mkdir(file_output_dir)

#name the output files and output file paths
output_file_path_budget = os.path.join(file_output_dir, 'budget_calculations_output.txt')

#point to the input files
csv_path_budget = os.path.join(script_dir, 'Resources', 'budget_data.csv') #points to the data file in subdirectory 'Resources' in the script working directory

#define a special function to output to the terminal and to a text file simultaneously
def print_to_term_and_write_to_file(text, file): 
    print(text)
    file.write(text + '\n')
    
#define variables needed for budget calculations 
total_profit_loss = 0
number_of_months = 0
monthly_profit_loss = 0
highest_profit = 0
highest_loss = 0
monthly_diff = 0
previous_month_profit_loss = None
highest_profit_month = None
highest_loss_month = None
monthly_differences_list = []
header_labels_budget = None #variable for storing the column headers of the CSV file

with open(csv_path_budget, 'r', encoding='UTF-8') as csv_file:  #open the CSV file from the Resources directory
    
    csv_reader = csv.DictReader(csv_file, delimiter=',') #create a dictionary using DictReader class (of CSV module) with the first row of the CSV file as set as the keys and values in the rows assocaited with the keys
    
    header_labels_budget = csv_reader.fieldnames #stores the first (header) row of the CSV file as a variable - this doesn't seem necessary when using csv.DictReader to read in the CSV file, but this is how you would do it in this script
    
    for row in csv_reader:
        
        #for each row in the CSV file that had data under the column header 'Date' add 1 to the month total counter  
        if 'Date' in row:
            number_of_months += 1
            
        #for each row in the CSV file that has data under the column header 'Profit/Losses' add to a running sum to calculate total profit and losses over the entire dataset    
        if 'Profit/Losses' in row:          
            total_profit_loss += float(row['Profit/Losses'])
            monthly_profit_loss = float(row['Profit/Losses']) #sends the profits/losses data for each row to a variabe for further calculations
    
        if previous_month_profit_loss is not None: #check to make sure the previous profits/losses row contains data (the first row of data will have no previous month to compare to since it is the first entry in the CSV file)
            monthly_diff = monthly_profit_loss - previous_month_profit_loss  #subtract previous row profit/loss from current row profit/loss to find the month to month difference
            monthly_differences_list.append(monthly_diff)  #append the current month to month profit/loss difference to a list that stores all the month to month profit/loss differences for later overall monthly profit/loss mean (average) calculation
       
        #this if/elif section stores the highest and lowest monthly profit/loss differences and the corresponding date information
        if  monthly_diff > highest_profit:  
            highest_profit = monthly_diff
            highest_profit_month = str(row['Date'])
        elif monthly_diff < highest_loss:
            highest_loss = monthly_diff
            highest_loss_month = str(row['Date'])
            
        previous_month_profit_loss = monthly_profit_loss #before moving to the next row, set the previous month profit/loss variable to the current row profit/loss value

    mean_monthly_diff = float(sum(monthly_differences_list)) / (number_of_months - 1) #calculate the mean month to month profit/loss from the list of monthly differences we stored as we iterated through the rows

#round all of the output variables to desired number of decimal places
rounded_mean_monthly_diff = round(mean_monthly_diff, 2)
rounded_total_profit_loss = round(total_profit_loss, 0)
rounded_highest_loss = round(highest_loss, 0)
rounded_highest_profit = round(highest_profit, 0)

#print all of the desired outputs to the terminal and send the data to a text file        
with open(output_file_path_budget, "w") as file:
    print()
    print_to_term_and_write_to_file("Financial Analysis", file)
    print_to_term_and_write_to_file("-------------------------", file)
    print_to_term_and_write_to_file(f"Total Months: {number_of_months}", file)
    print_to_term_and_write_to_file(f"Total: ${rounded_total_profit_loss:.0f}", file)
    print_to_term_and_write_to_file(f"Average Change: ${rounded_mean_monthly_diff}", file)
    print_to_term_and_write_to_file(f"Greatest Increase in Profits: {highest_profit_month} (${rounded_highest_profit:.0f})", file)
    print_to_term_and_write_to_file(f"Greatest Decrease in Profits: {highest_loss_month} (${rounded_highest_loss:.0f})", file)