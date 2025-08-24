import sys


INPUT_FILE_NAME = "inputPS02.txt"
OUTPUT_FILE_NAME = "outputPS02.txt"

def quick_sort(student_data, ascending=True):
    if len(student_data) <= 1:
        return student_data

    pivot = student_data[len(student_data) // 2][0]
    left = []
    right = []
    equal = []

    for student in student_data:
        if student[0] == pivot:
            equal.append(student)
        elif (student[0] < pivot and ascending) or (student[0] > pivot and not ascending):
            left.append(student)
        else:
            right.append(student)
    
    equal = [student for student in student_data if student[0] == pivot]

    return quick_sort(left, ascending) + equal + quick_sort(right, ascending)

try:
    # Read student data from input file, skipping the header line and invalid lines
    with open(INPUT_FILE_NAME, 'r') as input_file:
        lines = input_file.readlines()
        student_data = [line.strip().split(',') for line in lines[1:] if line.strip() and len(line.strip().split(',')) == 2]

    # Check if the input file is empty
    if not student_data:
        print("Input file is empty. Nothing will be written to the output file.")
    else:
        # Check if the number of students is exactly 20
        if len(student_data) != 20:
            print(f"Groups will be uneven as you have {len(student_data)} students.")
            sys.exit()

        # Clean up and format the student data
        student_data = [(student[0].strip().zfill(4), student[1].strip()) for student in student_data]

        # Sort the students using Quick Sort in ascending order
        sorted_students = quick_sort(student_data, ascending=True)

        # Initialize groups
        group1 = []
        group2 = []

        # Place students in respective groups based on ID prefix
        for student_id, student_name in sorted_students:
            if student_id[0] in ('0', '1', '2', '3', '4'):
                group1.append((student_id, student_name))
            elif student_id[0] in ('5', '6', '7', '8', '9'):
                group2.append((student_id, student_name))
            else:
                print(f"Invalid student ID: {student_id}")
                sys.exit()  # Exit if an invalid ID is encountered

        # Check if both groups have 10 participants
        if len(group1) != 10 or len(group2) != 10:
            print("Uneven groups. Each group should have 10 participants.")
            sys.exit()

        # Write group details to output file
        with open(OUTPUT_FILE_NAME, 'w') as output_file:
            # Write Group G1
            output_file.write('Group G1: (In ascending order)\nStudent ID,name\n')
            for i, (student_id, student_name) in enumerate(group1, 1):
                output_file.write(f"{i}. {student_id}, {student_name}\n")

            # Write Group G2 in descending order
            output_file.write('\nGroup G2: (In descending order)\nStudent ID,name\n')
            group2_descending = quick_sort(group2, ascending=False)
            for i, (student_id, student_name) in enumerate(group2_descending, 1):
                output_file.write(f"{i}. {student_id}, {student_name}\n")

        # Write details of students at 3rd and 7th locations
        with open(OUTPUT_FILE_NAME, 'a') as output_file:
            output_file.write('\nStudent Details, Placed in clue location\n')
            
            # Details for Group G1
            output_file.write('Group G1:\n')
            for i, (student_id, student_name) in enumerate(group1, 1):
                if i == 3:
                    output_file.write(f"{student_id}, {student_name}, {i}rd clue location\n")
                if i == 7:
                    output_file.write(f"{student_id}, {student_name}, {i}th\n")
            # Details for Group G2
            output_file.write('\nGroup G2:\n')
            for i, (student_id, student_name) in enumerate(group2_descending, 1):
                if i == 3:
                    output_file.write(f"{student_id}, {student_name}, {i}rd\n")
                if i == 7:
                    output_file.write(f"{student_id}, {student_name}, {i}th\n")

except FileNotFoundError:
    print("Input file not found.")
except Exception as e:
    print(f"An error occurred: {e}")
