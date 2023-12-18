export const crudOptions = vm => {
  return {
    pageOptions: {
      compact: true,
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true,
      rowId: 'id',
      height: '100%',
      highlightCurrentRow: false,
    },
    rowHandle: {
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled() {
          return !vm.hasPermissions('Retrieve');
        },
      },
      width: 70,
      edit: {
        thin: true,
        text: '',
        show: false,
        disabled() {
          return !vm.hasPermissions('Update');
        },
      },
      remove: {
        thin: true,
        text: 'delete',
        show: false,
        disabled() {
          return !vm.hasPermissions('Delete');
        },
      },
    },
    viewOptions: {
      componentType: 'form',
    },
    formOptions: {
      disabled: true,
      defaultSpan: 12,
    },
    indexRow: {
      // Alternatively, simply pass' true 'without displaying the title or centering it
      title: 'Serial No',
      align: 'center',
      width: 70,
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
          show: false,
          component: {
            placeholder: 'please input the key words',
          },
        },
      },
      {
        title: 'ID',
        key: 'id',
        width: 90,
        disabled: true,
        form: {
          disabled: true,
        },
      },
      {
        title: 'Request module',
        key: 'request_modular',
        search: {
          disabled: false,
        },
        width: 140,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: 'Please enter request module',
          },
        },
      },
      {
        title: 'Request path',
        key: 'request_path',
        search: {
          disabled: false,
        },
        width: 220,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: 'please input request path',
          },
        },
      },
      {
        title: 'Request params',
        key: 'request_body',
        search: {
          disabled: true,
        },
        disabled: true,
        type: 'textarea',
        form: {
          disabled: true,
          component: {
            props: {
              type: 'textarea',
            },
            autosize: {
              minRows: 2,
              maxRows: 8,
            },
            placeholder: 'please input request parameters',
          },
        },
      },
      {
        title: 'Request method',
        key: 'request_method',
        width: 80,
        type: 'input',
        search: {
          disabled: false,
        },
        form: {
          disabled: true,
          component: {
            placeholder: 'please input request method',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Instructions',
        key: 'request_msg',
        disabled: true,
        form: {
          component: {
            span: 12,
          },
        },
      },
      {
        title: 'IP address',
        key: 'request_ip',
        search: {
          disabled: false,
        },
        width: 130,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: 'please input IP address',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Request browser',
        key: 'request_browser',
        width: 180,
        type: 'input',
        form: {
          disabled: true,
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Response code',
        key: 'response_code',
        search: {
          disabled: true,
        },
        width: 80,
        type: 'input',
        form: {
          disabled: true,
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'OS',
        key: 'request_os',
        disabled: true,
        search: {
          disabled: true,
        },
        type: 'input',
        form: {
          disabled: true,
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Response',
        key: 'json_result',
        search: {
          disabled: true,
        },
        minWidth: 240,
        type: 'input',
        form: {
          disabled: true,
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Operator',
        width: 100,
        key: 'creator_name',
        form: {
          disabled: true,
        },
      },
      {
        title: 'Update time',
        key: 'update_datetime',
        width: 160,
        show: false,
        type: 'datetime',
        form: {
          disabled: true,
        },
      },
      {
        fixed: 'right',
        title: 'operate time',
        key: 'create_datetime',
        width: 160,
        type: 'datetime',
        form: {
          disabled: true,
        },
      },
    ],
  };
};
