import os
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def break_into_rows(data, rows, cols):
    """
    Step 1: Break the data into rows for easier processing.
    """
    x_grid = data['X'].values.reshape(rows, cols)
    y_grid = data['Y'].values.reshape(rows, cols)
    z_grid = data['Z'].values.reshape(rows, cols)  # Include Z if needed
    return x_grid, y_grid, z_grid

def reverse_even_rows(x_grid, y_grid, z_grid, rows):
    """
    Step 2: Reverse the order of even rows (0-based indexing).
    """
    for i in range(rows):
        if i % 2 == 1:  # Reverse even rows
            x_grid[i] = x_grid[i][::-1]
            y_grid[i] = y_grid[i][::-1]
            z_grid[i] = z_grid[i][::-1]  # Ensure Z is reversed too
    return x_grid, y_grid, z_grid

def combine_back_to_df(x_grid, y_grid, z_grid):
    """
    Step 3: Combine the processed rows back into a single DataFrame.
    """
    x_new = x_grid.flatten()
    y_new = y_grid.flatten()
    z_new = z_grid.flatten()
    count_column = list(range(len(x_new)))  # Generate the index column starting at 0
    return pd.DataFrame({
        "": count_column,  # First column with a blank header
        "X": x_new,
        "Y": y_new,
        "Z": z_new
    })

def process_snake_pattern(rows, cols):
    """
    Full process to reverse the snake pattern using a file dialog.
    """
    # Open file dialog to select CSV
    Tk().withdraw()  # Hide the root Tkinter window
    input_file = askopenfilename(
        title="Select the input CSV file",
        filetypes=[("CSV files", "*.csv")]
    )

    if not input_file:
        print("No file selected. Exiting...")
        return

    try:
        # Load the CSV file
        data = pd.read_csv(input_file)

        # Step 1: Break into rows
        x_grid, y_grid, z_grid = break_into_rows(data, rows, cols)

        # Step 2: Reverse even rows
        x_grid, y_grid, z_grid = reverse_even_rows(x_grid, y_grid, z_grid, rows)

        # Step 3: Combine back into a single DataFrame
        rearranged_data = combine_back_to_df(x_grid, y_grid, z_grid)

        # Generate output filename
        folder, filename = os.path.split(input_file)
        name, ext = os.path.splitext(filename)
        output_file = os.path.join(folder, f"{name}_unsnaked{ext}")

        # Save the rearranged data to a new CSV file
        rearranged_data.to_csv(output_file, index=False)
        print(f"Rearranged file saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Define the number of rows and columns for the plate
    rows = 6  # Adjust as needed
    cols = 8  # Adjust as needed

    # Process the file
    process_snake_pattern(rows, cols)
