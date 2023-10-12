import csv
import os

script_dir = os.path.dirname(os.path.abspath(__file__)) #sets the working directory to the directory that the script is currently located
os.chdir(script_dir)

#create a new file output directory 'analysis' in the script directory if it does not exist
file_output_dir = os.path.join(script_dir, 'analysis')
if not os.path.exists(file_output_dir):
    os.mkdir(file_output_dir)

#name the output files and output file paths
output_file_path_election = os.path.join(file_output_dir, 'election_tabulation_output.txt')

#point to the input files in subdirectory 'Resources' in the script working directory
csv_path_election = os.path.join(script_dir, 'Resources', 'election_data.csv')

#define a special function to output to the terminal and to a text file simultaneously
def print_to_term_and_write_to_file(text, file): 
    print(text)
    file.write(text + '\n')
    
#define variables needed for ballot tabulations
unique_candidates = {} #create a dictionary to store the unique candidate names
candidate_name = None #variable for use in summing vote totals for each unique candidate
number_of_ballots = 0  #variabe for storing the number of total ballots
top_vote_getter = None #variable for storing candidate name with most votes
top_vote_getter_counts = 0 #variable for storing the vote counts for the candidate with most votes

with open(csv_path_election, 'r', encoding='UTF-8') as csv_file:  #open the CSV file from the Resources directory
    
    csv_reader = csv.DictReader(csv_file, delimiter=',') #create a dictionary using DictReader class (of CSV module) with the first row of the CSV file as set as the keys and values in the rows assocaited with the keys
    
    header_labels_ballots = csv_reader.fieldnames #stores the first (header) row of the CSV file as a variable - this doesn't seem necessary when using csv.DictReader to read in the CSV file, but this is how you would do it in this script
    
    for row in csv_reader:   
        
        #if statement for counting overall ballot total
        if 'Ballot ID' in row:  
            number_of_ballots += 1
        
        # if statement for counting ballot totals for each unique candidate    
        candidate_name = row['Candidate']   
        if candidate_name in unique_candidates:
            unique_candidates[candidate_name] += 1
        else:
            unique_candidates[candidate_name] = 1
           
#printing all desired outputs to terminal and to file
print(header_labels_ballots)
with open(output_file_path_election, "w") as file:
    print()
    print_to_term_and_write_to_file("Election Results", file)
    print_to_term_and_write_to_file("-------------------------", file)
    print_to_term_and_write_to_file(f"Total Votes: {number_of_ballots}", file)
    print_to_term_and_write_to_file("-------------------------", file)
    
    #loop for printing the name of each individual unique candidate, their % of the total vote, and their total number of votes
    for candidate_name, unique_candidate_counts in unique_candidates.items():
        unique_candidate_percent_vote = (unique_candidate_counts / number_of_ballots) * 100
        rounded_unique_candidate_percent_vote = round(unique_candidate_percent_vote, 3)   #round the percentage of total votes to 3 decimal places
        
        #find which candidate received the most votes and therefore won the election
        if unique_candidate_counts > top_vote_getter_counts:
            top_vote_getter_counts = unique_candidate_counts
            top_vote_getter = candidate_name
            
        print_to_term_and_write_to_file(f"{candidate_name}: {rounded_unique_candidate_percent_vote}% ({unique_candidate_counts})", file)
    print_to_term_and_write_to_file("-------------------------", file)
    print_to_term_and_write_to_file(f"Winner: {top_vote_getter}", file)
    print_to_term_and_write_to_file("-------------------------", file)