from app.add_item import add_item
from app.match_item import match_items

def main():
    while True:
        print("\n--- Lost & Found Portal ---")
        print("1. Add Lost/Found Item")
        print("2. Match Lost/Found Items")
        print("3. Exit")

        choice = input("Please select an option (1-3): ").strip()

        if choice == '1':
            add_item()
        elif choice == '2':
            match_items()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
