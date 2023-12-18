import { downloadFile, request } from '@/api/service';

export const urlPrefix = '/api/prosafeai/table_details/';
export const urlVersionPrefix = '/api/prosafeai/version_info/';
export const urlAddVersionPrefix = '/api/prosafeai/data_management/import_data/';
export const urlExportPrefix = '/api/prosafeai/data_management/import_data/';

export function AddVersion(obj) {
  return request({
    url: urlAddVersionPrefix,
    method: 'post',
    data: obj,
  });
}

export function GetList(query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query,
  });
}

export function GetVersion(query) {
  return request({
    url: urlVersionPrefix,
    method: 'get',
    params: query,
  });
}

/**
 * 导出
 * @param params
 */
export function exportData(params) {
  return downloadFile({
    url: urlExportPrefix,
    params: params,
    method: 'get',
    filename: 'tableid_' + params.table_id,
    fileType: '.json',
  });
}
