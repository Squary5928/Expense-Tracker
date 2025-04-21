import csv
import os
from datetime import datetime
from textwrap import wrap
from colorama import Fore, Back, Style, init

FILENAME = 'expenses.csv'
init()

# Create CSV file if it doesn't exist
if not os.path.exists(FILENAME):
    with open(FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Category', 'Amount', 'Note'])

# Main menu loop
while True:
    os.system('clear')
    print(Fore.YELLOW + "====" + Fore.GREEN + "Squary's" + Fore.BLUE + " Expense " +Fore.RED + "Tracker" + Fore.YELLOW + "====\n" + Style.RESET_ALL)
    print("1) Add expense")
    print("2) View expenses")
    print("3) Edit/Delete expense")
    print("4) Clear all expenses")
    print("5) Export to PDF")
    print("6) Exit\n")

    choice = input("Choose an option: ")

    # Option 1: Add expense
    if choice == "1":
        os.system('clear')
        date = input("Enter date (YYYY-MM-DD) [Leave blank for today]: ").strip()
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        category = input("Enter category: ").strip()
        amount = input("Enter amount: ").strip()
        note = input("Enter note (optional): ").strip()

        with open(FILENAME, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount, note])

        input("\nExpense added! Press Enter to go to the menu.")

    # Option 2: View expenses
    elif choice == "2":
        os.system('clear')
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        if len(data) <= 1:
            print("No expenses recorded yet.")
        else:
            from tabulate import tabulate

            table_data = []
            for idx, row in enumerate(data[1:], start=1):
               date, category, amount, note = row
               note = "\n".join(wrap(note, 15))
               table_data.append([idx, date, category, amount, note])

            headers = ["No.", "Date", "Category", "Amount", "Note"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        input("\nPress Enter to go to the menu.")

    # Option 3: Edit or Delete
    elif choice == "3":
        os.system('clear')
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        if len(data) <= 1:
            print("No expenses to edit.")
        else:
            for i, row in enumerate(data[1:], start=1):
                print(f"{i}) {row[0]} | {row[1]} | {row[2]} | {row[3]}")
            try:
                num = int(input("\nEnter the number of the entry to edit/delete: "))
                if num < 1 or num > len(data) - 1:
                    raise ValueError
                action = input("Type 'edit' or 'delete': ").strip().lower()
                if action == 'delete':
                    confirm1 = input("Are you sure you want to delete this expense? (y/n): ")
                    if confirm1 == "y":
                       del data[num]
                       print("Expense deleted.")
                    elif confirm1 == "n":
                       print("Cancelled operation.")
                elif action == 'edit':
                    print("Leave blank to keep old value.")
                    date = input(f"New date ({data[num][0]}): ") or data[num][0]
                    category = input(f"New category ({data[num][1]}): ") or data[num][1]
                    amount = input(f"New amount ({data[num][2]}): ") or data[num][2]
                    note = input(f"New note ({data[num][3]}): ") or data[num][3]
                    data[num] = [date, category, amount, note]
                    print("Expense updated.")
                else:
                    print("Cancelled.")
            except:
                print("Invalid input.")

            # Save changes
            with open(FILENAME, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)

        input("Press Enter to go to the menu.")

    # Option 4: Clear all data
    elif choice == "4":
        os.system('clear')
        confirm = input(Back.RED + "WARNING!" + Style.RESET_ALL + " Are you sure you want to delete all expenses? (y/n): ").lower()
        if confirm == "y":
            with open(FILENAME, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Category', 'Amount', 'Note'])
            print("All expenses cleared.")
        else:
            print("Cancelled.")
        input("Press Enter to go to the menu.")

    # Option 5: Export to PDF
    elif choice == "5":
        os.system('clear')
        from fpdf import FPDF

        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", 'B', 18)
                self.set_text_color(0, 102, 204)
                self.cell(0, 12, "Expense Report", ln=1, align='C')
                self.ln(4)

        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        if len(data) <= 1:
            print("No expenses to export.")
        else:
            path = input("Enter full path to save PDF in " + Fore.YELLOW + "(e.g. saving it as /sdcard/Download/(your filename).pdf will make it visible in your Downloads folder in your files app.)" + Style.RESET_ALL + ": ").strip()
            if not path.endswith(".pdf"):
                path += ".pdf"

            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            headers = data[0]
            col_widths = [40, 40, 30, 70]

            pdf.set_fill_color(0, 102, 204)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", 'B', 13)

            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 12, header, border=1, fill=True, align='C')
            pdf.ln()

            pdf.set_font("Arial", size=11)
            pdf.set_text_color(0, 0, 0)

            total = 0.0
            fill = False

            for row in data[1:]:
                try:
                    total += float(row[2])
                except:
                    pass
                pdf.set_fill_color(245, 245, 245) if fill else pdf.set_fill_color(255, 255, 255)
                for i, cell in enumerate(row):
                    if len(cell) > 35:
                        cell = cell[:32] + "..."
                    pdf.cell(col_widths[i], 12, cell, border=1, fill=True)
                pdf.ln()
                fill = not fill

            pdf.ln(5)
            pdf.set_font("Arial", 'B', 13)
            pdf.set_text_color(0, 102, 204)
            pdf.cell(0, 10, f"Total Spent: {total:.2f}", ln=1, align='R')

            pdf.output(path)
            print(f"Exported expenses to {path}!")

        input("Press Enter to continue...")

    # Option 6: Exit
    elif choice == "6":
        os.system('clear')
        print("Goodbye!")
        break
