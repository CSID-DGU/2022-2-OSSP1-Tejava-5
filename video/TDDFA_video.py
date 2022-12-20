# coding: utf-8
from video import *

__author__ = 'cleardusk'

import pyximport
pyximport.install()


from .._3DDFA_V2.FaceBoxes import FaceBoxes
from .._3DDFA_V2.TDDFA import TDDFA
from .._3DDFA_V2.utils.render import render
# from utils.render_ctypes import render
from .._3DDFA_V2.utils.functions import cv_draw_landmark, get_suffix


def mask_convert(fname):
    cfg = yaml.load(open('configs/mb1_120x120.yml'), Loader=yaml.SafeLoader)

    # Init FaceBoxes and TDDFA, recommend using onnx flag
   # if args.onnx:
    import os
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    os.environ['OMP_NUM_THREADS'] = '4'

    from .._3DDFA_V2.FaceBoxes.FaceBoxes_ONNX import FaceBoxes_ONNX
    from .._3DDFA_V2.TDDFA_ONNX import TDDFA_ONNX

    face_boxes = FaceBoxes_ONNX()
    tddfa = TDDFA_ONNX(**cfg)

    # Given a video path
    fn = fname.split('/')[-1]
    reader = imageio.get_reader(fname)

    fps = reader.get_meta_data()['fps']

    suffix = get_suffix(fname)
    video_wfp = f'./masked.mp4'
    writer = imageio.get_writer(video_wfp, fps=fps)

    # run
    dense_flag = '3d' #in ('3d',)
    pre_ver = None
    for i, frame in tqdm(enumerate(reader)):
        frame_bgr = frame[..., ::-1]  # RGB->BGR

        if i == 0:
            # the first frame, detect face, here we only use the first face, you can change depending on your need
            boxes = face_boxes(frame_bgr)
            boxes = [boxes[0]]
            param_lst, roi_box_lst = tddfa(frame_bgr, boxes)
            ver = tddfa.recon_vers(param_lst, roi_box_lst, dense_flag=dense_flag)[0]

            # refine
            param_lst, roi_box_lst = tddfa(frame_bgr, [ver], crop_policy='landmark')
            ver = tddfa.recon_vers(param_lst, roi_box_lst, dense_flag=dense_flag)[0]
        else:
            param_lst, roi_box_lst = tddfa(frame_bgr, [pre_ver], crop_policy='landmark')

            roi_box = roi_box_lst[0]
            # todo: add confidence threshold to judge the tracking is failed
            if abs(roi_box[2] - roi_box[0]) * abs(roi_box[3] - roi_box[1]) < 2020:
                boxes = face_boxes(frame_bgr)
                boxes = [boxes[0]]
                param_lst, roi_box_lst = tddfa(frame_bgr, boxes)

            ver = tddfa.recon_vers(param_lst, roi_box_lst, dense_flag=dense_flag)[0]

        pre_ver = ver  # for tracking

        res = render(frame_bgr, [ver], tddfa.tri)
        writer.append_data(res[..., ::-1])  # BGR->RGB

    writer.close()
#    print(f'Dump to {video_wfp}')

