# Control assignment using a Crazyflie drone
Repository for a control assignment in the WASP Autonomous Systems course

## Installation
We will offer two options to run the code. The first one is to use Linux or MacOS and the second is to use a virtual machine provided by the company Bitcrazy that sells the Crazyflie drones. 

In the examples below we will put all new code in the directory wasp_as_cf to make it easy to clean up after the assignment.

#### MacOS and Linux
To avoid a system wide installation of all the dependencies we run the code in a virtual environment
<pre>
mkdir wasp_as_cf
cd wasp_as_cf
virtualenv -p python3 cfenv
source cfenv/bin/activate
</pre>
You should now see that you are in this environment by looking at the prompt in the terminal. It might look like
<pre>
(cfenv) patric@PJMacPro wasp_as_cf_yawswing % 
</pre>
That is, the prompt is pre-fixed with the name of the virtual environment.

If you close the terminal where you ran this you need to re-run the activate command. To get out of the virtual environment you run
<pre>
deactivate
</pre>

Create a directry where you keep the crazyflie python library code
<pre>
cd wasp_as_cf
git clone https://github.com/bitcraze/crazyflie-lib-python.git
cd crazyflie-lib-python.git
pip3 install -e .
</pre>

#### Virtual machine
* Download and install VirtualBox (https://www.virtualbox.org/wiki/Download_Old_Builds_6_1). We used 6.1.40 when testing this
* Install also the Extension pack when you installed VirtualBox (https://download.virtualbox.org/virtualbox/6.1.40/Oracle_VM_VirtualBox_Extension_Pack-6.1.40.vbox-extpack)
* You find the virtual machine image built by BitCraze here (https://github.com/bitcraze/bitcraze-vm/releases/)
* You find instruction from BitCraze here (https://github.com/bitcraze/bitcraze-vm). Note that
** The CrazyRadio must be seen by the virtual machien which you ensure by selecting it under Devices/USB
** The password is crazyflie (login name bitcraze)
** If your virtual machien freezes when you resize the window it helped me to increase the Graphics memory to 128MB in Settings (power down VM first)

## Geting the skeleton code
Go to the directory we created for the code and download the skeleton
<pre>
cd wasp_as_cf
git clone git:https://github.com/pjensfelt/wasp_as_cf_yawswing.git
cd wasp_as_cf_yawswing
</pre>
