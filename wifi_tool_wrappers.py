import subprocess
import enum


class wifiModes(enum.Enum):
    managed = "managed"
    monitor = "monitor"


class iwlistWrapper(object):
    """
    iwlist is mainly used for gathering data rather than setting anything....
    """

    @staticmethod
    def get_channels(interface_name):
        """
        returns the list of available channels, be careful with this method, it behaves differently in differnt modes
        :param interface_name: the name of the wifi interface for the system use
        :return: the list of available channels
        """
        raw_output = subprocess.getoutput("iwlist " +interface_name + " frequency")
        dirty_output_array = raw_output.split("\n")
        # total_channels_line = dirty_output_array[0]
        # # interface_name_last_letter_index = total_channels_line.index(interface_name) + len(interface_name)
        # # channel_index = total_channels_line.index("channels")
        # # # total_channels = int(total_channels_line[interface_name_last_letter_index:channel_index])
        # # # current_channel = None
        # # # try:
        # # #     current_channel_index = raw_output.index("(Channel ") + len("(Channel ")
        # # #     dirty_current_channel = raw_output[current_channel_index:].replace(")","")
        # # #     current_channel = int(dirty_current_channel)
        # # #     # it means that we can see the current channel of the interface
        # # # except ValueError:
        # # #     # it means that there is no current channel information right now.
        # # #     current_channel = None

        channels = []
        for i in range(1, len(dirty_output_array)):
            line = dirty_output_array[i]
            if "(" not in line and line != "": # ( means that we have a current channel line, and "" means that it is the
                #end of line so we should not try to parse it to an int
                channel_end_index = line.index("Channel") + len("Channel")
                semi_colon_index = line.index(":")
                channel = int(line[channel_end_index:semi_colon_index])
                channels.append(channel)

        return channels

    @staticmethod
    def get_current_channel(interface_name):
        """
        This function returns the current channel of the interface
        :param interface_name: the interface name that will be used in iwlist
        :return: the current channel number as int
        """
        try:
            raw_output = subprocess.getoutput("iwlist "+interface_name + " frequency")
            current_channel_index = raw_output.index("(Channel ") + len("(Channel ")
            dirty_current_channel = raw_output[current_channel_index:].replace(")", "")
            current_channel = int(dirty_current_channel)
            return current_channel

        except ValueError:
            return None

    @staticmethod
    def scan_for_networks(interface):
        """
        This method will utilize iwlist interface scan
        :param interface:
        :return:
        """
        pass


class iwWrapper(object):
    """
    iw Wrapper is for wrapping iw commands, iw manipulates wireless devices and their configurations
    """

    @staticmethod
    def set_channel(interface, channel):
        """
        Changes the channel of the interface
        :param interface: the system name of the interface
        :param channel: the channel that we want to set the interface to
        :return: success or not
        """
        # should we also check whether the channel set was succesful??

        result = subprocess.getoutput("iw dev " + interface + " set channel " + str(channel))
        if result == '':
            return True
        else: # if they change the output of the iw dev command this fucks up...
            return False

class ipWrapper(object):
    """
    This is a basic wrapper for ip which can manipulate routing, devices, policy routing and tunnels
    """
    @staticmethod
    def link_down(interface):
        result = subprocess.getoutput("ip link set " + interface + " down")
        return result

    @staticmethod
    def link_up(interface):
        result = subprocess.getoutput("ip link set " + interface + " up")
        return result

class iwconfigWrapper(object):
    """
    This class is for wrapping iwconfig tool
    """

    @staticmethod
    def set_mode(interface,mode):
        """
        This method changes the mode of the interface
        :param mode: the mode of the interaface as string, this can be managed or monitor
        :param interface: the system name of the interface, you can find the system name by typing ifconfig
        :return: returns the result of the subprocess command which should be empty...
        """
        result = subprocess.getoutput("iwconfig " + interface + " mode " + mode)
        return result

    @staticmethod
    def get_wifi_interfaces():
        result = subprocess.getoutput("iwconfig")
        resultarray = result.split("\n")
        interfaces = {}
        current_data = []
        current_interface = ""
        for line in resultarray:
            #print(line)
            if "no wireless extensions" in line:
                #print("nothing")
                pass
            elif line == "":
                #print("bop")
                if len(current_data) > 0 and current_interface != "":
                    #print("Data logged ", current_interface)
                    interfaces[current_interface] = current_data
                    current_interface = ""
                    current_data = []
            elif "IEEE 802.11" in line:
                if len(current_data) > 0 and current_interface != "":
                    #print("Data logged ", current_interface)
                    interfaces[current_interface] = current_data
                    current_interface = ""
                    current_data = []

                # means that we foun a wireless interface
                current_interface = line[:line.index(" ")]
                current_data.append(line)
                #print("NAME ", current_interface)
            else:
                #print("array |", line, "|end")
                current_data.append(line)
        return list(interfaces.keys())




#print(iwconfigWrapper.get_wifi_interfaces())

