import os
import sys
import csv
import fnmatch

CSV_HEADER = ["Project", "File", "Spotbug", "PMD", "Infer", "Spotbug Mutated", 
        "PMD Mutated", "Infer Mutated", "Spotbug Killed", "PMD Killed", "Infer Killed", 
        "Spotbug % (Project)", "PMD % (Project)", "Infer % (Project)"]

SUMMARY_HEADER = ["Project", "Spotbug % Killed", "PMD % Killed", "Infer % Killed"]

def percentage(part, whole):
  return 100 * float(part)/float(whole)

def main():
    args = sys.argv
    pathPos = args.index("--path")
    path = args[pathPos + 1]
    
    destPos = args.index("--dest")
    dest = args[destPos + 1]


    summary_data = []
    summary_data.append(SUMMARY_HEADER)


    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.csv'):
            summary_rows = []
            summary_rows.append(filename)
            csv_rows = []
            csv_rows.append(CSV_HEADER)
            spotbug_killed = 0
            pmd_killed = 0
            infer_killed = 0
            
            with open(os.path.join(root, filename), 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    csv_data = []
                    # Update metrics
                    if row[6] > row[3]:
                        spotbug_killed += 1
                    if row[7] > row[4]:
                        pmd_killed += 1
                    if row[8] > row[5]:
                        infer_killed += 1
                    line_count += 1

                    # Fill CSV data
                    csv_data.append(row[0]) # Project
                    csv_data.append(row[1]) # File
                    csv_data.append(row[3]) # Spotbug
                    csv_data.append(row[4]) # PMD
                    csv_data.append(row[5]) # Infer
                    csv_data.append(row[6]) # Spotbug Mutated
                    csv_data.append(row[7]) # PMD Mutated
                    csv_data.append(row[8]) # Infer Mutated
                    csv_data.append(row[6] > row[3]) # Spotbug Killed
                    csv_data.append(row[7] > row[4]) # PMD Killed
                    csv_data.append(row[8] > row[5]) # Infer Killed
                    csv_data.append("")
                    csv_data.append("")
                    csv_data.append("")
                    csv_rows.append(csv_data)

            # Update general metrics
            csv_rows[1][-3] = percentage(spotbug_killed, line_count)
            csv_rows[1][-2] = percentage(pmd_killed, line_count)
            csv_rows[1][-1] = percentage(infer_killed, line_count)
            summary_rows.append(percentage(spotbug_killed, line_count))
            summary_rows.append(percentage(pmd_killed, line_count))
            summary_rows.append(percentage(infer_killed, line_count))
            summary_data.append(summary_rows)
            with open(os.path.join(dest, filename), "w") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerows(csv_rows)
    with open(os.path.join(dest, "summary.csv"), "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(summary_data)

if __name__ == "__main__":
    main()
