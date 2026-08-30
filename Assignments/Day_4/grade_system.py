import streamlit as st

st.title("Student Grade Calculator")

mark_input = st.text_input("Enter the student's mark (0-100):")

if mark_input:
    try:
        mark = float(mark_input)

        if mark < 0 or mark > 100:
            st.error("Please enter a mark between 0 and 100.")

        elif mark >= 90:
            grade = "A"
            st.success(f"Mark: {mark} | Grade: {grade}")

        elif mark >= 80:
            grade = "B"
            st.success(f"Mark: {mark} | Grade: {grade}")

        elif mark >= 70:
            grade = "C"
            st.success(f"Mark: {mark} | Grade: {grade}")

        elif mark >= 60:
            grade = "D"
            st.success(f"Mark: {mark} | Grade: {grade}")

        else:
            grade = "E"
            st.success(f"Mark: {mark} | Grade: {grade}")

    except ValueError:
        st.error("Please enter a valid number.")
else:
    st.info("Enter a mark to calculate the grade.")