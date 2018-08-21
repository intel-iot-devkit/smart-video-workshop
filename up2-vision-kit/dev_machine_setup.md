
***Ubuntu Laptop Internet Connection Setup:- sharing wired connection with
an UP2 board.***

To enable remote access to the UP2 XWindows GUI the following steps need
to be completed.

1: Connect Laptop WiFi to an available WiFi network.

2: Select the unused Wired Connection and enable internet sharing.

3: Plug in Ethernet Cable directly from Laptop to UP2 Board.

4: Determine the IP address given to the UP2 board, using "**arp -a**"
command.

5: Open an SSH connection to the UP2 board, user "**upsquared**", password
"**upsquared**"

6: Run a command to start a VNC server on the UP2 board, "**sudo x11vnc
--auth guess**".

Sudo password is also "**upsquared**".

7: Start a VNC viewer on the laptop and connect to port 5900, using the
IP address determined in step 4 above.

Illustrated Instructions

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

**Enabling Remote Access using SSH and VNC**

From the laptop, open up an SSH terminal, using **upsquared@10.42.0.xx**
as the parameters. NOTE, your detected IP will likely be different. The
password for the upsquared and root account is "**upsquared**"

Once logged in, start the x11vnc server using the following command
"**sudo x11vnc -auth guess**".

If the x11vnc application is not installed, install it using the
following command "**sudo apt-get update && sudo apt install x11vnc** "

**Laptop VNC Viewer.**

If necessary install a VNC viewer application on the laptop using the
following command in a terminal,

"**sudo apt-get update && sudo apt install vncviewer**". The sudo password
is "**intel123**".

On the laptop start the vncviewer from a terminal using the following
command "**vncviewer 10.42.0.xxx:5900**" and if required login to the UP2
upsquared account using the upsquared password.

NOTE: the default setting for the VNC server running on the UP2 is to
shutdown when the viewer is closed.
