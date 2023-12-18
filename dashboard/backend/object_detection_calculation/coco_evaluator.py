""" version ported from https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py
    Notes:
        1) The default area thresholds here follows the values defined in COCO, that is,
        small:           area <= 32**2
        medium: 32**2 <= area <= 96**2
        large:  96**2 <= area.
        If area is not specified, all areas are considered.
        2) COCO's ground truths contain an 'area' attribute that is associated with the segmented area if
        segmentation-level information exists. While coco uses this 'area' attribute to distinguish between
        'small', 'medium', and 'large' objects, this implementation simply uses the associated bounding box
        area to filter the ground truths.
        3) COCO uses floating point bounding boxes, thus, the calculation of the box area
        for IoU purposes is the simple open-ended delta (x2 - x1) * (y2 - y1).
        PASCALVOC uses integer-based bounding boxes, and the area includes the outer edge,
        that is, (x2 - x1 + 1) * (y2 - y1 + 1). This implementation assumes the open-ended (former)
        convention for area calculation.
"""

from collections import defaultdict

import numpy as np
from object_detection_calculation.bounding_box import BBFormat


def get_coco_summary(groundtruth_bboxes, detected_bboxes):
    """Calculate the 12 standard metrics used in COCOEval,
        AP, AP50, AP75,
        AR1, AR10, AR100,
        APsmall, APmedium, APlarge,
        ARsmall, ARmedium, ARlarge.
        When no ground-truth can be associated with a particular class (NPOS == 0),
        that class is removed from the average calculation.
        If for a given calculation, no metrics whatsoever are available, returns NaN.
    Parameters
        ----------
            groundtruth_bboxes : list
                A list containing objects of type BoundingBox representing the ground-truth bounding boxes.
            detected_bboxes : list
                A list containing objects of type BoundingBox representing the detected bounding boxes.
    Returns:
            A dictionary with one entry for each metric.
    """

    # separate bbs per image X class
    _bboxes_info = _group_detections(detected_bboxes, groundtruth_bboxes)

    # pairwise ious
    _ious = {key: _compute_ious(**info) for key, info in _bboxes_info.items()}

    def _evaluate(iou_threshold, max_detections, area_range):
        # accumulate evaluations on a per-class basis
        _evaluate_results = defaultdict(lambda: {"scores": [], "matched": [], "NP": []})

        for img_id, class_id in _bboxes_info:
            evaluate_result = _evaluate_image(
                _bboxes_info[img_id, class_id]["detected"],
                _bboxes_info[img_id, class_id]["ground"],
                _ious[img_id, class_id],
                iou_threshold,
                max_detections,
                area_range,
            )
            accuracy = _evaluate_results[class_id]
            accuracy["scores"].append(evaluate_result["scores"])
            accuracy["matched"].append(evaluate_result["matched"])
            accuracy["NP"].append(evaluate_result["NP"])

        # now reduce accumulations
        for class_id in _evaluate_results:
            accuracy = _evaluate_results[class_id]
            accuracy["scores"] = np.concatenate(accuracy["scores"])
            accuracy["matched"] = np.concatenate(accuracy["matched"]).astype(np.bool_)
            accuracy["NP"] = np.sum(accuracy["NP"])

        results = {"detail": []}

        # run ap calculation per-class

        tp_list, fp_list, np_list = [], [], []

        for class_id in _evaluate_results:
            accuracy = _evaluate_results[class_id]

            tmp_res = _compute_ap_recall(
                accuracy["scores"], accuracy["matched"], accuracy["NP"]
            )

            tp_list.append(tmp_res["TP"])
            fp_list.append(tmp_res["FP"])
            np_list.append(tmp_res["NP"])

            results["detail"].append({"class": class_id, **tmp_res})

        results["mAP"] = round(np.mean([x["AP"] for x in results["detail"]]), 3)

        micro_result = _calculate_precision_recall_fscore(
            tp_list, fp_list, np_list, average="micro"
        )
        macro_result = _calculate_precision_recall_fscore(
            tp_list, fp_list, np_list, average="macro"
        )
        weighted_result = _calculate_precision_recall_fscore(
            tp_list, fp_list, np_list, average="weighted"
        )

        for key, res in {
            "micro": micro_result,
            "macro": macro_result,
            "weighted": weighted_result,
        }.items():
            results[f"{key}*precision"] = round(res[0], 3)
            results[f"{key}*recall"] = round(res[1], 3)
            results[f"{key}*f1score"] = round(res[2], 3)

        return results

    iou_thresholds = np.linspace(
        0.5, 0.95, int(np.round((0.95 - 0.5) / 0.05)) + 1, endpoint=True
    )

    # compute simple AP with all thresholds, using up to 100 detections, and all areas
    full_metrics = {
        round(iou, 2): _evaluate(
            iou_threshold=iou, max_detections=100, area_range=(0, np.inf)
        )
        for iou in iou_thresholds
    }

    # mAP = round(np.mean([x['mAP'] for x in full_metrics.values() if x['mAP'] is not None]), 3)

    return full_metrics


