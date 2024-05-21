import pandas as pd
from urllib.request import urlopen
import datetime


class SchoolAssessmentAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame()
        self.merged_file = pd.DataFrame()

    def process_file(self, file_path):
        # Open and read the content of the file based on its extension
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            self.data = pd.read_excel(file_path)
        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                # Assuming the text file has a specific format that can be read as a DataFrame
                self.data = pd.read_csv(file, delimiter='\t')

    def transfer_data(self, source_file, destination_file):
        # Transfer and merge data based on file extensions
        try:
            if source_file.endswith('.csv') and destination_file.endswith('.csv'):
                frames = [pd.read_csv(source_file), pd.read_csv(destination_file)]
            elif source_file.endswith('.xlsx') and destination_file.endswith('.xlsx'):
                frames = [pd.read_excel(source_file), pd.read_excel(destination_file)]
            else:
                raise ValueError("Unsupported file format combination")
            
            self.merged_file = pd.concat(frames, ignore_index=True)
            return self.merged_file
        except Exception as e:
            return f'An error occurred: {str(e)}'

    def fetch_web_data(self, url):
        # Fetch data from a webpage using urlopen
        try:
            with urlopen(url) as response:
                self.web_content = response.read()
                # Process web content as needed (e.g., parsing HTML)
        except Exception as e:
            return f'An error occurred while fetching web data: {str(e)}'

    def analyze_content(self, filename):
        # Analyze assessment data to identify best and worst courses and semesters
        self.process_file(filename)

        # Calculate average scores for each course
        course_columns = ['INF 652', 'CSC 241', 'ITM 101', 'ITM 371', 'COSC 201']
        self.avg_scores = {course: self.data[course].mean() for course in course_columns}

        # Identify courses with highest and lowest average scores
        self.highest_avg_course = max(self.avg_scores, key=self.avg_scores.get)
        self.lowest_avg_course = min(self.avg_scores, key=self.avg_scores.get)

        # Calculate average scores for each semester
        self.data['Total_score'] = self.data[course_columns].sum(axis=1)
        self.avg_scores_by_semester = self.data.groupby('Semester')['Total_score'].mean().to_dict()

        # Identify the best and worst semesters
        self.best_semester = max(self.avg_scores_by_semester, key=self.avg_scores_by_semester.get)
        self.worst_semester = min(self.avg_scores_by_semester, key=self.avg_scores_by_semester.get)

        # Identify top 5 students overall
        self.top_students = self.data.nlargest(5, 'Total_score')
        self.top_students_dict = self.top_students[['Name', 'Total_score']].to_dict(orient='records')

        # Determine the best course for each of the top 5 students
        self.top_students_courses = []
        for i, student in self.top_students.iterrows():
            best_course = student[course_columns].idxmax()
            self.top_students_courses.append((student['Name'], best_course))

        # Generate recommendations based on the analysis
        self.rec1 = f'Consider reviewing the curriculum for {self.lowest_avg_course}, as it has the lowest average score.'
        self.rec2 = f'Look into the factors contributing to the success in {self.highest_avg_course}, which has the highest average score.'
        self.rec3 = f'Investigate potential issues in the {self.worst_semester} semester, which has the lowest overall performance.'
        self.rec4 = f'Analyze what contributes to the success in the {self.best_semester} semester, which has the highest overall performance.'
        self.rec5 = 'Students struggling in their courses are encouraged to seek help from the top students in their best courses.'


    def generate_summary(self):
        # Generate summary report for the school principal
        print("School Assessment Summary Report\n")
        print(f"1. Course Performance Analysis:")
        print(f"    - Highest Average Score: {self.highest_avg_course} ({self.avg_scores[self.highest_avg_course]:.2f})")
        print(f"    - Lowest Average Score: {self.lowest_avg_course} ({self.avg_scores[self.lowest_avg_course]:.2f})")
        print(f"\n2. Semester Performance Analysis:")
        print(f"    - Best Semester: {self.best_semester} (Average Score: {self.avg_scores_by_semester[self.best_semester]:.2f})")
        print(f"    - Worst Semester: {self.worst_semester} (Average Score: {self.avg_scores_by_semester[self.worst_semester]:.2f})")
        print(f"\n3. Top 5 Students:")
        for student, course in self.top_students_courses:
            print(f"    - {student}: Best Course: {course}")
        print(f"\n4. Recommendations:")
        print(f"    - {self.rec1}")
        print(f"    - {self.rec2}")
        print(f"    - {self.rec3}")
        print(f"    - {self.rec4}")
        print(f"    - {self.rec5}")
        print(f"\nReport Generated on: {datetime.date.today()}")


# Example usage
analyzer = SchoolAssessmentAnalyzer()
merged_file = analyzer.transfer_data('Spring (1).csv', 'fall.csv')
analyzer.analyze_content('all_semester.csv')
analyzer.generate_summary()