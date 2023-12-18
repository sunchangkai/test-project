import { downloadFile, request } from '@/api/service';
import { tableListUrl } from '@/views/prosafeAI/dataManager/api';
import { urlVersionPrefix } from '@/views/prosafeAI/metadataInfo/api';

export const attackMethodUrl = '/api/prosafeai/modelV_crud/attack_method_info/';
export const taskAddUrl = '/api/prosafeai/modelV_crud/create_task/';
export const downYamlUrl = '/api/prosafeai/modelV_crud/download_hyperparameter/';

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

export function createTask(obj) {
  return request({
    url: taskAddUrl,
    method: 'post',
    data: obj,
  });
}

export function GetAttackMethods(query) {
  return request({
    url: attackMethodUrl,
    method: 'get',
    params: query,
  });
}

export function GetTableList() {
  return request({
    url: tableListUrl,
    method: 'get',
  });
}

export function GetVersion(query) {
  return request({
    url: urlVersionPrefix,
    method: 'get',
    params: query,
  });
}

export function GetPic(query) {
  return request({
    url: '/api/prosafeai/modelV_crud/mutation_image/',
    method: 'post',
    data: query,
  });
}

export function GetTemplates(query) {
  return request({
    url: '/api/prosafeai/modelV_crud/hyperparamter_template_list/',
    method: 'get',
    params: query,
  });
}

export function CreateTempl(data) {
  return request({
    url: '/api/prosafeai/modelV_crud/save_hyperparamter_template/',
    method: 'post',
    data,
  });
}

export function DelTempl(query) {
  return request({
    url: '/api/prosafeai/modelV_crud/delete_hyperparamter_template/',
    method: 'get',
    params: query,
  });
}
