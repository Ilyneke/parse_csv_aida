import csv
import os
from datetime import datetime


def copy_new_reports():
    path_to_new_aida_reports = f'\\\\zeon\\SYSVOL\\sbrce.ru\\report_it\\report2019\\{str(datetime.now().date())}\\'
    aida_reports = f'C:\\Users\\Xarisov\\Desktop\\py\\parse_csv_aida\\aida_reports\\'
    not_yet_reports = [i for i in os.scandir(path_to_new_aida_reports) if i not in os.scandir(aida_reports)]
    for entry in not_yet_reports:
        os.popen(f'copy {path_to_new_aida_reports}{entry.name} {aida_reports}{entry.name}')
    parse(aida_reports)


def parse(path_aida_reports):

    macs = '04-D4-C4-8E-4F-58 0C-38-3E-48-68-B0 90-2B-34-08-62-C5'
    with os.scandir(path_aida_reports) as it:
        for entry in it:
            with open(path_aida_reports + entry.name, 'r') as aida_report:
                report = csv.DictReader(aida_report)
                rows = [i for i in report]
                for i in range(len(rows)):
                    if rows[i]['Item'] == 'Компьютер':
                        name_pc = rows[i]['Value']
                    elif len(rows[i]['Value']) >= 16 and rows[i]['Value'] in macs:
                        print(name_pc, rows[i]['Value'])

    print('OK')


copy_new_reports()
