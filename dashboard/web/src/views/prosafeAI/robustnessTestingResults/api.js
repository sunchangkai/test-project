import { request, downloadFile } from '@/api/service';

export const urlPrefix = 'api/prosafeai/modelV_crud/';

export function getEchartsData(data) {
  return request({
    url: urlPrefix + 'view_robustness_metrics/',
    method: 'post',
    data,
  });
}

export function getRunLabels(params) {
  return request({
    url: urlPrefix + 'get_run_labels/',
    method: 'get',
    params,
  });
}

export function getRunAttackMethods(params) {
  return request({
    url: urlPrefix + 'get_run_attack_methods/',
    method: 'get',
    params,
  });
}

export function getAttackSampleInfoList(params) {
  return request({
    url: urlPrefix + 'view_attack_sample_info/',
    method: 'get',
    params,
  });
}

export function downloadTxt(params) {
  return downloadFile({
    url: urlPrefix + 'download_attack_sample/',
    params: params,
    method: 'get',
    filename: 'run_id' + params.run_id,
    fileType: '.txt',
  });
}
