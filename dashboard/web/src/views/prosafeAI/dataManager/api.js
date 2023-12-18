import { request } from '@/api/service';

export const tableListUrl = '/api/prosafeai/prosafeai_tables/';

export function GetList(query) {
  return request({
    url: tableListUrl,
    method: 'get',
    params: query,
  });
}
