import csv
import json
import os
from datetime import datetime
import logging

logging.basicConfig(filename='aida_reports_parser.log', level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')


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


def pc_compare(old: dict, new: dict):
    for elem in new.keys():
        if old.get(elem, 0) == 0:
            logging.info(f'Update: {elem} has been added!')
        elif new[elem] != old[elem]:
            logging.warning(f'Some elements in {elem} has been changed!:\nOld: {old[elem]}\nNew: {new[elem]}')


def parse(path_aida_reports):
    computers = {}
    with os.scandir(path_aida_reports) as it:
        for entry in it:
            with open(path_aida_reports + entry.name, 'r') as aida_report:
                report = csv.DictReader(aida_report)
                printers = []
                mem = [[], None]
                programs = []
                for line in report:
                    if line['Item'] == 'Компьютер':
                        pc_name = line['Value']
                        print(pc_name)
                    elif line['Item'] == 'Генератор':
                        user = line['Value']
                    elif 'Процессоры' in line['Device'] and line['Item'] == 'Версия':
                        processor_name = line['Value']
                    elif line['Item'] == 'DMI системная плата':
                        motherboard = line['Value']
                    elif line['Item'] == 'Системная плата':
                        type_system = line['Value']
                    elif line['Item'] == 'Принтер':
                        if line['Value'] not in '''FaxMicrosoft Print to PDFMicrosoft XPS Document Writer
OneNote for Windows 10Отправить в OneNote 16Foxit Reader PDF PrinterGeneric / Text OnlydoPDF v7''':
                            printers.append(line['Value'])
                    elif 'Устройства памяти' in line['Device'] and line['Item'] == 'Тип' and not mem[1]:
                        mem[1] = line['Value']
                    elif 'Устройства памяти' in line['Device'] and line['Item'] == 'Размер':
                        mem[0].append(line['Value'])
                    elif 'Установленные программы' in line['Page']:
                        if 'Версия' in line['Item']:
                            programs.append({'Name': line['Device'],
                                             'Version': line['Value']})
                        elif 'Дата' in line['Item']:
                            programs[-1]['Date'] = line['Value']

                computers[pc_name] = {
                    'PC name': pc_name,
                    'Username': user,
                    'Specs': {
                        'PC': type_system,
                        'CPU': processor_name,
                        'Motherboard': motherboard,
                        'Memory': str(mem[1]) + '+'.join(mem[0])
                    },
                    'Printers': printers,
                    'Programs': programs
                }

    try:
        with open('computers.json', 'r') as parsed_json:
            pc_compare(json.load(parsed_json), computers)
    except:
        pass

    with open('computers.json', 'w') as parsed_json:
        json.dump(computers, parsed_json, indent='   ')
    logging.info('Report "Computers.json" has been updated!')


path_to_new_aida_reports = f''  # put path to newest reports there
print(copy_new_reports(path_to_new_aida_reports))
