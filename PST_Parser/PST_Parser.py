from argparse import ArgumentParser
import csv
import pypff
import re

#https://github.com/libyal/documentation/blob/master/PFF%20Forensics%20-%20analyzing%20the%20horrible%20reference%20file%20format.pdf
#Redemtion library?
#Password protected files
#https://github.com/libyal/documentation/blob/master/PFF%20forensics%20-%20e-mail%20and%20appoinment%20falsification%20analysis.pdf
#https://github.com/libyal/libpff/blob/master/pypff/pypff_file.c

def process_folders(pff_folder):
    folder_name = pff_folder.name if pff_folder.name else "N/A"
    print("Folder: {} (sub-dir: {}/sub-msg: {})".format(folder_name,
          pff_folder.number_of_sub_folders,
          pff_folder.number_of_sub_messages))

    # Process messages within a folder
    data_list = []
    for msg in pff_folder.sub_messages:
        for i in msg.sub_items:
            print(i)
        data_dict = process_message(msg)
        data_dict['folder'] = folder_name
        data_list.append(data_dict)

    # Process folders within a folder
    for folder in pff_folder.sub_folders:
        data_list += process_folders(folder)

    return data_list


def process_message(msg):
    # Attachments
    attachments = []
    total_attachment_size_bytes = 0
    if msg.number_of_attachments > 0:
        for i in range(msg.number_of_attachments):
            total_attachment_size_bytes = total_attachment_size_bytes + (msg.get_attachment_by_index(i)).size()
#               # get the content of the attachment file
            attachments.append(
                ((msg.attachment(i)).read_buffer((msg.attachment(i)).size())).decode('ascii',
                                                                                                         errors="ignore"))
    return {
        "subject": msg.subject,
        "sender": msg.sender_name,
        "header": msg.transport_headers,
        "body": msg.plain_text_body,
#       "creation_time": msg.creation_time,
#       "submit_time": msg.client_submit_time,
#        "delivery_time": msg.delivery_time,
        "attachment_count": msg.number_of_attachments,
        "total_attachment_size": total_attachment_size_bytes,
        "attachments": attachments
    }


    # Extract attributes
    attribs = ['conversation_topic', 'number_of_attachments',
               'sender_name', 'subject', 'plain_text_body',
               #'transport_headers'
               #'attachment','total_attachment_size_bytes','attachments'
               ]
    data_dict = {}
    for attrib in attribs:
        data_dict[attrib] = getattr(msg, attrib, "N/A")

    if msg.transport_headers is not None:
        data_dict.update(process_headers(msg.transport_headers))

    return data_dict


def process_headers(header):
    # Read and process header information
    key_pattern = re.compile("^([A-Za-z\-]+:)(.*)$")
    header_data = {}
    for line in header.split("\r\n"):
        if len(line) == 0:
            continue

        reg_result = key_pattern.match(line)
        if reg_result:
            key = reg_result.group(1).strip(":").strip()
            value = reg_result.group(2).strip()
        else:
            value = line

        if key.lower() in header_data:
            if isinstance(header_data[key.lower()], list):
                header_data[key.lower()].append(value)
            else:
                header_data[key.lower()] = [header_data[key.lower()],
                                            value]
        else:
            header_data[key.lower()] = value
    return header_data


def write_data(outfile, data_list):
    # Build out additional columns
    print("Writing Report: ", outfile)
    columns = ['folder', 'conversation_topic', 'number_of_attachments',
               'sender_name', 'subject', 'plain_text_body'
               # 'transport_headers'
               ]
    formatted_data_list = []
    for entry in data_list:
        tmp_entry = {}

        for k, v in entry.items():
            if k not in columns:
                columns.append(k)

            if isinstance(v, list):
                tmp_entry[k] = ", ".join(v)
            else:
                tmp_entry[k] = v
        formatted_data_list.append(tmp_entry)

    # Write CSV report
    with open(outfile, 'a', newline='', encoding='utf-8-sig') as openfile:
        csvfile = csv.DictWriter(openfile, columns)
        csvfile.writeheader()
        csvfile.writerows(formatted_data_list)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("pff")
    parser.add_argument("outputcsv")
    args = parser.parse_args()

    #Open OST/PST
    pff_obj = pypff.file()
    pff_obj.open(args.pff)

    #Parser
    parsed_data = process_folders(pff_obj.root_folder)
    pff_obj.close()

    # Write CSV report
    write_data(args.outputcsv, parsed_data)
