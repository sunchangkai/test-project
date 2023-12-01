/*
 * @创建文件时间: 2021-06-01 22:41:19
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-08-01 02:35:45
 * 联系Qq:1638245306
 * @文件介绍:
 */
import { Message } from 'element-ui';
import store from '@/store';
import util from '@/libs/util';

/**
 * @description Securely parsing JSON strings
 * @param {String} jsonString JSON string that needs to be parsed
 * @param {String} defaultValue
 */
export function parse(jsonString = '{}', defaultValue = {}) {
  let result = defaultValue;
  try {
    result = JSON.parse(jsonString);
  } catch (error) {
    console.log(error);
  }
  return result;
}

export function response(data = {}, msg = '', code = 0) {
  return [200, { code, msg, data }];
}

export function responseSuccess(data = {}, msg = '成功') {
  return response(data, msg);
}

export function responseError(data = {}, msg = '请求失败', code = 500) {
  return response(data, msg, code);
}

export function errorLog(error) {
  store.dispatch('d2admin/log/push', {
    message: '数据请求异常',
    type: 'danger',
    meta: {
      error,
    },
  });
  if (process.env.NODE_ENV === 'development') {
    util.log.danger('>>>>>> Error >>>>>>');
    console.log(error);
  }
  Message({
    message: error.message,
    type: 'error',
    duration: 5 * 1000,
  });
}

export function errorCreate(msg) {
  const error = new Error(msg);
  errorLog(error);
  throw error;
}

export function dataNotFound(msg) {
  Message({
    message: msg,
    type: 'info',
    duration: 5 * 1000,
  });
}

export function successMsg(msg) {
  Message({
    message: msg,
    type: 'success',
    duration: 5 * 1000,
  });
}
