# Create GDSN RFCIN messages

Program to create GDSN Request For CIN (RFCIN) messages for a data recipient based on a list of supplier GLNS.

**Background**

The RFCIN message is used by a data recipient and is a request to resend the CIN-messages for the published items (one gtin or all items).

More information about the Global Data Synchronisation Network (GDSN): https://www.gs1.org/services/gdsn

**Usage**
1. Create a csv file in the input directory with the structure:

> gln_ds,gtin,tm (for one gtin per row)
> or gln,tm (for all published gtins of a supplier)

> gln_ds = GLN Data source
> gtin = Global Trade Item Number
> tm = target_market

2. Change (if needed) the data_pool_gln in the source code

3. Change the sender_gln in the source code

4. Change (if needed) the setting if there are GTINS in the inputfile (gtins_included)

3. Run the program from the command prompt with the name of the csv-file as parameter

> create_rfcin.py test_file

4. In the directory output a new directory will be created with the same name as the csv file.
   In the created directory there a one or more batches with RFCIN messages. The batchsize can be changed in the source code.
   
5. Upload the xml files via FTP or AS2 to your GDSN data pool.

6. Messages will be processed by the datapool.

7. If a publication exits data will be received.
