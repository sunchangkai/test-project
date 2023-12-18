import { request } from '@/api/service';
import { tableListUrl } from '@/views/prosafeAI/dataManager/api';

export function GetList(query) {
  return request({
    url: tableListUrl,
    method: 'get',
    params: query,
  });
}
