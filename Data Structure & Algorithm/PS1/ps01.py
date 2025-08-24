import sys


INPUT_FILE_NAME = "inputPS01.txt"
OUTPUT_FILE_NAME = "outputPS01.txt"


class BankDenominationCount:

    def __init__(self, bank_name=None, denomination_count=None, month=None):

        self.bank_name = bank_name.strip()
        _d_cnt = int(denomination_count.strip()) # throws ValueError if not parsed to an integer
        if _d_cnt < 0:
            raise ValueError("denomination count cannot be negative.")
        self.denomination_cnt = _d_cnt
        self.month = month.strip().lower() # lowercase should be equal to "may" or "june"

    def __str__(self):
        return f"{self.bank_name}, {self.denomination_cnt}"

    def __repr__(self):
        return f"BankDenominationCount(bank_name='{self.bank_name}', denomination_count='{self.denomination_cnt}', month='{self.month}')"


def read_bank_details(f_name):
    bank_details_may = [] # hold may month bank details
    bank_details_june = [] # hold june month bank details
    bank_details_new = [] # hold new  bank details
    
    is_new_bank = False
    
    with open(f_name, "r") as bank_details:
        bank_detail = bank_details.readline()
        while bank_detail: # loop till end of file
            bank_detail = bank_detail.strip()
            if bank_detail > "" and bank_detail != "Bank name, note count, month": # skip blank lines and header
                    if bank_detail == "New Bank details:":
                        is_new_bank = True
                    else:
                        try:
                            b = BankDenominationCount(*bank_detail.split(","))                        
                            if is_new_bank:  # input line after new bank details
                                bank_details_new.append(b)
                            elif b.month == "may":
                                bank_details_may.append(b)
                            elif b.month == "june":
                                bank_details_june.append(b)
                            # else skip
                        except ValueError:
                            print(f"Record - '{bank_detail}' was skipped as denomination count is expected to be positive integer.")
                
            bank_detail = bank_details.readline() # read next line
            
    return bank_details_may, bank_details_june, bank_details_new


def write_bank_details(output_file, bank_details, month):
    output_file.write(f"{str.capitalize(month)} month details:\n")
    for b in bank_details:
         output_file.write(f"{b}\n")


def swap(b, i, j): # swap ith and jth elements
    temp = b[i]
    b[i] = b[j]
    b[j] = temp


def max_heapify(bank_details, curr_idx, key_func):
    lc_idx = 2 * curr_idx + 1 # left child index
    rc_idx = 2 * curr_idx + 2 # right child index
    mk_idx = curr_idx         # max key index

    if bank_details:
        size = len(bank_details)
        if lc_idx < size and key_func(bank_details[lc_idx]) > key_func(bank_details[mk_idx]):
            mk_idx = lc_idx

        if rc_idx < size and key_func(bank_details[rc_idx]) > key_func(bank_details[mk_idx]):
            mk_idx = rc_idx

        if mk_idx != curr_idx: # swap if index(max_key) != current node
            swap(bank_details, mk_idx, curr_idx)
            if mk_idx == rc_idx:
                max_heapify(bank_details, rc_idx, key_func)
            else:
                max_heapify(bank_details, lc_idx, key_func)

    else: # bank_details is empty list
        return 

    
def max_heap_build(bank_details, key_func):

    size = len(bank_details)
    start_idx =  (size - 2) // 2 if size  > 1 else 0 # start at last non-leaf node or root node
    for i in range(start_idx, -1, -1): 
        max_heapify(bank_details, i, key_func)


def max_heap_pop(bank_details, key_func):

    l = len(bank_details)
    if l == 0:
        raise IndexError("list is empty")
    elif l > 1:
        b = bank_details[0]
        bank_details[0] = bank_details.pop()
        max_heapify(bank_details, 0, key_func)
        
    else:
        b = bank_details.pop()
    return b
    

def main():

    try:
        bank_details_may, bank_details_june, bank_details_new = read_bank_details(INPUT_FILE_NAME)

        with open(OUTPUT_FILE_NAME, "w") as bank_output_file:

            # Q1 list out the bank name and its ₹2000 note denomination count for both may and june month
            write_bank_details(bank_output_file, bank_details_may, "may")
            bank_output_file.write("\n")
            write_bank_details(bank_output_file, bank_details_june, "june")

            # Q2 caculate total number of ₹2000 notes deposited in all the banks for both months
            total_currency_notes_may = total_currency_notes_june = 0
            for b in bank_details_may:
                total_currency_notes_may += b.denomination_cnt
            for b in bank_details_june:
                total_currency_notes_june += b.denomination_cnt
            bank_output_file.write("\n")
            bank_output_file.write(f"Total Rs 2000 note count for May & June month: '{total_currency_notes_may}' & '{total_currency_notes_june}'\n")

            # Q3 add new bank details to the list and figure out the max Rs 2000 notes deposited in which bank for may & June month.
            bank_output_file.write("\nAdded new bank details:\n")
            for b in bank_details_new:
                bank_output_file.write(f"{b.bank_name}, {b.denomination_cnt}, {str.capitalize(b.month)}\n")
                if b.month == "may":
                    bank_details_may.append(b)
                elif b.month == "june":
                    bank_details_june.append(b)
            key_func = lambda b_det:  b_det.denomination_cnt
            max_heap_build(bank_details_may, key_func)
            bank_output_file.write(f"Maximum notes deposited in {bank_details_may[0].bank_name}: {bank_details_may[0].denomination_cnt} for May month...\n")

            max_heap_build(bank_details_june, key_func)
            bank_output_file.write(f"Maximum notes deposited in {bank_details_june[0].bank_name}: {bank_details_june[0].denomination_cnt} for June month...\n")
            bank_output_file.write("\n")

            # Q4 calculate the total amount that collected so far for both months
            total_currency_notes = 0
            for b in bank_details_may:
                total_currency_notes += b.denomination_cnt
            for b in bank_details_june:
                total_currency_notes += b.denomination_cnt
            bank_output_file.write(f"Total amount that collected so far in all the banks: 'Rs {2000 * total_currency_notes}'")

            # Q5 remove two bank details from the list which shows max Rs 2000 note denominations for the may month.
            bank_output_file.write("\n")
            max_heap_pop(bank_details_may, key_func)
            max_heap_pop(bank_details_may, key_func)

            # Q6 print the max heap tree for both months
            write_bank_details(bank_output_file, bank_details_may, "may")
            bank_output_file.write("\n")
            write_bank_details(bank_output_file, bank_details_june, "june")
            sys.exit(0)
            
    except FileNotFoundError as  f_err:
        print(f"Make sure if file named {f_err.filename} exists in the current working directory and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
