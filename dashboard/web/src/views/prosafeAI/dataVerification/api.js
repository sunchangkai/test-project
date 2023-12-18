import { downloadFile, request } from '@/api/service';
// import { urlPrefix } from '@/views/system/user/api'
// downloadJsonFile
export const urlTask = '/api/prosafeai/task_list/';
export const urlVersion = '/api/prosafeai/version_info/';
export const urlTable = '/api/prosafeai/prosafeai_tables/';
export const urlRequirement = '/api/prosafeai/requirements_list/';
export const urlSubRequirement = '/api/prosafeai/sub_requirements/';
export const urlSubTask = '/api/prosafeai/result_list/';
export const urlCommitCreateTask = '/api/prosafeai/data_verification/import_task/';
export const urlRunTask = '/api/prosafeai/data_verification/run_verification/';
export const urldownloadReport = 'api/prosafeai/export_report/';

export function GetList(query) {
  return request({
    url: urlTask,
    method: 'get',
    params: query,
  });
}

export function GetTable(query) {
  return request({
    url: urlTable,
    method: 'get',
    params: query,
  });
}

export function GetRequirement(query) {
  return request({
    url: urlRequirement,
    method: 'get',
    params: query,
  });
}

export function GetVersion(query) {
  return request({
    url: urlVersion,
    method: 'get',
    params: query,
  });
}

export function RunTask(obj) {
  return request({
    url: urlRunTask,
    method: 'post',
    data: obj,
  });
}

/** 导出模板操作 */
export function exportData() {
  return downloadFile({
    url: urlCommitCreateTask,
    params: {},
    filename: 'export_requirement_json_template',
    fileType: '.json',
    method: 'get',
  });
}

export function downloadReport(query) {
  return downloadFile({
    url: urldownloadReport,
    params: query,
    filename: 'export_verification_report',
    fileType: '.pdf',
    method: 'get',
  });
}

export function GetSubRequirement(query) {
  return request({
    url: urlSubRequirement,
    method: 'get',
    params: query,
  });
}

export function GetSubTask(query) {
  return request({
    url: urlSubTask,
    method: 'get',
    params: query,
  });
}

export function CommitCreateTask(obj) {
  return request({
    url: urlCommitCreateTask,
    method: 'post',
    data: obj,
  });
}

// export function AddObj (obj) {
//   return request({
//     url: '/api/system/user/',
//     method: 'post',
//     data: obj
//   })
// }
//
// export function UpdateObj (obj) {
//   return request({
//     url: urlPrefix + obj.id + '/',
//     method: 'put',
//     data: obj
//   })
// }
//
// export function DelObj (id) {
//   return request({
//     url: urlPrefix + id + '/',
//     method: 'delete',
//     data: { id }
//   })
// }
