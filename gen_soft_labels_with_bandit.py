import argparse
import subprocess
import os
import regex as re


'''
Requirements for run_bandit.sh:
 > pip install bandit
'''
parser = argparse.ArgumentParser(description='Obtain soft labels using Bandit.')
parser.add_argument('-f', '--code-file', required=True, type=str, help='The path to the Python code file')
args = parser.parse_args()

code_file = args.code_file

if not os.path.isfile(code_file):
    print("ERROR: Please provide a valid file")
    exit(1)
if not code_file.endswith('.py'):
    print("ERROR: Please provide a Python file (with extension .py)")
    exit(1)

# Run Bandit on the Python file
subprocess.call(['sh', './run_bandit.sh', code_file])

bandit_result_file = "bandit_" + os.path.basename(code_file) + ".txt"

issue_pattern = re.compile(">> Issue: \[.+:(.*)\] (.*)")
value_pattern = re.compile("\s*Severity: (\w+)\s+Confidence: (\w+)")
locat_pattern = re.compile("\s*Location: (.*\.py):(\d+):(-*[\d]+)")

# Read Bandit output file to obtain all issues
issue_list = []  # Stores the issues, confidence, line number and code
issue_num = -1   # For indexing list
line_num = 0     # For creating dynamic regex
with open(bandit_result_file, 'r') as f:
    lines = f.readlines()
    for line in lines:
        m_issue = issue_pattern.match(line.strip())
        m_value = value_pattern.match(line.strip())
        m_locat = locat_pattern.match(line.strip())

        if m_issue is not None:
            # This is a line stating an issue
            issue_name = m_issue.group(1)
            issue_desc = m_issue.group(2)

            issue_num += 1
            issue_list.append([issue_name])
        elif m_value is not None:
            # This is a line stating the severity and confidence of the previous line's issue
            severity = m_value.group(1)
            confidence = m_value.group(2)

            issue_list[issue_num].append(confidence)
        elif m_locat is not None:
            # This is a line stating the location of the most recent issue
            issue_line = m_locat.group(2)
            issue_col = m_locat.group(3)

            line_num = issue_line
            issue_list[issue_num].append(issue_line)
        else:
            # This could be the line with the code we care about
            # Create dynamic regex to check
            code_str = str(line_num) + "\s+(.*)"
            code_pattern = re.compile(code_str)
            m_code = code_pattern.match(line.strip())
            if m_code is not None:
                issue_code = m_code.group(1)

                issue_list[issue_num].append(issue_code)

# Filter out only issues with Medium or High confidence
relevant_issues = [[line_number, name] for name, confidence, line_number, code in issue_list
                   if confidence == "Medium" or confidence == "High"]

# Write to output file
base_filename = os.path.basename(code_file)[:-3]
bandit_soft_labels_file = "bandit_soft_labels_" + base_filename + ".txt"
with open(bandit_soft_labels_file, 'w') as outfile:
    for line_number, issue_name in relevant_issues:
        outfile.write(line_number + "\t" + issue_name + "\n")

print("Relevant issues and their line numbers have been added to", bandit_soft_labels_file)