def _calculate_precision_recall_fscore(TP, FP, NP, average="weighted"):
    """
    args:
        TP: tp_list of per class
        FP: fp_list of per class
        NP: np_list of per class

    calculate precision, recall, f1score
    precision = TP / (TP + FP)
    recall = TP / NP
    f1score = 2TP / (TP + NP + FP)
    """
    if average == "macro":
        precision = sum([tp / (tp + fp + np.exp(-12)) for tp, fp in zip(TP, FP)]) / len(
            TP
        )
        recall = sum([tp / (num_p + np.exp(-12)) for tp, num_p in zip(TP, NP)]) / len(
            TP
        )
        f1score = sum(
            [
                2 * tp / (tp + num_p + fp + np.exp(-12))
                for tp, fp, num_p in zip(TP, FP, NP)
            ]
        ) / len(TP)

        return precision, recall, f1score

    elif average == "micro":
        precision = sum([tp for tp in TP]) / (
            sum([tp + fp for tp, fp in zip(TP, FP)]) + np.exp(-12)
        )
        recall = sum([tp for tp in TP]) / (sum([num_p for num_p in NP]) + np.exp(-12))
        f1score = sum([2 * tp for tp in TP]) / (
            sum([tp + num_p + fp for tp, fp, num_p in zip(TP, FP, NP)]) + np.exp(-12)
        )

        return precision, recall, f1score

    elif average == "weighted":
        total = sum([num_p for num_p in NP])

        weights = [n / total for n in NP]

        precision = sum(
            [w * tp / (tp + fp + np.exp(-12)) for w, tp, fp in zip(weights, TP, FP)]
        )
        recall = sum(
            [w * tp / (num_p + np.exp(-12)) for w, tp, num_p in zip(weights, TP, NP)]
        )
        f1score = sum(
            [
                w * 2 * tp / (tp + num_p + fp + np.exp(-12))
                for w, tp, fp, num_p in zip(weights, TP, FP, NP)
            ]
        )

        return precision, recall, f1score

    else:
        raise Exception("average must choose in (macro, micro, weighted)")


def _group_detections(detected_bboxes, groundtruth_bboxes):
    """simply group groundtruth_bboxes and detected_bboxes on a (image & class) basis"""
    bbox_info = defaultdict(lambda: {"detected": [], "ground": []})
    for detected in detected_bboxes:
        img_id = detected.get_image_name()
        class_id = detected.get_class_id()
        bbox_info[img_id, class_id]["detected"].append(detected)
    for ground in groundtruth_bboxes:
        img_id = ground.get_image_name()
        class_id = ground.get_class_id()
        bbox_info[img_id, class_id]["ground"].append(ground)

    return bbox_info


def _get_area(a):
    """COCO does not consider the outer edge as included in the bbox"""
    x, y, x2, y2 = a.get_absolute_bounding_box(format=BBFormat.XYX2Y2)
    return (x2 - x) * (y2 - y)


def _iou(a, b):
    xa, ya, x2a, y2a = a.get_absolute_bounding_box(format=BBFormat.XYX2Y2)
    xb, yb, x2b, y2b = b.get_absolute_bounding_box(format=BBFormat.XYX2Y2)

    # innermost left x
    xi = max(xa, xb)
    # innermost right x
    x2i = min(x2a, x2b)
    # same for y
    yi = max(ya, yb)
    y2i = min(y2a, y2b)

    # calculate areas
    Aa = max(x2a - xa, 0) * max(y2a - ya, 0)
    Ab = max(x2b - xb, 0) * max(y2b - yb, 0)
    Ai = max(x2i - xi, 0) * max(y2i - yi, 0)
    return Ai / (Aa + Ab - Ai)


def _compute_ious(detected, ground):
    """compute pairwise ious"""

    ious = np.zeros((len(detected), len(ground)))

    for g_idx, g in enumerate(ground):
        for d_idx, d in enumerate(detected):
            ious[d_idx, g_idx] = _iou(d, g)

    return ious


