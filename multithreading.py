import argparse
import os
import cv2
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from VideoShow import VideoShow

def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

def threadBoth(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", "-s", default=0,
                    help="Path to video file or integer representing webcam index"
                         + " (default 0).")
    ap.add_argument("--thread", "-t", default="none",
                    help="Threading mode: get (video read in its own thread),"
                         + " show (video show in its own thread), both"
                         + " (video read and video show in their own threads),"
                         + " none (default--no multithreading)")
    args = vars(ap.parse_args())

    if (
        isinstance(args["source"], str)
        and args["source"].isdigit()
        and not os.path.isfile(args["source"])
    ):
        args["source"] = int(args["source"])

    threadBoth(0)


if __name__ == "__main__":
    main()
