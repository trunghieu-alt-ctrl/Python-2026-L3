import numpy as np

marks = np.array([15.5, 18.0, 12.5, 19.0])
credits = np.array([3, 4, 2, 3])

print("Marks:", marks)
print("Credits:", credits)

gpa = np.average(marks, weights=credits)
print(f"Weighted Average GPA: {gpa:.2f}")
