import csv


class ExamData:
    def __init__(self, exam_name):
        self.exam_name = exam_name
        self.candidates = []
        self.number_of_passed_exams = 0
        self.number_of_failed_exams = 0
        self.best_score = 0
        self.worst_score = 100

    def get_number_of_cadidates(self):
        return len(set(self.candidates))


class ExamResultReader:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}

    def prepare_data(self):
        with open(self.filename, newline='') as csvfile:
            fieldnames = ['Exam Name', 'Candidate ID', 'Score', 'Grade']
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            row_count = 0
            for row in reader:
                row_count += 1
                if row_count == 1:
                    continue
                exam_data = self.get_exam_data(row['Exam Name'])
                exam_data.candidates.append(row['Candidate ID'])
                if row['Grade'] == 'Pass':
                    exam_data.number_of_passed_exams += 1
                else:
                    exam_data.number_of_failed_exams += 1
                exam_data.best_score = max(
                    exam_data.best_score,
                    int(row['Score'])
                )
                exam_data.worst_score = min(
                    exam_data.worst_score,
                    int(row['Score'])
                )
        return self.data

    def get_exam_data(self, exam_name):
        if exam_name not in self.data:
            exam_data = ExamData(exam_name)
            self.data[exam_name] = exam_data
        return self.data[exam_name]


class ExamReport:
    def __init__(self, data):
        self.data = data

    def generate(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = [
                'Exam Name',
                'Number of Candidates',
                'Number of Passed Exams',
                'Number of Failed Exams',
                'Best Score',
                'Worst Score'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key, exam_data in self.data.items():
                number_of_cadidates = exam_data.get_number_of_cadidates()
                writer.writerow({
                    'Exam Name': exam_data.exam_name,
                    'Number of Candidates': number_of_cadidates,
                    'Number of Passed Exams': exam_data.number_of_passed_exams,
                    'Number of Failed Exams': exam_data.number_of_failed_exams,
                    'Best Score': exam_data.best_score,
                    'Worst Score': exam_data.worst_score
                })


exam_result_reader = ExamResultReader('resources/exam_results.csv')
data = exam_result_reader.prepare_data()
exam_report = ExamReport(data)
exam_report.generate('exam_report.csv')
