import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

new_contacts_list = []
contacts_dict = {}

def format_phone(line):
    pattern = re.compile(r'(\+7|8)\s?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})')
    subst_pattern = r"+7(\2)\3-\4-\5"
    formatted_phone = pattern.sub(subst_pattern, line)
    return formatted_phone

def format_phone_additional(line):
    pattern = re.compile(r'\s?\(?[доб.\s]+(\d{4})\)?')
    subst_pattern = r" доб.\1"
    formatted_phone = pattern.sub(subst_pattern, line)
    return formatted_phone

def name_combiner(line = list):
    first_item_words = line[0].split()
    second_item_words = line[1].split()
    third_item_words = line[2].split()
    combined_names = first_item_words + second_item_words + third_item_words
    if len(combined_names) == 2:
        combined_names.append('')
    return combined_names
    

for row in contacts_list[1:]:
    name = name_combiner(row[:3])
    while len(row) < 7:
        row.append("")
    while len(row) > 7:
        row.pop()


    last_name, first_name, surname = name
    # print(last_name, first_name, surname)
    organization = row[3]
    position = row[4]
    phone = row[5]
    email = row[6]


    phone = format_phone(phone)
    phone = format_phone_additional(phone)

    key = (last_name, first_name)
    if key not in contacts_dict:
        contacts_dict[key] = [last_name, first_name, surname, organization, position, phone, email]
    else:
        existing_entry = contacts_dict[key]
        if organization:
            existing_entry[3] = organization
        if position:
            existing_entry[4] = position
        if not existing_entry[5] and phone:
            existing_entry[5] = phone
        if email:
            existing_entry[6] = email

new_contacts_list = [list(entry) for entry in contacts_dict.values()]

header = ["lastname", "firstname", "surname", "organization", "position", "phone", "email"]
new_contacts_list.insert(0, header)

with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_contacts_list)
