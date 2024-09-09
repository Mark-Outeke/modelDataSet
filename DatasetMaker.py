import json
import csv
import os

# Define the directory where your JSON files are located
data_directory = "C:\\Dev\\Model Data set"

# Step 1: Load enrollment JSON file (trackedEntityInstance as the first column)
with open(os.path.join(data_directory, 'Enrollments.json'), 'r') as f:
    enrollments = json.load(f)

# Step 2: Load the other JSON files containing data elements
with open(os.path.join(data_directory,'Output.json'), 'r') as f:
    output_data = json.load(f)

with open(os.path.join(data_directory,'1-2 Weeks treatmentStageOutputtest.json'), 'r') as f:
    week_1_2_data = json.load(f)
with open(os.path.join(data_directory,'3-4 Weeks treatmentStageOutputtest.json'), 'r') as f:
    week_3_4_data = json.load(f)
with open(os.path.join(data_directory,'5-6 Weeks treatmentStageOutputtest.json'), 'r') as f:
    week_5_6_data = json.load(f)
with open(os.path.join(data_directory,'7-8 Weeks treatmentStageOutputtest.json'), 'r') as f:
    week_7_8_data = json.load(f)
with open(os.path.join(data_directory,'Month 3 treatmentStageOutputtest.json'), 'r') as f:
    Month_3_data = json.load(f)
with open(os.path.join(data_directory,'Month 4 treatmentStageOutputtest.json'), 'r') as f:
    Month_4_data = json.load(f)
with open(os.path.join(data_directory,'Month 5 treatmentStageOutputtest.json'), 'r') as f:
    Month_5_data = json.load(f)                     
# Repeat the above for all other treatment stage files (e.g., 3-4 Weeks, 5-6 Weeks, etc.)
# Load other treatment stage files similarly (example for Month 6 treatmentstage)
with open(os.path.join(data_directory,'Month 6 treatmentStageOutputtest.json'), 'r') as f:
    Month_6_data = json.load(f)
with open(os.path.join(data_directory,'Month 7 treatmentStageOutputtest.json'), 'r') as f:
    Month_7_data = json.load(f)    

with open(os.path.join(data_directory,'treatmentoutcome1.json'), 'r') as f:
    treatment_outcome_data = json.load(f)

with open(os.path.join(data_directory,'Month 3 FollowUpLabResults.json'), 'r') as f:
    Month_3_followup_data = json.load(f)

with open(os.path.join(data_directory,'Month 6 FollowUpLabResults.json'), 'r') as f:
    Month_6_followup_data = json.load(f)

with open(os.path.join(data_directory,'Month 7 FollowUpLabResults.json'), 'r') as f:
    Month_7_followup_data = json.load(f)
# Step 3: Create a function to match data elements from the JSON files based on trackedEntityInstance
def get_data_elements_for_instance(instance_id, json_data):
    # Extract data elements from the provided JSON data for the given instance ID
    data_elements = {}
    for entry in json_data['events']:  # Adjust this key based on actual structure
        if entry['trackedEntityInstance'] == instance_id:
            for data_value in entry['dataValues']:
                data_elements[data_value['dataElement']] = data_value['value']
    return data_elements

# Step 4: Prepare the combined data for CSV
combined_data = []

# Iterate over each tracked entity instance in the enrollment file
for enrollment in enrollments:
    tei_id = enrollment['trackedEntityInstance']
    row_data = {'TrackedEntityInstance': tei_id}
    
    # Step 5: Add data from output.json
    output_elements = get_data_elements_for_instance(tei_id, output_data)
    row_data.update(output_elements)
    
    # Step 6: Add data from 1-2 Weeks treatment stage and more...
    week_1_2_elements = get_data_elements_for_instance(tei_id, week_1_2_data)
    row_data.update(week_1_2_elements)

    week_3_4_elements = get_data_elements_for_instance(tei_id, week_3_4_data)
    row_data.update(week_3_4_elements)

    week_5_6_elements = get_data_elements_for_instance(tei_id, week_5_6_data)
    row_data.update(week_5_6_elements)

    week_7_8_elements = get_data_elements_for_instance(tei_id, week_7_8_data)
    row_data.update(week_7_8_elements)

    Month_3_elements = get_data_elements_for_instance(tei_id, Month_3_data)
    row_data.update(Month_3_elements)

    Month_4_elements = get_data_elements_for_instance(tei_id, Month_4_data)
    row_data.update(week_1_2_elements)

    Month_5_elements = get_data_elements_for_instance(tei_id, Month_5_data)
    row_data.update(week_1_2_elements)

    Month_6_elements = get_data_elements_for_instance(tei_id, Month_6_data)
    row_data.update(week_1_2_elements)
    
    month_3_followup_elements = get_data_elements_for_instance(tei_id, Month_3_followup_data)
    row_data.update(month_3_followup_elements)

    month_6_followup_elements = get_data_elements_for_instance(tei_id, Month_6_followup_data)
    row_data.update(month_6_followup_elements)

    month_7_followup_elements = get_data_elements_for_instance(tei_id, Month_7_followup_data)
    row_data.update(month_7_followup_elements)
    
    
    # Step 8: Add data from treatmentoutcome1.json
    treatment_outcome_elements = get_data_elements_for_instance(tei_id, treatment_outcome_data)
    row_data.update(treatment_outcome_elements)

    # Append the row data to the combined data list
    combined_data.append(row_data)

# Step 9: Define the CSV file and write the combined data to it
csv_file = 'combined_data.csv'

# Extract fieldnames (columns) from the first row of combined data
# Dynamically generate fieldnames by collecting all unique keys from combined_data
fieldnames = set()
for row in combined_data:
    fieldnames.update(row.keys())
fieldnames = list(fieldnames)

#fieldnames = ['TrackedEntityInstance'] + list(combined_data[0].keys())[1:]

# Step 10: Write the combined data to a CSV file
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined_data)
else:
    # If file exists, append the data without writing headers again
    with open(csv_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(combined_data)

print(f"Data successfully combined and written to {csv_file}")
