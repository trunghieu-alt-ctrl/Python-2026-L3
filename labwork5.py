import pandas as pd

print("--- Data Manipulation ---")
df_students = pd.read_csv('students.csv')

print("\nFirst five rows:")
print(df_students.head())

print(f"\nRows: {df_students.shape[0]}, Columns: {df_students.shape[1]}")

print("\nName and GPA:")
print(df_students[['name', 'GPA']].head())

print("\nStudents with GPA >= 3.5:")
print(df_students[df_students['GPA'] >= 3.5].head())

print("\nSorted by GPA (Descending):")
print(df_students.sort_values(by='GPA', ascending=False).head())

print("\nAverage GPA by major:")
print(df_students.groupby('major')['GPA'].mean())

print("\n--- From Raw Data To Useful Info ---")
df_scores = pd.read_csv('scores.csv')

print("\nMissing values in students.csv:")
print(df_students.isnull().sum())
print("\nMissing values in scores.csv:")
print(df_scores.isnull().sum())

df_students['age'] = df_students['age'].fillna(df_students['age'].mean())
df_students['GPA'] = df_students['GPA'].fillna(df_students['GPA'].mean())
df_scores['math'] = df_scores['math'].fillna(df_scores['math'].mean())
df_scores['database'] = df_scores['database'].fillna(df_scores['database'].mean())

df_merged = pd.merge(df_students, df_scores, on='student_id')
df_merged['average_score'] = df_merged[['python', 'math', 'database']].mean(axis=1)

print("\nTop 5 students by average score:")
top_5 = df_merged.sort_values(by='average_score', ascending=False).head(5)
print(top_5[['student_id', 'name', 'major', 'average_score']])

print("\nAverage score by major:")
print(df_merged.groupby('major')['average_score'].mean())
