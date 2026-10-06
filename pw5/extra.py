import polars as po
import os

def export_to_csv(system):
    """
    Export students, courses, and marks to CSV files.
    """
    print("\n[Exporting to CSV...]")
    
    # Export Students
    with open("students.csv", "w") as f:
        f.write("id,name,dob\n")  # Header
        for s in system.students:
            f.write(f"{s.id},{s.name},{s.dob}\n")
            
    # Export Courses
    with open("courses.csv", "w") as f:
        f.write("id,name,credits\n") # Header
        for c_id, c in system.courses.items():
            f.write(f"{c_id},{c.name},{c.credits}\n")
            
    # Export Marks
    with open("marks.csv", "w") as f:
        f.write("course_id,student_id,mark\n") # Header
        for s in system.students:
            for c_id, mark in s.marks.items():
                f.write(f"{c_id},{s.id},{mark}\n")
                
    print("Export completed: students.csv, courses.csv, marks.csv")

def load_with_polars():
    """
    Load CSV files into Polars DataFrames
    """
    print("\n[Loading CSV files into Polars DataFrames...]")
    try:
        df_students = po.read_csv("students.csv")
        df_courses = po.read_csv("courses.csv")
        df_marks = po.read_csv("marks.csv")
        print("Load successful! Here are the dataframes:")
        print("\n--- Students ---")
        print(df_students)
        print("\n--- Courses ---")
        print(df_courses)
        print("\n--- Marks ---")
        print(df_marks)
        return df_students, df_courses, df_marks
    except FileNotFoundError:
        print("CSV files not found. Please export data first.")
        return None, None, None

def query_dataframe(df_students):
    """
    Add one extra 'query' function that allows users to enter conditions
    """
    if df_students is None:
        return
        
    print("\n[Query Function]")
    print("Example conditions: name = 'Mr. Volunteers' or id = '123'")
    
    while True:
        condition = input("Enter a condition (or 'exit' to quit): ").strip()
        if condition.lower() == 'exit':
            break
            
        try:
            # Parse the condition. Basic format expected: column_name = 'value'
            # Note: This is a simple parser. Polars filtering syntax is different,
            # so we translate the simple string into a Polars filter.
            if "=" in condition:
                # Split by "=" and strip spaces and quotes
                parts = condition.split("=", 1)
                col_name = parts[0].strip()
                val = parts[1].strip().strip("'").strip('"')
                
                # Check if column exists
                if col_name not in df_students.columns:
                    print(f"Error: Column '{col_name}' does not exist.")
                    continue
                    
                # Run the query on Po's dataframe
                # po.col(col_name) selects the column, == val does the comparison
                result = df_students.filter(po.col(col_name) == val)
                
                if result.height == 0:
                    print("No records found matching the condition.")
                else:
                    print("\nQuery Result:")
                    print(result)
            else:
                print("Invalid condition format. Please use: column = 'value'")
                
        except Exception as e:
            print(f"Query error: {e}")

# Đoạn code mô phỏng (Mock) để chạy test độc lập
if __name__ == "__main__":
    from domains.models import Student, Course, SchoolManagement
    
    # Tạo dữ liệu giả để test
    sys = SchoolManagement()
    s1 = Student("S01", "Mr. Volunteers", "01/01/2000")
    s2 = Student("S02", "Alice", "02/02/2001")
    s1.marks = {"C01": 15.5}
    s2.marks = {"C01": 18.0}
    sys.students.extend([s1, s2])
    sys.courses["C01"] = Course("C01", "Python", 3)
    
    # Chạy 3 yêu cầu Extra
    export_to_csv(sys)
    df_s, df_c, df_m = load_with_polars()
    query_dataframe(df_s)