def _evaluate_image(
    detected, ground, ious, iou_threshold, max_detections=None, area_range=None
):
    """use COCO's method to associate detections to ground truths"""
    # sort dts by decreasing confidence
    detected_sort = np.argsort([-d.get_confidence() for d in detected], kind="stable")

    # sort list of dts and chop by max detections
    detected = [detected[idx] for idx in detected_sort[:max_detections]]
    ious = ious[detected_sort[:max_detections]]

    # generate ignored gt list by area_range
    def _is_ignore(bbox):
        if area_range is None:
            return False
        return not (area_range[0] <= _get_area(bbox) <= area_range[1])

    ground_ignore = [_is_ignore(g) for g in ground]

    # sort gts by ignore last
    ground_sort = np.argsort(ground_ignore, kind="stable")
    ground = [ground[idx] for idx in ground_sort]
    ground_ignore = [ground_ignore[idx] for idx in ground_sort]
    ious = ious[:, ground_sort]

    ground_match = {}
    detected_match = {}

    for d_idx, d in enumerate(detected):
        # information about best match so far (m=-1 -> unmatched)
        iou = min(iou_threshold, 1 - 1e-10)
        match = -1
        for g_idx, g in enumerate(ground):
            # if this gt already matched, and not a crowd, continue
            if g_idx in ground_match:
                continue
            # if dt matched to reg gt, and on ignore gt, stop
            if (
                match > -1
                and ground_ignore[match] == False
                and ground_ignore[g_idx] == True
            ):
                break
            # continue to next gt unless better match made
            if ious[d_idx, g_idx] < iou:
                continue
            # if match successful and best so far, store appropriately
            iou = ious[d_idx, g_idx]
            match = g_idx
        # if match made store id of match for both dt and gt
        if match == -1:
            continue
        detected_match[d_idx] = match
        ground_match[match] = d_idx

    # generate ignore list for dts
    detected_ignore = [
        ground_ignore[detected_match[d_idx]]
        if d_idx in detected_match
        else _is_ignore(d)
        for d_idx, d in enumerate(detected)
    ]

    # get score for non-ignored dts
    scores = [
        detected[d_idx].get_confidence()
        for d_idx in range(len(detected))
        if not detected_ignore[d_idx]
    ]
    matched = [
        d_idx in detected_match
        for d_idx in range(len(detected))
        if not detected_ignore[d_idx]
    ]

    n_gts = len([g_idx for g_idx in range(len(ground)) if not ground_ignore[g_idx]])
    return {"scores": scores, "matched": matched, "NP": n_gts}


def _compute_ap_recall(scores, matched, NP, recall_thresholds=None):
    """This curve tracing method has some quirks that do not appear when only unique confidence thresholds
    are used (i.e. Scikit-learn's implementation), however, in order to be consistent, the COCO's method is reproduced.
    """

    # precision = TP / (TP + FP)
    # recall = TP / NP
    # f1score = 2 * TP / (TP + NP + FP)

    if NP == 0:
        return {
            "precision": 0,
            "recall": 0,
            "AP": 0,
            "interpolated precision": [],
            "interpolated recall": [],
            "NP": 0,
            "TP": 0,
            "FP": 0,
        }

    # by default evaluate on 101 recall levels
    if recall_thresholds is None:
        recall_thresholds = np.linspace(
            0.0, 1.00, int(np.round((1.00 - 0.0) / 0.1)) + 1, endpoint=True
        )

    # sort in descending score order
    index_sort = np.argsort(-scores, kind="stable")

    # scores = scores[index_sort]
    matched = matched[index_sort]

    tp = np.cumsum(matched)
    fp = np.cumsum(~matched)

    recall = tp / NP
    precision = tp / (tp + fp)

    # make precision monotonically decreasing
    i_pr = np.maximum.accumulate(precision[::-1])[::-1]

    rec_idx = np.searchsorted(recall, recall_thresholds, side="left")
    # n_recalls = len(recall_thresholds)

    # get interpolated precision values at the evaluation thresholds
    i_pr = np.array([i_pr[r] if r < len(i_pr) else 0 for r in rec_idx])

    return {
        "precision": round(tp[-1] / (tp[-1] + fp[-1]), 3) if len(tp) != 0 else 0,
        "recall": round(tp[-1] / NP, 3) if len(tp) != 0 else 0,
        "f1score": round((2 * tp[-1]) / (tp[-1] + fp[-1] + NP), 3) if len(tp) else 0,
        # "AP": round(np.mean(i_pr), 3) if len(i_pr)  else 0,
        "AP": round(np.mean(i_pr), 3),
        "interpolated precision": [round(pr, 3) for pr in i_pr],
        "interpolated recall": [round(recall, 3) for recall in recall_thresholds],
        "NP": NP,
        "TP": tp[-1] if len(tp) != 0 else 0,
        "FP": fp[-1] if len(fp) != 0 else 0,
    }
