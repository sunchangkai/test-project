import { request } from '@/api/service';
import { tableListUrl } from '@/views/prosafeAI/dataManager/api';
import { urlVersionPrefix } from '@/views/prosafeAI/metadataInfo/api';

export const samplecodePrefix = '/api/prosafeai/modelV_crud/generate_code/';
export const taskListPrefix = '/api/prosafeai/modelV_crud/modelV_task_list/';
export const taskAddUrl = '/api/prosafeai/modelV_crud/create_task/';

export function GetTaskList(query) {
  return request({
    url: taskListPrefix,
    method: 'get',
    params: query,
  });
}

export function createTask(obj) {
  return request({
    url: taskAddUrl,
    method: 'post',
    data: obj,
  });
}

export function GetTableList() {
  return request({
    url: tableListUrl,
    method: 'get',
  });
}

export function GetSampleCode(query) {
  return request({
    url: samplecodePrefix,
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
