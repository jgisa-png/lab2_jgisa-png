import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")
    
    # TODO: a) Check if all scores are percentage based (0-100)
    for assignment in data:
        score = assignment['score']
        if score < 0 or score > 100:
            print("Note invalid for", assignment['assignment'])
            return

    # TODO: b) Validate total weights (Total=100, Summative=40, Formative=60)
    total_weight = 0
    summative_weight = 0
    formative_weight = 0

    for assignment in data:
        total_weight += assignment["weight"]
        if assignment["group"] == "Summative":
            summative_weight += assignment["weight"]
        elif assignment["group"] == "Formative":
            formative_weight += assignment["weight"]
   

    weights_are_valid = True
    if total_weight != 100:
        print("Error: Total weight must equal 100")
        weights_are_valid = False
    if summative_weight != 40:
        print("Error: Summative weight must equal 40")
        weights_are_valid = False
    if formative_weight != 60:
        print("Error: Formative weight must equal 60")
        weights_are_valid = False
    if not weights_are_valid:
        return

    # TODO: c) Calculate the Final Grade and GPA
    weighted_total = 0
    for assignment in data:
        weighted_total += assignment["score"] * assignment["weight"]
    final_grade = weighted_total / 100
    print("final Grade:",final_grade)
    gpa = (final_grade / 100) * 5.0
    print("gpa:",gpa)

    # TODO: d) Determine Pass/Fail status (>= 50% in BOTH categories)
    formative_score = 0
    summative_score = 0
    for assignment in data:
        if assignment["group"] == "Formative":
            formative_score += assignment["score"] * assignment["weight"]
        elif assignment["group"] == "Summative":
            summative_score += assignment["score"] * assignment["weight"]

    formative_percent = formative_score / formative_weight
    summative_percent = summative_score / summative_weight
   
    status = "PASSED" if formative_percent >= 50 and summative_percent >= 50 else "FAILED"

    # TODO: e) Check for failed formative assignments (< 50%)
    #          and determine which one(s) have the highest weight for resubmission.
    failed_formative = [
        assignment for assignment in data
        if assignment["group"] == "Formative" and assignment["score"] < 50
    ]
    resubmission = []
    if failed_formative:
        highest_weight = max(assignment["weight"] for assignment in failed_formative)
        resubmission = [
            assignment for assignment in failed_formative
            if assignment["weight"] == highest_weight
        ]

    # TODO: f) Print the final decision (PASSED / FAILED) and resubmission options
    print("Final Status:", status)
    if not resubmission:
        print("No resubmission needed")
    else:
        print("Assignment(s) to resubmit:")
        for assignment in resubmission:
            print(assignment["assignment"])

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
