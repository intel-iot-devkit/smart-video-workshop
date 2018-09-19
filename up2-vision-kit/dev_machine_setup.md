
***Ubuntu Laptop Internet Connection Setup:- sharing wired connection with
an UP2 board.***

To enable remote access to the UP2 XWindows GUI the following steps need
to be completed.

1: Connect Laptop WiFi to an available WiFi network.

2: Select the unused Wired Connection and enable internet sharing.

3: Plug in Ethernet Cable directly from Laptop to UP2 Board.

4: Determine the IP address given to the UP2 board, using "**arp -a**"
command.



***Illustrated Instructions***

Select the **wifi/Ethernet** icon from the top menu, and choose **Edit
Connections...**

![](../images/edit_connections1.png)

In the **Network Connections** dialog, highlight **Wired Connection 1,**
and click **Edit**

![](../images/wired_connection1.png)

Select the **IPv4 Settings** tab and select the **Method** pulldown and
choose **Shared to other computers,** and click **Save**

![](../images/network_connections.png)

Plug in an Ethernet Cable between the UP2 upper Ethernet port and the
laptop. Open up a terminal and type "**arp -a**" to determine the IP
address of the enpxxxx port. In the screenshot below the wired Ethernet
IP address is 10.42.0.218, the others are wifi addresses and can be
safely ignored.
![](../images/arp1.png)

The 10.42.0.x IP address has been assigned to your Up2 board.




***OpenCL driver upgrade for Up2 board installed with OpenVINO R3.343***
1. SSH to Up2 board with the IP address you just obtained, password: **upsquared**

        ssh upsquared@10.42.0.xxx
    
2. Go to the directory contains the OpenCL driver update script

        cd /opt/intel/computer_vision_sdk/install_dependencies/
        
3. Run the upgrade script

        sudo ./install_NEO_OCL_driver.sh
        
4. Once done, reboot Up2

        sudo reboot
        
    
