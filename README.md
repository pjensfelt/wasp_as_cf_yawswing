# Control assignment using a Crazyflie drone
Repository for a control assignment in the WASP Autonomous Systems course

## Your task
Your task is to write code that makes the drone follow the reference signal as closely as possible. The reference signal is a square wave with period 10s. That is, 5s at 60degs, 5s at -60degs, 5s at 45degs, and so on. You do not need to worry about changing the yaw reference value, it will be done for you in the skeleton that you statrt from. 

<p>
Please follow he instructions below to install the needed code. You will be given a skeleton to start from.
</p>

<p>
You should document your project with a video showing the drone moving, a log file and a figure showing the angles.
</p>

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
  * The CrazyRadio must be seen by the virtual machien which you ensure by selecting it under Devices/USB
  * The password is crazyflie (login name bitcraze)
  * If your virtual machien freezes when you resize the window it helped me to increase the Graphics memory to 128MB in Settings (power down VM first)

## Geting the skeleton code
Go to the directory we created for the code and download the skeleton
<pre>
cd wasp_as_cf
git clone git:https://github.com/pjensfelt/wasp_as_cf_yawswing.git
cd wasp_as_cf_yawswing
</pre>

## Running the code
* First you need to make sure that the radio module is connected to your machine and detected.
* Connect the battery on the drone. Keep the USB-cable plugged in whenever you are not testing soemthing as this will charge the battery. You can run the drone with the cable connected also but it will be difficult to rotate.
* Turn on the drone by pressing in (GENTLY!!!) the small black push button in-between two of the arms. Make sure that the drone is standing on a flat surface when you do this as the drone's IMU calibrates upon boot.
* Opening the code cf_yawswing.py and edit the URI (line 14) matches the channel of your drone
* Run the code with <pre> 
python3 cf_yawswing.py
</pre>
You should see that it connects to your drone and it should start printing information in the terminal
<pre>
(cfenv) patric@PJMacPro wasp_as_cf_yawswing % python3 cf_yawswing.py
Wating for a connection
Connecting to radio://0/83/2M
WARNING:cflib.crazyflie.log:Error no LogEntry to handle id=2
WARNING:cflib.crazyflie.log:Error no LogEntry to handle id=1
Connected to radio://0/83/2M
Disabling controller
Waiting for position estimate to be good enough...
Ready! Press e to enable motors, h for help and Q to quit
yaw: (curr=-0.2088501900434494, ref=45, err=45.20885019004345),   battery:3.8V
     control: (False, 10000, 10000, 10000, 10000)
</pre>
If you rotate the drone you should see how the current angle change ("curr" above). You can also see how the reference angle changes between +45 and -45. The row that starts with control contains the contains a flag for Enable/Disable the motors followed by the PWM values that controls the speed of the four motors. The latter values can be set between 0 (not moving) and 65535 (max speed).

<p>
You are expected to change the code that now sets the PWM signal to 10,000 for all four motors, i.e.
<pre>
    def calc_control_signals(self):
        # Calculate the error between the reference yaw signal and the current yaw
        yaw_err = self.angle_difference(self.yaw_ref, self.yaw_curr)

        # YOUR CODE STARTS HERE
        # In the code below set the variables m1, m2, m3, m4 appropriately
        # They should each take on values in [0,65535] which is taken care of
        # by the function limit_int below

        m1 = 10000
        m2 = 10000
        m3 = 10000
        m4 = 10000

        # YOUR CODE ENDS HERE

        # Set the control variables and make sure that they are
        # integers and between 0 and 65535
        self.motor_pwm1 = self.limit_int(m1, 0, 0xFFFF)
        self.motor_pwm2 = self.limit_int(m2, 0, 0xFFFF)
        self.motor_pwm3 = self.limit_int(m3, 0, 0XFFFF)
        self.motor_pwm4 = self.limit_int(m4, 0, 0XFFFF)
</pre>
</p>

## Q&A
* Q: Why is moy drone not rotating between the same angles?
* A: Note that your task is to make the estimated yaw angle track the reference yaw angle. Since the estimate might drift the actual angle of the drone might not move between +/-45degs which is fine. What matters is making the estimated yaw track the references.
* Q: The propellors are not moving despite me enabling the motors and setting a PWM value. What si wrong?
* A: Reset the drone  

