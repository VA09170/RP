#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 20:20:48 2020

@author: vaibhavpatel
"""


#import lib
try:
    import csv
    import glob
    import os.path
    from subprocess import call
    from joblib import Parallel,delayed
except:
    print("error in the lib")

try:
    video_dir = './DATA/videos/TrainValVideo'
    output_dir = './DATA/frames'
    features_out = './DATA/features'
    jobs = 16
    print(os.path.exists(video_dir))

    print(os.path.exists(output_dir))

    print(os.path.exists(features_out))
except:
    print("error in the dir")

data_file = []

def core_func(video_path):
    global data_file
    video_parts = get_video_parts(video_path)
    filename_no_ext, filename = video_parts

    # Only extract if we haven't done it yet. Otherwise, just get
    # the info.
    if not check_already_extracted(video_parts):
        # Now extract it.
        src = os.path.join(video_dir,filename)
        dest = os.path.join(output_dir,filename_no_ext + '-%04d.jpg')
        #print('in', src, dest)
        call(["ffmpeg", "-i", src,"-r", "4", dest])
    # Now get how many frames it is.
    nb_frames = get_nb_frames_for_video(video_parts)
    #print('written: ',nb_frames)
    data_file.append([filename_no_ext, nb_frames])



def get_nb_frames_for_video(video_parts):
    """Given video parts of an (assumed) already extracted video, return
    the number of frames that were extracted."""
    filename_no_ext, _ = video_parts
    generated_files = glob.glob(os.path.join(output_dir, filename_no_ext + '*.jpg'))
    return len(generated_files)

def get_video_parts(video_path):
    """Given a full path to a video, return its parts."""
    parts = video_path.split(os.path.sep)
    # print(parts)
    filename = parts[4]
    filename_no_ext = filename.split('.')[0]
    return filename_no_ext, filename

def check_already_extracted(video_parts):
    """Check to see if we created the -0001 frame of this file."""
    filename_no_ext, _ = video_parts
    return bool(os.path.exists(os.path.join(output_dir,
                               filename_no_ext + '-0001.jpg')))


print("at vfiles")
vfiles = glob.glob(os.path.join(video_dir, '*.mp4'))
print("vfiles:", vfiles)
print("processing parallel")
results = Parallel(n_jobs=jobs)(delayed(core_func)(video_path) for video_path in vfiles)               
print("results", results)
with open('data_file.csv', 'w') as fout:
    writer = csv.writer(fout)
    writer.writerows(data_file)

print("Extracted and wrote %d video files." % (len(data_file)))


from tqdm import tqdm
vfiles = glob.glob(os.path.join(video_dir, '*.mp4'))
pbar = tqdm(total=len(vfiles))

data_file = []
for video_path in vfiles:
    video_parts = get_video_parts(video_path)
    filename_no_ext, filename = video_parts
    generated_files = glob.glob(os.path.join(output_dir, filename_no_ext + '*.jpg'))
    data_file.append([filename_no_ext, len(generated_files)])
    pbar.update(1)
pbar.close()
with open('data_file.csv', 'w') as fout:
    writer = csv.writer(fout)
    writer.writerows(data_file)

print("Extracted and wrote %d video files." % (len(data_file)))



    