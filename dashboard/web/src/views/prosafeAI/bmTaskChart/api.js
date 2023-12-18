import { request } from '@/api/service';

export const basicChartUrl = '/api/prosafeai/modelV_crud/view_basic_metrics/';
export const sliceChartUrl = '/api/prosafeai/modelV_crud/view_slices_basic_metrics/';
export const urlOddList = '/api/prosafeai/table_field_info/';

export function GetOddList(query) {
  return request({
    url: urlOddList,
    method: 'get',
    params: query,
  });
}
export function GetBasicChart(obj) {
  return request({
    url: basicChartUrl,
    method: 'post',
    data: obj,
  });
}

export function GetSliceChart(obj) {
  return request({
    url: sliceChartUrl,
    method: 'post',
    data: obj,
  });
}
