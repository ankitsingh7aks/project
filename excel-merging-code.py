import pandas as pd
import os

# **User-Defined Column Names (Update the target columns here if needed)**
# Here the user should define the columns for the target file. These will be the final columns in the target file.
target_columns = [
    'import_id',    # Column for the import ID from Source 1
    'IP',            # Column for the IP address from Source 1
    'Qid',           # Column for the QID from Source 1
    'Threat',        # Column for the threat description from Source 1
    'Severity',      # Column for the severity level from Source 1
    'Tag',           # Column for the Tag from Source 2
    'Status',        # Column for the Status from Source 2
    'server_owner',  # Column for the server owner from Source 3
    'support_group'  # Column for the support group from Source 3
]

# **Column Mappings for the Source Files to Target File Columns**
# The user must define how the columns from each source file map to the target file.
source1_mapping = {
    'import_id': 'import_id',  # Source 1 'import_id' to Target 'import_id'
    'IP': 'IP',                # Source 1 'IP' to Target 'IP'
    'Qid': 'Qid',              # Source 1 'Qid' to Target 'Qid'
    'Threat': 'Threat',        # Source 1 'Threat' to Target 'Threat'
    'Severity': 'Severity'     # Source 1 'Severity' to Target 'Severity'
}

source2_mapping = {
    'import_id': 'import_id',  # Source 2 'import_id' to Target 'import_id'
    'Id': 'Id',                # Source 2 'Id' to Target 'Id' (this can be used if necessary)
    'Tag': 'Tag',              # Source 2 'Tag' to Target 'Tag'
    'Status': 'Status'         # Source 2 'Status' to Target 'Status'
}

source3_mapping = {
    'IP': 'IP',                 # Source 3 'IP' to Target 'IP'
    'hostname': 'hostname',     # Source 3 'hostname' to Target 'hostname' (this can be used if needed)
    'server_owner': 'server_owner',  # Source 3 'server_owner' to Target 'server_owner'
    'support_group': 'support_group'  # Source 3 'support_group' to Target 'support_group'
}

# **Default Source File Names (Update only if you want to specify default names)**
# If the user doesn't enter the file names, these default values will be used.
default_source1_filename = 'source1.xlsx'
default_source2_filename = 'source2.xlsx'
default_source3_filename = 'source3.xlsx'

def create_target_file(target_columns, source1_filename, source2_filename, source3_filename, output_filename):
    """
    Creates a target file using three source files.
    - Source 1 provides 'import_id' and 'IP'.
    - Source 2 is merged using 'import_id'.
    - Source 3 is merged using 'IP'.
    - The user defines the mapping of source columns to target columns.
    - If no match is found, fills missing values with '#N/A'.
    """

    # **Step 1: Create an Empty Target DataFrame with User-Defined Columns**
    target_df = pd.DataFrame(columns=target_columns)

    # **Step 2: Load Source 1 and Extract the Relevant Columns**
    source1_path = os.path.join(os.getcwd(), source1_filename)  # Use current directory for the file
    source1_df = pd.read_excel(source1_path, sheet_name=0)  # Load the first sheet by default
    source1_df.rename(columns=source1_mapping, inplace=True)

    # Extract the import_id and IP from source1_df and initialize target_df with import_id
    target_df['import_id'] = source1_df['import_id']  # Add import_id from Source 1
    target_df['IP'] = source1_df['IP']                # Add IP from Source 1

    # **Step 3: Load Source 2 and Merge Using 'import_id'**
    source2_path = os.path.join(os.getcwd(), source2_filename)  # Use current directory for the file
    source2_df = pd.read_excel(source2_path, sheet_name=0)  # Load the first sheet by default
    source2_df.rename(columns=source2_mapping, inplace=True)

    # Merge on 'import_id' (left join ensures we preserve all rows from source1)
    target_df = target_df.merge(source2_df, on='import_id', how='left')

    # **Step 4: Load Source 3 and Merge Using 'IP'**
    source3_path = os.path.join(os.getcwd(), source3_filename)  # Use current directory for the file
    source3_df = pd.read_excel(source3_path, sheet_name=0)  # Load the first sheet by default
    source3_df.rename(columns=source3_mapping, inplace=True)

    # Merge on 'IP' (left join ensures we preserve all rows from source1)
    target_df = target_df.merge(source3_df, on='IP', how='left')

    # **Step 5: Fill Missing Values with '#N/A'**
    target_df.fillna('#N/A', inplace=True)

    # **Step 6: Save the Final Target File**
    # Ensure the output filename has the proper extension
    if not output_filename.endswith('.xlsx'):
        output_filename += '.xlsx'
    
    output_path = os.path.join(os.getcwd(), output_filename)  # Save in the current directory
    target_df.to_excel(output_path, index=False, engine='openpyxl')  # Specify engine to avoid ambiguity
    print(f"✅ Target file successfully created and saved as '{output_filename}'.")

    return target_df


# **Main Execution Flow**

# Request User Input for Source File Names
source1_filename = input(f"Enter the filename for Source 1 file (default: '{default_source1_filename}'): ") or default_source1_filename
source2_filename = input(f"Enter the filename for Source 2 file (default: '{default_source2_filename}'): ") or default_source2_filename
source3_filename = input(f"Enter the filename for Source 3 file (default: '{default_source3_filename}'): ") or default_source3_filename

# Request User Input for Output File Name
output_filename = input("Enter the name for the output target file (e.g., 'target_output.xlsx'): ")

# **Create the Target File**
result_df = create_target_file(target_columns, source1_filename, source2_filename, source3_filename, output_filename)

# **Print the resulting DataFrame (optional)**
print(result_df)
