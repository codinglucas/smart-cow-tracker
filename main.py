import os
import sys

# Add parent directory to path for imports to work properly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import local modules
from logger.bluetooth_reader import get_weight
from logger.data_logger import log_to_excel  # This will be our updated Excel handler
from analyzer.trend_analyzer import plot_trends

def main():
    # Make sure all necessary directories exist
    os.makedirs('data', exist_ok=True)

    choice='empty'
    
    while True:
        if choice == '2':
        # View trends flow
            try:
                pred_option = input("Include prediction? (y/n): ").strip().lower()
                show_prediction = pred_option == 'y'
                
                print("Loading weight trends...")
                plot_trends(show_prediction)
            except Exception as e:
                print(f"Error displaying trends: {e}")

        print("\nSmart Cow Tracker")
        print("1. Weigh a cow")
        print("2. View weight trends")
        print("3. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            # Weight measurement flow
            try:
                cow_id = input("Enter Cow ID: ")
                
                # Validate cow ID (basic validation)
                if not cow_id.strip():
                    print("Error: Cow ID cannot be empty.")
                    continue
                
                print("Waiting for weight from Tru-Test...")
                weight = get_weight()
                
                if weight:
                    # Validate weight
                    try:
                        weight = float(weight)
                        if weight <= 0:
                            print("Error: Weight must be a positive number.")
                            continue
                    except ValueError:
                        print("Error: Weight must be a valid number.")
                        continue
                    
                    # Log data with our new horizontal Excel structure
                    log_to_excel(cow_id, weight)
                    print(f"Logged: Cow {cow_id} - {weight} kg")
                    
                    # Optional: Show confirmation of all weights for this cow
                    show_history = input("Show weight history for this cow? (y/n): ").strip().lower()
                    if show_history == 'y':
                        # This would require a new function to read and display the history
                        # For now, we'll just suggest viewing trends
                        choice = '2'
                        continue
                else:
                    print("Failed to get weight.")
                    
                    # Fallback to manual entry
                    manual_entry = input("Enter weight manually? (y/n): ").strip().lower()
                    if manual_entry == 'y':
                        try:
                            manual_weight = float(input("Enter weight in kg: "))
                            if manual_weight <= 0:
                                print("Error: Weight must be a positive number.")
                                continue
                                
                            log_to_excel(cow_id, manual_weight)
                            print(f"Logged: Cow {cow_id} - {manual_weight} kg")
                        except ValueError:
                            print("Invalid weight entered. Returning to menu.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '2':
        # View trends flow
            try:
                pred_option = input("Include prediction? (y/n): ").strip().lower()
                show_prediction = pred_option == 'y'
                
                print("Loading weight trends...")
                plot_trends(show_prediction)
            except Exception as e:
                print(f"Error displaying trends: {e}")
                
                
        elif choice == '3':
            # Exit the program
            print("Exiting Smart Cow Tracker. Goodbye!")
            break
            
        else:
            print("Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()