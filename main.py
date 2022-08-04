import csv
import json
import os
from datetime import datetime


def copy_new_reports(path_to_new_aida_reports):
    """
    Update list of aida reports
    :return: parse()
    """
    aida_reports = f'{os.getcwd()}\\aida_reports\\'
    not_yet_reports = [i for i in os.scandir(path_to_new_aida_reports) if i not in os.scandir(aida_reports)]
    for entry in not_yet_reports:
        os.popen(f'copy {path_to_new_aida_reports}{entry.name} {aida_reports}{entry.name}')
    return parse(aida_reports)


def parse(path_aida_reports):
    computers = {}
    with os.scandir(path_aida_reports) as it:
        for entry in it:
            with open(path_aida_reports + entry.name, 'r') as aida_report:
                report = csv.DictReader(aida_report)
                for line in report:
                    if line['Item'] == 'Компьютер':
                        pc_name = line['Value']
                    elif line['Item'] == 'Генератор':
                        user = line['Value']

                computers[pc_name] = {
                    'Имя компьютера': pc_name,
                    'Имя пользователя': user
                }
    with open('computers.json', 'w') as parsed_json:
        json.dump(computers, parsed_json, indent='   ')
    return 'Parse - OK'


path_to_new_aida_reports = input()
print(copy_new_reports(path_to_new_aida_reports))
