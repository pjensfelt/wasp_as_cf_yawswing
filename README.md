# wasp_as_cf_yawswing
Repository for a control assignment in the WASP Autonomous Systems course

## Installation
We will offer two options to run the code. The first one is to use Linux or MacOS and the second is to use a virtual machine provided by the company Bitcrazy that sells the Crazyflie that we will be using. 

In the examples below we will put all new code in the directory wasp_as_cf to make it as easy as possible to clean up after the assignment.

### MacOS and Linux
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

### Virtual machine


## Geting the skeleton code
Go to the directory we created for the code and download the skeleton
<pre>
cd wasp_as_cf
git clone git:https://github.com/pjensfelt/wasp_as_cf_yawswing.git
cd wasp_as_cf_yawswing
</pre>
