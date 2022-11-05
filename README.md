# Assignment on making the Crazyflie drone swing back and forth
Repository for a control assignment in the WASP Autonomous Systems course

## Your task
Your task is to write code that makes the drone follow the reference signal as closely as possible. The reference signal is a square wave with period 10s. That is, 5s at 20degs, 5s at -20degs, 5s at 20degs, and so on. 

<br/>[![Watch the video](https://img.youtube.com/vi/ZTXV2UIzZWA/0.jpg)](https://www.youtube.com/watch?v=ZTXV2UIzZWA). 
<p>
In the video above you see an example of what it might look like when the drone osscilated between +/-20 degrees. In this example the code is written in C as part of the firmware of the drone and ran 1kHz. While this allows you to use the provided UI seen in the video it does make the overall assignment much harder given the limited time we have here. Therefore, in this assignment, we will instead make use of the python client library for the communicating with the drone from an external computer.
</p>

<p>
Please follow he instructions below to install the needed code. You will be given a skeleton to start from. You do not need to worry about changing the yaw reference value, it will be done for you in the skeleton.
</p>


## Installation
We will offer two options to run the code. The first one is to install things direcly on your machine and the second is to use a <i>virtual machine</i>. The latter example will not allow you to get as good result as you will be communicating from the virtual machine to the host machine (your laptop) and then to the drone. This means that communication will be slow.

In the examples below we will put all new code in the directory <i>wasp_as_cf</i> to make it easy to clean up after the assignment.

#### Installing directly on your machine
The aim is here to install [cflib: Crazyflie python library](https://github.com/bitcraze/crazyflie-lib-python) which requires Python 3.7+. In the instructions below replace python/pip with python3/pip3 if the system complains.

First we create a directory where we keep all files so that you can clean later.
<pre>
mkdir wasp_as_cf
cd wasp_as_cf
</pre>
To avoid a system wide installation of all the dependencies we run the code in a self-contained python environment. This way it will not influence your python installation. For this we will use [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html). 
<pre>
virtualenv -p python3 cfenv
source cfenv/bin/activate
</pre>
If you use Windows the latter command is replaced with
<pre>
cfenv/bin/activate.bit
</pre>

You should now see that you are in this environment by looking at the prompt in the terminal. It might look like
<pre>
(cfenv) patric@PJMacPro wasp_as_cf_yawswing % 
</pre>
That is, the prompt is pre-fixed with the name of the virtual environment.

If you close the terminal where you ran this you need to re-run the activate command. To get out of the virtual environment you can also run the command <i>deactivate</i>.

Create a directry where you keep the crazyflie python library code
<pre>
cd wasp_as_cf
git clone https://github.com/bitcraze/crazyflie-lib-python.git
cd crazyflie-lib-python.git
pip3 install -e .
</pre>

If you do not have git installed you can also download the source code as a zip file. You go to the [github page for Crazyflie python library](https://github.com/bitcraze/crazyflie-lib-python) and click the green button Code in the upper right corner and select "Download ZIP".

##### USB under Linux
With linux, the crazyradio is easily recognized, but you have to setup UDEV-permissions. Look at the usb [permission instructions](https://github.com/bitcraze/crazyflie-lib-python/blob/master/docs/installation/usb_permissions.md) to setup udev on linux.

##### Crazyradio antenna Windows
If you use Windows you need to [install the driver](https://www.bitcraze.io/documentation/repository/crazyradio-firmware/master/building/usbwindows/) for the Crazyradio USB antenna.

#### Virtual machine
An alternative to installing the source directly on your machine is to use a Virtualbox virtual machine.
* Download and install VirtualBox (https://www.virtualbox.org).
* You find the virtual machine image built by BitCraze here (https://github.com/bitcraze/bitcraze-vm/releases/)
* You find instruction from Bitcraze here (https://github.com/bitcraze/bitcraze-vm). Note that
  * The Crazyradio USB antenna must be seen by the virtual machine which you ensure by selecting it under Devices/USB in the top menu.
  * The password is crazyflie (login name bitcraze).
* You do not need to install anything inside the virtual machine, it is all set up for you.

##### Tweaking the VM
* Is your virtual machine freezing when you resize the window? For me it was solved by increasing the Graphics memory to 128MB in Settings (power down VM first).
* Life is usually a lot easier in your VM if you install the guest additions. This allows you, for example, to make the clipboard operate across both host and virtual machine so that you can copy things from a window on one and past it in another.
* To install guest additions do the following in a terminal
<pre>
sudo apt update
sudo apt install virtualbox-guest-additions-iso
</pre>

## Geting the skeleton code
Go to the directory we created for the code and download the skeleton
<pre>
cd wasp_as_cf
git clone https://github.com/pjensfelt/wasp_as_cf_yawswing.git
cd wasp_as_cf_yawswing
</pre>

## Before starting
* Be nice to the drone. They are used in a course and should be handed back in the same shape as you got them.
* How to use the motors to make the drone rotate arond its vertical axis? This is probably the first thing you want to think about or perform experiments to figure out.
* The thrust (upward force) on the drone is the sum of forces from the motors. Tthe drone should stay on the surface, which means that you might want to think about the max signals you can send to the motors without the drone taking off and then ensure that your signals stay below that.
* Note that your task is to make the estimated yaw angle track the reference yaw angle. Since the estimate might drift the actual angle of the drone might not move between +/-20degs which is fine. What matters is making the estimated yaw track the references.

## Running the code
* First you need to make sure that the radio module is connected to your machine and detected. If you use the virtual machine make sure that you have selected the CrazyRadio PA in the menu Devices/USB inside the virtual machine.
* Connect the battery on the drone. Keep the USB-cable plugged in whenever you are not testing something as this will charge the battery. You can run the drone with the cable connected also but it will be difficult to rotate.
* Turn on the drone by pressing in (GENTLY!!!) the small black push button in-between two of the arms 
<br/>[![Watch the video](https://img.youtube.com/vi/E5t2qfsGqQY/default.jpg)](https://www.youtube.com/watch?v=E5t2qfsGqQY&t=2s). 
* Make sure that the drone is standing on a flat surface when you do this as the drone's IMU calibrates upon boot.
* Opening the code cf_yawswing.py and edit the URI (line 14) matches the channel of your drone
* Run the code with <pre> 
python3 cf_yawswing.py
</pre>
You should see that it connects to your drone and it should start printing information in the terminal
<pre>
(cfenv) patric@PJMacPro wasp_as_cf_yawswing % python3 cf_yawswing.py
Wating for a connection
Connecting to radio://0/83/2M
WARNING:cflib.crazyflie.log:Error no LogEntry to handle id=1
WARNING:cflib.crazyflie.log:Error no LogEntry to handle id=2
Connected to radio://0/83/2M
Disabling controller
Waiting for position estimate to be good enough...
Ready! Press e to enable motors, h for help and Q to quit
yaw: (curr=0.44396063685417175, ref=60, err=59.55603936314583),   battery:3.64V
     control: (False, 10000, 10000, 10000, 10000)
</pre>
If you rotate the drone you should see how the current angle change ("curr" above). You can also see how the reference angle changes between +45 and -45. The row that starts with control contains the contains a flag for Enable/Disable the motors followed by the PWM values that controls the speed of the four motors. The latter values can be set between 0 (not moving) and 65535 (max speed).

### Sanity check
To ensure that you have a responsive system do a test where you disable (press 'd') and enable (press 'e') the motors. They should stop/start spinning directly when you press. If they do not you have a problem. If you use the virtual machine this is almost guaranteed to happen and then you need to lower the frequency of the loop (increas ethe period).
<pre>
    # Control period. [ms]
    # WARNING: Reducing this might clogg the communication
    # We are controlling the motor PWMs which is not meant
    # to be done from offboard
    period_in_ms = 100
</pre>

## Your coding task
You are expected to change the code (lines 207-210) that now sets the PWM signal to 10,000 for all four motors, i.e.
<pre>
        # YOUR CODE STARTS HERE
        # In the code below set the variables m1, m2, m3, m4 appropriately
        # They should each take on values in [0,65535] which is taken care of
        # by the function limit_int below

        m1 = 10000
        m2 = 10000
        m3 = 10000
        m4 = 10000

        # YOUR CODE ENDS HERE
</pre>

## Suggested setup
Below you see the suggested setup
<br/><img src="IMG_8479.png" width=512 title="Suggested setup">
* The USB cable is connected to the drone to charge the battery onboard whenever you are not performing an experiment that requires the drone to be free.
* The CrazyRadio USB antenna is connected
* An extra battery is being charged

## Video demonstration
In the video below we show first how to install and set up the virtual machine, install the skeleton code, change the channel and run the code. If you are not using the virtual machine skip directly ahead to 4:45.
<br/>[![Watch the video](https://img.youtube.com/vi/IACCsOqROpI/0.jpg)](https://www.youtube.com/watch?v=IACCsOqROpI). 
<br/>Below you find the time stamps for different events in the file
* 0:00 Install the virtual machine file from bitcraze
* 0:40 Setting up and starting the VM
* 2:00 Connecting the USB antenna
* 2:35 Install guest additions (see above)
* 4:08 Active bidirectional clipboard (not shared desktop as I say in the video)
* 4:25 Copy/paste in Linux
* 4:45 Installing the skeleton code
* 5:15 Running the code <== <b>DONT DO THIS!!! FIRST CHANGE THE CHANNEL AS BELOW!!!</b>
* 5:55 Change the channel for the drone in the code
* 6:40 Connecting to the drone and running the code
* 6:55 What we see on the screen and where to change in the code

## Q&A
* Q: How do I plot the result? 
* A: The python file is setup to output a csv file with SPACE separator. You can open the file is for example excel or MATLAB. In MATLAB you could do
<pre>
d=load('log_20221101_141838.csv');
plot(d(:,1),d(:,2),d(:,1),d(:,3)), grid, xlabel('Time [s]'), ylabel('Yaw angle [deg]'), legend('Current yaw','Reference yaw')
</pre>
* Q: The propellors are not moving despite me enabling the motors and setting a PWM value. What is wrong?
* A: Reset the drone by pressing the black push button.
* Q: The system tells me that numpy is not install, BUT I JUST RAN IT AND IT WORKED?!?!?!?!
<pre>
patric@vpn37-186 wasp_as_cf_yawswing % python3 cf_yawswing.py
Traceback (most recent call last):
  File "/Users/patric/Dropbox/Documents/code/wasp_as_cf_yawswing/cf_yawswing_P.py", line 9, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
</pre>
* A: Did you install your system in a virtual environment and did you change terminal and forgot to active the virtual environment?
<pre>
cd wasp_as_cf
source cfenv/bin/activate
</pre>
* Q: No connecttion to the drone?
* A: Did you set the correct URI? If you use a Virtual Machine, did you remember to hand over the CrazyRadio PA to the Virtual Machine (see instructions above).
* Q: No permission to access the crazyradio USB antenna on your linux machine? 
* A: Check that you have set the udev-permissions (see section above on USB under Linux)
* Q: The virtual machine does not allow me to paste things I copied from the host, why?
* A1: You need to active bidirection clipboard and this requires installing the guest additions. Did you do that?
* A2: If you try to paste by ctrl-v it will not work, in Liunx it is shift-ctrl-v (and shift-ctrl-c to copy from a terminal).
