/*
 * @Author: zhaoyang8710
 * @Date: 2023-09-13 16:59:37
 * @LastEditors: zhaoyang8710
 * @LastEditTime: 2023-09-20 17:57:43
 * @FilePath: /prosafeai-prosafeai-main/dashboard/web/src/views/prosafeAI/robustNewTask/constants.js
 */
export const bboxTypeList = [
  { value: '0', label: '(X1, Y1, X2, Y2)' },
  { value: '1', label: '(X1, Y1, W, H)' },
  { value: '2', label: '(YOLO)' },
];

export const scaleTypeList = [
  { value: 0, label: 'No' },
  { value: 1, label: 'Yes' },
];

export const groundtruthAnnoType = [
  {
    label: '(x, y, x, y)',
    value: 'xyxy',
  },
  {
    label: '(x, y, w, h)',
    value: 'xywh',
  },
  {
    label: '(x, y, x, y)_scaled',
    value: 'xyxy_scaled',
  },
  {
    label: '(x, y, w, h)_scaled',
    value: 'xywh_scaled',
  },
];
export const predictionAnnoType = [
  {
    label: '(x, y, x, y)',
    value: 'xyxy',
  },
  {
    label: '(x, y, w, h)',
    value: 'xywh',
  },
  {
    label: '(x, y, x, y)_scaled',
    value: 'xyxy_scaled',
  },
  {
    label: '(x, y, w, h)_scaled',
    value: 'xywh_scaled',
  },
];
