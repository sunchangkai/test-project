import { request } from '@/api/service';
import { urlVersionPrefix } from '@/views/prosafeAI/metadataInfo/api';

export const urlChartPrefix = 'api/prosafeai/data_display/data_statistics/';
export const urlOddList = 'api/prosafeai/table_field_info/';

export function GetOddList(query) {
  return request({
    url: urlOddList,
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
export function GetChartData(obj) {
  return request({
    url: urlChartPrefix,
    method: 'post',
    data: obj,
  });
}
