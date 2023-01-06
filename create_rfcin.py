"""
The RFCIN message is used by a data recipient and is a request to resend the published items (one gtin or all items).
Author: Sjoerd Schaper - GS1 Nederland
"""

import csv
import pprint
import json
import sys
import datetime
import time
import os
import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


if len(sys.argv) > 1:
    source_file = sys.argv[1]
else:
    source_file = "test_file"

# Change this to the GLN of your data pool
data_pool_gln = '8712345013042'

# Change this to the GLN of the data recipient (is sender of the xml file)
sender_gln = '8712345013103'

# Indicate if the input file contains gln,gtin,tm (True) or gln,tm (False)
gtin_included = False

if gtin_included:
    headers = ['gln_ds','gtin','tm']
    if source_file == "test_file":
        source_file = "test_file_gtin"
else:
    headers = ['gln_ds', 'tm']

infile = os.path.join('input', source_file + '.csv')

# To prevent overloading the data pool the messages are split up in batches  
batch_size = 100

batch = os.path.join('output',source_file,'batch_001')
if not os.path.exists(batch):
    os.makedirs(batch)

cntr = 1
b_nr = 1

# ISReload is a GSDN option
is_reload = 'false'


with open(infile, 'r', encoding='utf-8', errors='ignore') as fp:

    reader = csv.DictReader(fp, fieldnames=headers, skipinitialspace=True)
    for row in reader:
        if row.get('gln_ds') != 'gln_ds':
            time_sys = time.strftime("%Y-%m-%dT%H:%M:%S")
            file_id = get_random_string(8)
            if cntr % batch_size == 0:
                b_nr = b_nr + 1
                batch = os.path.join('output',source_file, 'batch_' + str(b_nr).zfill(3))
                if not os.path.exists(batch):
                    os.makedirs(batch)
            file_name = os.path.join(batch,f"RFCIN_" + sender_gln + "_" + source_file + "_" + row.get('gln_ds') + "_"  + row.get('tm') + "_" + file_id + ".xml")
            inst_id = get_random_string(8)
            outfile = open(str(file_name), "w", encoding='utf-8')
            outfile.write('<?xml version="1.0" encoding="utf-8"?>\n')
            outfile.write('<request_for_catalogue_item_notification:requestForCatalogueItemNotificationMessage xmlns:sh="http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:gs1:gdsn:request_for_catalogue_item_notification:xsd:3 http://www.gdsregistry.org/3.1/schemas/gs1/gdsn/RequestForCatalogueItemNotification.xsd" xmlns:request_for_catalogue_item_notification="urn:gs1:gdsn:request_for_catalogue_item_notification:xsd:3">\n')
            outfile.write('<sh:StandardBusinessDocumentHeader>\n')
            outfile.write('<sh:HeaderVersion>1.0</sh:HeaderVersion>\n')
            outfile.write('<sh:Sender>\n')
            outfile.write(f'<sh:Identifier Authority="GS1">{sender_gln}</sh:Identifier>\n')
            outfile.write('</sh:Sender>\n')
            outfile.write('<sh:Receiver>\n')
            outfile.write(f'<sh:Identifier Authority="GS1">{data_pool_gln}</sh:Identifier>\n')
            outfile.write('</sh:Receiver>\n')
            outfile.write('<sh:DocumentIdentification>\n')
            outfile.write('<sh:Standard>GS1</sh:Standard>\n')
            outfile.write('<sh:TypeVersion>3.1</sh:TypeVersion>\n')
            outfile.write(f'<sh:InstanceIdentifier>RFCIN_{sender_gln}_{inst_id}</sh:InstanceIdentifier>\n')
            outfile.write('<sh:Type>requestForCatalogueItemNotification</sh:Type>\n')
            outfile.write(f'<sh:CreationDateAndTime>{time_sys}</sh:CreationDateAndTime>\n')
            outfile.write('</sh:DocumentIdentification>\n')
            outfile.write('</sh:StandardBusinessDocumentHeader>\n')

            # transactiom
            trans_id = get_random_string(8)
            outfile.write('<transaction>\n')
            outfile.write('<transactionIdentification>\n')
            outfile.write(f'<entityIdentification>RFCIN_ADD_{sender_gln}_{trans_id}</entityIdentification>\n')
            outfile.write('<contentOwner>\n')
            outfile.write(f'<gln>{sender_gln}</gln>\n')
            outfile.write('</contentOwner>\n')
            outfile.write('</transactionIdentification>\n')

            # document
            doc_id = get_random_string(8)
            outfile.write('<documentCommand>\n')
            outfile.write('<documentCommandHeader type="ADD">\n')
            outfile.write('<documentCommandIdentification>\n')
            outfile.write(f'<entityIdentification>RFCIN_ADD_{sender_gln}_{doc_id}</entityIdentification>\n')
            outfile.write('<contentOwner>\n')
            outfile.write(f'<gln>{sender_gln}</gln>\n')
            outfile.write('</contentOwner>\n')
            outfile.write('</documentCommandIdentification>\n')
            outfile.write('</documentCommandHeader>\n')
            outfile.write('<request_for_catalogue_item_notification:requestForCatalogueItemNotification>\n')
            outfile.write(f'<creationDateTime>{time_sys}</creationDateTime>\n')
            outfile.write('<documentStatusCode>ADDITIONAL_TRANSMISSION</documentStatusCode>\n')
            outfile.write('<catalogueItemSubscriptionIdentification>\n')
            outfile.write(f'<entityIdentification>Item_{row.get("gln")}_{row.get("tm")}_{doc_id}</entityIdentification>\n')
            outfile.write('<contentOwner>\n')
            outfile.write(f'<gln>{sender_gln}</gln>\n')
            outfile.write('</contentOwner>\n')
            outfile.write('</catalogueItemSubscriptionIdentification>\n')
            outfile.write(f'<dataRecipient>{sender_gln}</dataRecipient>\n')
            outfile.write(f'<dataSource>{row.get("gln")}</dataSource>\n')
            if gtin_included:
                outfile.write(f'<gtin>{row.get("gtin")}</gtin>\n')    
            outfile.write(f'<recipientDataPool>{data_pool_gln}</recipientDataPool>\n')
            outfile.write('<targetMarket>\n')
            outfile.write(f'<targetMarketCountryCode>{row.get("tm")}</targetMarketCountryCode>\n')
            outfile.write('</targetMarket>\n')
            outfile.write(f'<isReload>{is_reload}</isReload>\n')
            outfile.write('</request_for_catalogue_item_notification:requestForCatalogueItemNotification>\n')
            outfile.write('</documentCommand>\n')
            outfile.write('</transaction>\n')
            outfile.write('</request_for_catalogue_item_notification:requestForCatalogueItemNotificationMessage>\n')
            outfile.close()