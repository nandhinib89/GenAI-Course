def studentgrade():
    try:
        score = float(input("Enter the student's score (0-100): "))
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100.")
        
        if score >= 90:
            grade = 'A'
        elif score >= 80:
            grade = 'B'
        elif score >= 70:
            grade = 'C'
        elif score >= 60:
            grade = 'D'
        else:
            grade = 'E'
        
        print("The student's score is:", score)
        print(f"The student's grade is: {grade}")
    except ValueError as e:
        print(f"Invalid input: {e}")

studentgrade()