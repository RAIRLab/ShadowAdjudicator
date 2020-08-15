# This file sets up AirSim for the Uber accident case study and communicates
# with ShadowAdjudicator in order to make a decision

# This file is based on code from "hello_car.py" in the AirSim GitHub repository

import airsim
import time
import sys

from os.path  import exists, normpath
from os       import remove, makedirs
from filelock import SoftFileLock


CAPTURE_STILLS = False # Toggle capture of image stills
IMAGE_STYLE    = "fpv" # Camera options: front_center, front_right, front_left, fpv, back_center


# Get input parameter
if(len(sys.argv) < 2 or not (sys.argv[1] == "1" or sys.argv[1] == "2")):
  print("Usage: python3 uber_AirSim.py <Number of Reasoning Agents -- 1 or 2>")
  exit(1)

if (sys.argv[1] == "1"): out_text = "Single agent"
else:                    out_text = "Both agents"


# Create folder for still capture
if CAPTURE_STILLS:
  t = time.localtime()
  time_stamp = str(t.tm_year) + "-" + \
               str(t.tm_mon)  + "-" + \
               str(t.tm_mday) + "_" + \
               str(t.tm_hour) + "-" + \
               str(t.tm_min)  + "-" + \
               str(t.tm_sec)  + "/"
  img_dir = "stills/" + time_stamp
  if not exists(img_dir):
    makedirs(img_dir)


# Acquire lock for input file
out_file   = "reasoner_input.txt"
lock_file1 = out_file + ".lock"
lock1      = SoftFileLock(lock_file1)

with lock1:
  # Connect to the AirSim simulator 
  client = airsim.CarClient()
  client.confirmConnection()
  client.reset() # Ensure vehicles start still
  client.enableApiControl(True, "Car1")
  client.enableApiControl(True, "Car2")
  car_controls1 = airsim.CarControls()
  car_controls2 = airsim.CarControls()

  print("Moving actors into their initial positions...")
  client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(-200,0,0), airsim.to_quaternion(0,0,18.9)), True, "Car1")
  client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0,-22,0), airsim.to_quaternion(0,0,14)), True, "Car2")

  # Capture image at start of simulation
  if CAPTURE_STILLS:
    image    = client.simGetImage(IMAGE_STYLE, airsim.ImageType.Scene)
    filename = img_dir + "start.png"
    airsim.write_file(normpath(filename), image)

  # Get vehicles moving
  car_controls1.throttle = 1
  car_controls1.steering = 0
  car_controls2.throttle = 0.37
  car_controls2.steering = 0
  client.setCarControls(car_controls1, "Car1")
  client.setCarControls(car_controls2, "Car2")
  print("Beginning Simulation of Accident")

  # Send request for reasoning to ShadowAdjudicator
  open(out_file, "w").write(out_text)


in_file    = "reasoner_output.txt"
lock_file2 = in_file + ".lock"
lock2      = SoftFileLock(lock_file2)

print("Waiting for a response from ShadowAdjudicator...")
with lock2:
  print("Response received")
  decision = open(in_file, "r").read()

if decision == "(NeedToBrake c)":
  print("Applying brakes...")
  car_controls1.throttle = 0
  car_controls1.brake    = 1
  client.setCarControls(car_controls1, "Car1")

# See if a collision occurs in the next 15 seconds
for i in range(150):
  collision_info = client.simGetCollisionInfo("Car1")

  if collision_info.has_collided:
    print("A collision occurred!")

    # Capture image of collision
    if CAPTURE_STILLS:
      image    = client.simGetImage(IMAGE_STYLE, airsim.ImageType.Scene)
      filename = img_dir + "collision.png"
      airsim.write_file(normpath(filename), image)

    break

  car_state1 = client.getCarState("Car1")
  car_state2 = client.getCarState("Car2")
  y1         = car_state1.kinematics_estimated.position.y_val
  y2         = car_state2.kinematics_estimated.position.y_val

  if y2 > y1 + 5.5:
    print("Collision avoided!")

    # Capture image after avoiding collision
    if CAPTURE_STILLS:
      image    = client.simGetImage(IMAGE_STYLE, airsim.ImageType.Scene)
      filename = img_dir + "avoided.png"
      airsim.write_file(normpath(filename), image)

    break

  time.sleep(0.1)

# Gently stop vehicles
car_controls1.throttle = 0
car_controls2.throttle = 0
client.setCarControls(car_controls1, "Car1")
client.setCarControls(car_controls2, "Car2")

client.enableApiControl(False, "Car1")
client.enableApiControl(False, "Car2")

# Clean up communication files
if(exists(in_file)):  remove(in_file)
if(exists(out_file)): remove(out_file)

