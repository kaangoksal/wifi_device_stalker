

import csv

class mac_database:

    def __init__(self):
        self.database = self.create_database_from_csv()

    def create_database_from_csv(self):
        with open('oui.csv') as f:
            reader = csv.reader(f)
            lines_list = list(reader)

        mac_dict = {}
        for line in lines_list:
            mac_addr_header = line[1]
            #print("mac header " +str(line[1]))
            company_name = line[2]
            #print("compname " + str(line[2]))
            mac_dict[mac_addr_header] = company_name

        return mac_dict

    def poll_mac_address(self, mac):
        dots_removed = mac.replace(":", "")
        query_part = dots_removed[:6].upper()

        return_item = self.database[query_part]

        if return_item is not None:
            return return_item
        else:
            return "Unknown " + query_part


#n = mac_database()
#print(n.poll_mac_address("0c:68:03:ae:6f:b0"))
