#!/usr/bin/env python3

# This script prunes the external storage drive for old surveillence camera files

import shutil;
from os import listdir;
from os.path import join;
from os.path import exists;
from sys import exit;

# debugging constants
debuglevel = 2

# paths
external_drive = "/media/external/"
cameras = ["Camera1","Camera2"]

# disk usage hysteresis
du_high = 0.90
du_low  = 0.80

# Determine drive fullness
stat = shutil.disk_usage(external_drive);
disk_usage = stat.used / stat.total;

# terminate the program if disk usage is below the limit
if (disk_usage < du_high):
    if (debuglevel > 0):
        print("Disk usage at %.2f within limit of %.2f." % (disk_usage, du_high), end=' ');
        print("No pruning required.");
    exit(0);


while (disk_usage > du_low):

    print ("Disk usage at %.2f, " % disk_usage , end = '');
    camera_dir = join(external_drive, cameras[0]);
    if (not exists(camera_dir)):
        print ("camera directory \"" + camera_dir + "\" does not exist!");
        exit(1);

    yearlist = listdir(camera_dir);
    yearlist.sort();
    if (not yearlist):
        print ("no years within camera directory \"" + camera_dir + "\"!");
        exit(1);
    yearpath = join(camera_dir, yearlist[0]);
    datepath = yearlist[0];

    monthlist = listdir(yearpath);
    monthlist.sort();
    if (not monthlist):
        # remove the year directory
        for camera in cameras:
            if (debuglevel > 1):
                print ("removing year directory \"" + join(external_drive, camera, yearpath) + "\".");
            shutil.rmtree(join(external_drive, camera, yearpath), ignore_errors=True);
        continue;
    monthpath = join(yearpath, monthlist[0]);
    datepath = join(datepath, monthlist[0]);

    daylist = listdir(monthpath);
    daylist.sort();
    if (not daylist):
        # remove the month directory
        for camera in cameras:
            if (debuglevel > 1):
                print ("removing month directory \"" + join(external_drive, camera, monthpath) + "\".");
            shutil.rmtree(join(external_drive, camera, monthpath), ignore_errors=True);
        continue;
    daypath = join(monthpath, daylist[0]);
    datepath = join(datepath, daylist[0]);

    # remove the day directory
    for camera in cameras:
        if (debuglevel > 1):
            print ("removing day directory \"" + join(external_drive, camera, datepath) + "\".");
        shutil.rmtree(join(external_drive, camera, datepath), ignore_errors=True);

    # update disk usage
    stat = shutil.disk_usage(external_drive);
    disk_usage = stat.used / stat.total;

if (debuglevel > 0):
    print("Finished with disk usage at %.2f within limit of %.2f." % (disk_usage, du_low));
exit(0);
