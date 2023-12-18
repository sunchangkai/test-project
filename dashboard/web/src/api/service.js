import axios from 'axios';
import Adapter from 'axios-mock-adapter';
import { get } from 'lodash';
import util from '@/libs/util';
import { dataNotFound, errorCreate, errorLog } from './tools';
import router from '@/router';
import qs from 'qs';

/**
 * @description Create Request Instance
 */
axios.defaults.retry = 1;
axios.defaults.retryDelay = 1000;

export function getErrorMessage(code, msg) {
  if (typeof msg === 'string') {
    // return 'response code: ' + code + ' msg:' + msg
    return msg;
  }
  if (typeof msg === 'object') {
    if (msg.code === 'token_not_valid') {
      util.cookies.remove('token');
      util.cookies.remove('uuid');
      router.push({ path: '/login' });
      router.go(0);
      return 'Login timed out, please log in again!';
    }
    if (msg.code === 'user_not_found') {
      util.cookies.remove('token');
      util.cookies.remove('uuid');
      router.push({ path: '/login' });
      router.go(0);
      return 'User is invalid, please log in again!';
    }
    return Object.values(msg);
  }
  if (Object.prototype.toString.call(msg).slice(8, -1) === 'Array') {
    return msg;
  }
  return msg;
}

function createService() {
  const service = axios.create({
    baseURL: util.baseURL(),
    timeout: 20000,
    paramsSerializer: params => qs.stringify(params, { indices: false }),
  });

  service.interceptors.request.use(
    config => config,
    error => {
      console.log(error);
      return Promise.reject(error);
    },
  );
  service.interceptors.response.use(
    response => {
      // console.log('raw response ', response)
      let dataAxios = response.data;
      // console.log('response.config.url ', response.config.url)
      if (
        response.config.url === '/api/prosafeai/modelV_crud/download_report/' ||
        response.config.url === '/api/prosafeai/modelV_crud/download_hyperparameter/'
      ) {
        if (response.headers['content-type'] === 'application/json') {
          const fileReader = new FileReader();
          fileReader.onload = e => {
            console.log('filereader e:', e.target.result);
            try {
              const jsonData = JSON.parse(e.target.result);
              console.log('filereader :', jsonData);
              if (jsonData.code !== 2000) {
                errorCreate(jsonData.msg);
              }
            } catch (err) {
              console.log('parse json err:', err);
              // errorCreate('parse json error！')
            }
          };
          fileReader.readAsText(dataAxios);
        }
      }
      if (response.headers['content-disposition']) {
        dataAxios = response;
      }
      // This status code is agreed with the backend
      const { code } = dataAxios;
      // Judging based on code
      if (code === undefined) {
        // If there is no code, it means that this is not an interface developed by the backend of the project, such as D2Admin requesting the latest version
        return dataAxios;
      } else {
        // Having a code indicates that this is a backend interface for further judgment
        switch (code) {
          case 2000:
            // [Example] code===2000 represents no errors
            // TODO may require code and msg for subsequent processing, so removing. data returns all results
            // return dataAxios.data
            return dataAxios;
          case 401:
            // TODO Incomplete replacement token
            util.cookies.remove('token');
            util.cookies.remove('uuid');
            util.cookies.remove('refresh');
            router.push({ path: '/login' });
            errorCreate(`${getErrorMessage(401, dataAxios.msg)}`);
            break;
          case 404:
            dataNotFound(`${dataAxios.msg}`);
            break;
          case 4000:
            errorCreate(`${getErrorMessage(4000, dataAxios.msg)}`);
            console.log('resonpse msg:' + dataAxios.msg);
            break;
          case 400:
            console.log('response 400:' + dataAxios.msg);
            errorCreate(`${dataAxios.msg}`);
            break;
          default:
            errorCreate(`${dataAxios.msg}: ${response.config.url}`);
            break;
        }
      }
    },
    error => {
      const status = get(error, 'response.status');
      switch (status) {
        case 400:
          error.message = 'Request Error';
          break;
        case 401:
          refreshTken()
            .then(res => {
              util.cookies.set('token', res.access);
            })
            .catch(e => {
              router.push({ name: 'login' });
              router.go(0);
              error.message = 'Unauthenticated, please log in';
            });
          break;
        case 403:
          error.message = 'access denied';
          break;
        case 404:
          error.message = `Request address error: ${error.response.config.url}`;
          break;
        case 408:
          error.message = 'Request timed out';
          break;
        case 500:
          error.message = 'internal server error';
          break;
        case 501:
          error.message = 'service not implemented';
          break;
        case 502:
          error.message = 'gateway error';
          break;
        case 503:
          error.message = 'service is not available';
          break;
        case 504:
          error.message = 'gateway timeout';
          break;
        case 505:
          error.message = 'HTTP version not supported';
          break;
        default:
          break;
      }
      errorLog(error);
      return Promise.reject(error);
    },
  );
  return service;
}

/**
 * @description Create Request Method
 * @param {Object} service axios 实例
 */
function createRequestFunction(service) {
  // Verify if it is in tenant mode. Tenant mode replaces domain name with domain name and port
  return function(config) {
    const token = util.cookies.get('token');
    // Perform Boolean compatibility
    var params = get(config, 'params', {});
    for (const key of Object.keys(params)) {
      if (String(params[key]) === 'true') {
        params[key] = 1;
      }
      if (String(params[key]) === 'false') {
        params[key] = 0;
      }
    }

    const configDefault = {
      headers: {
        Authorization: 'JWT ' + token,
        'Content-Type': get(config, 'headers.Content-Type', 'application/json'),
      },
      timeout: 60000,
      baseURL: util.baseURL(),
      data: {},
      params: params,
    };

    return service(Object.assign(configDefault, config));
  };
}

// Examples and request methods for real network requests
export const service = createService();
export const request = createRequestFunction(service);

// Examples and request methods for simulating network requests
export const serviceForMock = createService();
export const requestForMock = createRequestFunction(serviceForMock);

// Network Request Data Simulation Tool
export const mock = new Adapter(serviceForMock);

const refreshTken = function() {
  const refresh = util.cookies.get('refresh');
  return request({
    url: 'token/refresh/',
    method: 'post',
    data: {
      refresh: refresh,
    },
  });
};

/**
 * Download files
 * @param url
 * @param params
 * @param method
 * @param filename
 */
export const downloadFile = function({ url, params, method, filename, fileType = '.pdf' }) {
  request({
    url: url,
    method: method,
    params: params,
    responseType: 'blob', // If this attribute is added, the error code will not be received. So we need to remove it.
  })
    .then(res => {
      console.log(res);
      const data = { type: 'application/pdf;charset-UTF-8' };

      const blob = new Blob([res.data], data);
      if (!res.data) {
        // errorCreate(`This run is failed. Please re-run the task`)
        return;
      }
      const reader = new FileReader();
      reader.onload = e => {
        console.log('e.target', e.target);
        const objectUrl = URL.createObjectURL(blob);
        // console.log(objectUrl);
        const a = document.createElement('a');
        // console.log(res.headers);
        // let filename = res.headers['content-disposition'].split(';')[1].split('filename=')[1];
        // console.log(filename)
        const filenameStr = window.decodeURI(
          filename + fileType || res.headers['content-disposition'].split('=')[1],
        );
        a.download = String(filenameStr);
        a.href = objectUrl;
        a.click();
        window.URL.revokeObjectURL(a.href);
      };
      reader.readAsText(blob);
    })
    .catch(err => {
      console.log(err);
    });
};
