/*
 * @创建文件时间: 2021-06-03 00:50:28
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-07-29 22:49:02
 * 联系Qq:1638245306
 * @文件介绍: 菜单的按钮和接口配置
 */
import { request } from '@/api/service';
export const crudOptions = vm => {
  return {
    pageOptions: {
      compact: true,
    },
    options: {
      tableType: 'vxe-table',
      rowKey: false,
      width: '100%',
      height: '100%',
    },
    rowHandle: {
      width: 180,
      edit: {
        thin: true,
        text: 'edit',
      },
      remove: {
        thin: true,
        text: 'delete',
      },
    },
    indexRow: {
      // Alternatively, simply pass' true 'without displaying the title or centering it
      title: 'Serial No',
      align: 'center',
      width: 100,
    },
    viewOptions: {
      disabled: true,
      componentType: 'form',
    },
    formOptions: {
      defaultSpan: 24,
    },
    columns: [
      {
        title: 'Key words',
        key: 'search',
        show: false,
        disabled: true,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true,
            },
            placeholder: 'please input key words',
          },
        },
        form: {
          disabled: true,
        },
        view: {
          disabled: true,
        },
      },
      {
        title: 'ID',
        key: 'id',
        show: false,
        width: 90,
        form: {
          disabled: true,
        },
      },

      {
        title: 'Permission name',
        key: 'name',
        sortable: true,
        width: 150,
        search: {
          disabled: false,
        },
        type: 'select',
        dict: {
          data: vm.dictionary('system_button'),
        },
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'required' },
          ],
          component: {
            span: 12,
            props: {
              clearable: true,
              elProps: {
                allowCreate: true,
                filterable: true,
                clearable: true,
              },
            },
          },
          itemProps: {
            class: { yxtInput: true },
          },
          valueChange(key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            if (value != null) {
              const obj = component.dictOptions.find(item => {
                return item.value === value;
              });
              if (obj && obj.value) {
                form.name = obj.label;
                form.value = obj.value;
              }
            }
          },
          helper: {
            render(h) {
              return (
                <el-alert
                  title="A new value not in the list can be entered manually"
                  type="warning"
                  description="The more commonly used suggestions are placed in dictionary management"
                />
              );
            },
          },
        },
      },
      {
        title: 'Permission value',
        key: 'value',
        sortable: true,
        width: 200,
        search: {
          disabled: false,
        },
        type: 'input',
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'required' },
          ],
          component: {
            span: 12,
            placeholder: 'please input permission value',
            props: {
              elProps: {
                clearable: true,
              },
            },
          },
          itemProps: {
            class: { yxtInput: true },
          },
          helper: {
            render(h) {
              return (
                <el-alert
                  title="Judgment display for front-end button permissions"
                  type="warning"
                  description="How to use: vm.hasPermissions (permission value)"
                />
              );
            },
          },
        },
      },
      {
        title: 'Request method',
        key: 'method',
        sortable: true,
        width: 150,
        search: {
          disabled: false,
        },
        type: 'select',
        dict: {
          data: [
            { label: 'GET', value: 0 },
            { label: 'POST', value: 1 },
            { label: 'PUT', value: 2 },
            { label: 'DELETE', value: 3 },
          ],
        },
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'required' },
          ],
          component: {
            span: 12,
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'Interface path',
        key: 'api',
        sortable: true,
        search: {
          disabled: true,
        },
        type: 'select',
        dict: {
          url: '/swagger.json',
          label: 'label',
          value: 'value',
          getData: (url, dict) => {
            return request({ url: url }).then(ret => {
              const res = Object.keys(ret.paths);
              const data = [];
              for (const item of res) {
                const obj = {};
                obj.label = item;
                obj.value = item;
                data.push(obj);
              }
              return data;
            });
          },
        },
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'required' },
          ],
          component: {
            span: 24,
            props: {
              elProps: {
                allowCreate: true,
                filterable: true,
                clearable: true,
              },
            },
          },
          itemProps: {
            class: { yxtInput: true },
          },
          helper: {
            render(h) {
              return (
                <el-alert
                  title="Please fill in correctly to avoid being intercepted when requesting. Match singletons using regex,For example: /api/xx/.*?/"
                  type="warning"
                />
              );
            },
          },
        },
      },
    ],
  };
};
