def capitalize_first_letter(file_path):
    try:
        # Open the file and read all lines
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Ensure we don't lose content and capitalize each line safely
        capitalized_lines = [line[:1].upper() + line[1:].lower() if line else '' for line in lines]
        
        # Write back the modified lines to the file
        with open(file_path, 'w') as file:
            file.writelines(capitalized_lines)
        
        print(f"File '{file_path}' has been updated successfully!")
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    file_path = input("Enter the path to your text file: ")
    capitalize_first_letter(file_path)
