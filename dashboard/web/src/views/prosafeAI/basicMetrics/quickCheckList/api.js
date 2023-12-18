import { downloadFile, request } from '@/api/service';
export const urlPrefix = '/api/prosafeai/modelV_crud/quick_modelV_run/';
export const downloadUrl = '/api/prosafeai/modelV_crud/download_report/';

export function GetList(query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query,
  });
}

export function exportData(params) {
  return downloadFile({
    url: downloadUrl,
    params: params,
    method: 'get',
    filename: 'run_id' + params.run_id,
    fileType: '.pdf',
  });
}
