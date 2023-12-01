import * as api from './api';
export const crudOptions = vm => {
  return {
    // pagination: false,
    pageOptions: {
      compact: true,
    },
    options: {
      tableType: 'vxe-table',
      stripe: false,
      rowKey: true,
      rowId: 'id',
      height: '100%',
      highlightCurrentRow: false,
      defaultExpandAll: true,
      treeConfig: {
        lazy: true,
        hasChild: 'has_children',
        loadMethod: ({ row }) => {
          return api.GetList({ parent: row.id, lazy: true }).then(ret => {
            return ret.data.data;
          });
        },
        iconLoaded: 'el-icon-loading', // 美化loading图标
      },
    },
    rowHandle: {
      width: 140,
      view: {
        thin: true,
        text: '',
        disabled() {
          return !vm.hasPermissions('Retrieve');
        },
      },
      edit: {
        thin: true,
        text: '',
        disabled() {
          return !vm.hasPermissions('Update');
        },
      },
      remove: {
        thin: true,
        text: '',
        disabled() {
          return !vm.hasPermissions('Delete');
        },
      },
    },
    indexRow: {
      // Alternatively, simply pass' true 'without displaying the title or centering it
      title: 'serial number',
      align: 'center',
      width: 100,
    },

    viewOptions: {
      componentType: 'form',
    },
    formOptions: {
      defaultSpan: 12,
    },
    columns: [
      {
        title: 'Key words',
        key: 'search',
        show: false,
        disabled: true,
        search: {
          disabled: false,
        },
        form: {
          disabled: true,
          component: {
            props: {
              clearable: true,
            },
            placeholder: 'Please enter a keyword',
          },
        },
        view: {
          disabled: true,
        },
      },
      {
        title: 'ID',
        key: 'id',
        show: false,
        disabled: true,
        width: 90,
        form: {
          disabled: true,
        },
      },
      {
        show: false,
        title: 'Higher office',
        key: 'parent',
        type: 'tree-selector',
        dict: {
          isTree: true,
          label: 'name',
          value: 'id',
          cache: false,
          getData: (url, dict, { form, component }) => {
            // 配置此参数会覆盖全局的getRemoteDictFunc
            return api.DeptLazy().then(ret => {
              return ret.data;
            });
          },
          getNodes(values, data) {
            // 配置行展示远程获取nodes
            return new Promise((resolve, reject) => {
              const row = vm.getEditRow();
              resolve(row.parent !== null ? [{ name: row.parent_name, id: row.parent }] : []);
            });
          },
        },
        form: {
          helper: 'Leave blank as the root node by default',
          component: {
            span: 12,
            props: {
              multiple: false,
              elProps: {
                lazy: true,
                hasChild: 'has_children',
                load(node, resolve) {
                  // 懒加载
                  api.DeptLazy({ parent: node.data.id }).then(data => {
                    resolve(data.data);
                  });
                },
              },
            },
          },
        },
      },
      {
        title: 'Department name',
        key: 'name',
        sortable: true,
        treeNode: true, // 设置为树形列
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true,
            },
          },
        },
        width: 180,
        type: 'input',
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'Department name is required' },
          ],
          component: {
            span: 12,
            props: {
              clearable: true,
            },
            placeholder: 'Please enter a department name',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'Department ID',
        key: 'key',
        sortable: true,
        form: {
          component: {
            props: {
              clearable: true,
            },
            placeholder: 'Please enter the identification characters',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'Principal',
        key: 'owner',
        sortable: true,
        form: {
          component: {
            span: 12,
            props: {
              clearable: true,
            },
            placeholder: 'Please enter the person in charge',
          },
        },
      },
      {
        title: 'Phone',
        key: 'phone',
        sortable: true,
        form: {
          component: {
            span: 12,
            props: {
              clearable: true,
            },
            placeholder: 'Please type your phone number',
          },
        },
      },
      {
        title: 'email',
        key: 'email',
        sortable: true,
        form: {
          component: {
            span: 12,
            props: {
              clearable: true,
            },
            placeholder: 'Please enter the email',
          },
          rules: [
            {
              type: 'email',
              message: 'Please enter the correct email address',
              trigger: ['blur', 'change'],
            },
          ],
        },
      },
      {
        title: 'Sort',
        key: 'sort',
        sortable: true,
        width: 80,
        type: 'number',
        form: {
          value: 1,
          component: {
            span: 12,
            placeholder: 'Please select a serial number',
          },
        },
      },
      {
        title: 'Status',
        key: 'status',
        sortable: true,
        search: {
          disabled: false,
        },
        width: 90,
        type: 'radio',
        dict: {
          data: vm.dictionary('button_status_bool'),
        },
        form: {
          value: true,
          component: {
            span: 12,
            placeholder: 'Please select a status',
          },
        },
      },
    ].concat(vm.commonEndColumns()),
  };
};
