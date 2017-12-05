from wifiInterface import wifi_device_sniffer_Interface
from wifi_tool_wrappers import iwconfigWrapper, iwWrapper, ipWrapper, iwlistWrapper


available_wifi_interfaces = iwconfigWrapper.get_wifi_interfaces()

print("Select wifi interface to use")
print("===============================")
i = 1
for wifi_interface_name in available_wifi_interfaces:
    print(str(i) + ") " + wifi_interface_name)
    i +=1

user_selection = int(input()) - 1

selected_interface = wifi_device_sniffer_Interface("Sniff1", available_wifi_interfaces[user_selection])
selected_interface.start_wifi_monitor_mode()
selected_interface.start_searching()

while 1:
    print(selected_interface.found_devices.get())



