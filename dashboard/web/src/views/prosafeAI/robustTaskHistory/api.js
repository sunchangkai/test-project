import { downloadFile, request } from '@/api/service';
export const urlPrefix = '/api/prosafeai/prosafeai_tables/';
export const taskHistoryPrefix = '/api/prosafeai/modelV_crud/modelV_run_list/';
export const reviewCodeUrl = '/api/prosafeai/modelV_crud/review_code/';
export const downloadUrl = '/api/prosafeai/modelV_crud/download_report/';

/**
 * 导出
 * @param params
 */
export function exportData(params) {
  return downloadFile({
    url: downloadUrl,
    params: params,
    method: 'get',
    filename: 'run_id' + params.run_id,
    fileType: '.pdf',
  });
}
export function GetHistoryList(query) {
  return request({
    url: taskHistoryPrefix,
    method: 'get',
    params: query,
  });
}

export function GetList(query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query,
  });
}

export function ReviewCode(query) {
  return request({
    url: reviewCodeUrl,
    method: 'get',
    params: query,
  });
}
