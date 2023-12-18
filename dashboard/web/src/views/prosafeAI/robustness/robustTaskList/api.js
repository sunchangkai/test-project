import { downloadFile, request } from '@/api/service';

import { urlVersionPrefix } from '@/views/prosafeAI/metadataInfo/api';
import { downYamlUrl } from '@/views/prosafeAI/robustNewTask/api';

export const samplecodePrefix = '/api/prosafeai/modelV_crud/generate_code/';
export const taskListPrefix = '/api/prosafeai/modelV_crud/modelV_task_list/';

/**
 * 导出
 * @param params
 */
export function downloadYaml(params) {
  return downloadFile({
    url: downYamlUrl,
    params: params,
    method: 'get',
    filename: 'task_id' + params.task_id,
    fileType: '.yaml',
  });
}

export function GetTaskList(query) {
  return request({
    url: taskListPrefix,
    method: 'get',
    params: query,
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
