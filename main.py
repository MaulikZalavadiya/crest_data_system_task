import os
import pandas as pd


class FileProcessor:
    """
    Class to process data from multiple dat files and generate a result CSV file.

    Parameters:
    -----------
    input_folder : str
        Path to the folder containing input dat files.
    output_folder : str
        Path to the folder where the result CSV file will be saved.

    Methods:
    --------
    manage_files():
        Reads all dat files from the input folder, processes the data, calculates gross salary,
        and saves the result to the output folder with required footer details.
    """

    def __init__(self, input_folder, output_folder):
        # Initialize the class with input and output folder paths
        self.input_folder = input_folder
        self.output_folder = output_folder

    def manage_files(self):
        try:
            # Initialize an empty DataFrame to accumulate all data
            all_data = pd.DataFrame()

            # Loop through each .dat file in the input folder
            if not os.path.exists(self.input_folder):
                raise FileNotFoundError(f"Input folder '{self.input_folder}' does not exist.")

            dat_files = [f for f in os.listdir(self.input_folder) if f.endswith('.dat')]
            if not dat_files:
                raise FileNotFoundError("No .dat files found in the input folder.")

            for filename in dat_files:
                file_path = os.path.join(self.input_folder, filename)  # Construct the full file path
                try:
                    data = pd.read_csv(file_path, sep='\t')  # Read the .dat file into a DataFrame
                    all_data = pd.concat([all_data, data], ignore_index=True)  # Append data to the accumulated DataFrame
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

            # Remove duplicate rows if any
            all_data.drop_duplicates(inplace=True)

            # Proceed if there is data to process
            if not all_data.empty:
                all_data = all_data.head(10)  # Take the first 10 rows

                try:
                    # Calculate the gross salary
                    all_data['gross_salary'] = all_data['basic_salary'] + all_data['allowances']
                    gross_salaries = all_data['gross_salary'].dropna().astype(float)  # Extract and convert gross salaries to float
                except KeyError as e:
                    raise KeyError(f"Missing required columns: {e}")

                # Calculate the second highest salary
                if len(gross_salaries) > 1:
                    second_highest_salary = gross_salaries.nlargest(2).iloc[-1]
                else:
                    second_highest_salary = gross_salaries.iloc[0] if not gross_salaries.empty else None

                average_salary = gross_salaries.mean()  # Calculate the average salary

                # Prepare the output DataFrame
                result_data = all_data[['id', 'first_name', 'last_name', 'email', 'job_title', 'basic_salary', 'allowances', 'gross_salary']]

                # Ensure the output folder exists
                os.makedirs(self.output_folder, exist_ok=True)

                output_file_path = os.path.join(self.output_folder, 'result.csv')  # Set the output file path

                # Write the DataFrame to a CSV file
                result_data.to_csv(output_file_path, index=False)

                # Append the salary details footer to the CSV file
                with open(output_file_path, 'a', newline='') as file:
                    file.write(f"\nSecond Highest Salary: {second_highest_salary}\n")
                    file.write(f"Average Salary: {average_salary}\n")

                print(f"Processed data saved to: {output_file_path}")
            else:
                print("No valid data found to process.")

        except FileNotFoundError as e:
            print(f"File not found error: {e}")
        except KeyError as e:
            print(f"Key error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Define the paths for the input and output folders
    employee_info = os.path.join(os.getcwd(), 'employee_info')
    employee_result = os.path.join(os.getcwd(), 'employee_result')

    # Create an instance of FileProcessor and call manage_files
    processor = FileProcessor(employee_info, employee_result)
    processor.manage_files()
