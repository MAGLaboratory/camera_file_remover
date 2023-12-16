#!/usr/bin/env python3

# This script prunes the external storage drive for old surveillence camera files
import shutil;
from os import listdir;
from os.path import join;
from os.path import exists;
from sys import exit;

# debugging constants
debuglevel = 0

# maximum removal tries
max_rm_try = 3

# paths
external_drive = "/media/external/cameras"
cameras = [
        "Camera1",
        "Camera2",
        "Camera3",
        "Camera4",
        "Camera5",
        "Camera6",
        "Camera7"
]

# disk usage hysteresis
du_high = 0.90
du_low  = 0.80

# Determine drive fullness
stat = shutil.disk_usage(external_drive);
disk_usage = stat.used / stat.total;

# function definitions
def rm_wrapper(directory):
    try_count = 0
    while (try_count < max_rm_try):
        try_count += 1;
        try: 
            shutil.rmtree(directory);
            break;
        except FileNotFoundError:
            if (debuglevel > 0):
                print("File Not Found When Attempting Removal of \"" 
                        + directory + "\"");
        except BaseException as e:
            print("Other Error Encountered When Attempting Removal of \""
                    + directory + "\"");
            if (try_count >= max_rm_try):
                raise e;
    # end while try_count lt max_rm_try            
    return

# terminate the program if disk usage is below the limit
if (disk_usage < du_high):
    if (debuglevel > 0):
        print("Disk usage at %.2f within limit of %.2f." % (disk_usage, du_high), end=' ');
        print("No pruning required.");
    exit(0);

# iterate through the directory structure
# empty directories are removed when hit
# day directories are removed when they are the smallest date found
while (disk_usage > du_low):
    if (debuglevel > 1):
        print ("Disk usage at %.2f, " % disk_usage);
    camera_dir = join(external_drive, cameras[0]);
    if (not exists(camera_dir)):
        print ("camera directory \"" + camera_dir + "\" does not exist!");
        exit(1);

    # handle years
    yearlist = listdir(camera_dir);
    yearlist.sort();
    if (not yearlist):
        if (debuglevel > 0):          # removing years is a bit rare.
            print ("no years within camera directory \"" + camera_dir + "\"!");
        exit(1);
    yearpath = join(camera_dir, yearlist[0]);
    datepath = yearlist[0];

    # handle months
    monthlist = listdir(yearpath);
    monthlist.sort();
    if (not monthlist):
        # remove the year directory
        for camera in cameras:
            if (debuglevel > 1):
                print ("removing year directory \"" + join(external_drive, camera, yearpath) + "\".");
            rm_wrapper(join(external_drive, camera, yearpath));
        continue;
    monthpath = join(yearpath, monthlist[0]);
    datepath = join(datepath, monthlist[0]);

    # handle days
    daylist = listdir(monthpath);
    daylist.sort();
    if (not daylist):
        # remove the month directory
        for camera in cameras:
            if (debuglevel > 1):
                print ("removing month directory \"" + join(external_drive, camera, monthpath) + "\".");
            rm_wrapper(join(external_drive, camera, monthpath));
        continue;
    daypath = join(monthpath, daylist[0]);
    datepath = join(datepath, daylist[0]);

    # remove the day directory
    for camera in cameras:
        if (debuglevel > 1):
            print ("removing day directory \"" + join(external_drive, camera, datepath) + "\".");
        rm_wrapper(join(external_drive, camera, datepath));

    # update disk usage
    stat = shutil.disk_usage(external_drive);
    disk_usage = stat.used / stat.total;

if (debuglevel > 0):
    print("Finished with disk usage at %.2f within limit of %.2f." % (disk_usage, du_low));
exit(0);
