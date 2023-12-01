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
        text: 'Edit',
      },
      remove: {
        thin: true,
        text: 'Delete',
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
        title: 'key words',
        key: 'search',
        show: false,
        disabled: true,
        search: {
          disabled: false,
        },
        form: {
          disabled: true,
          component: {
            placeholder: 'please input key words',
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
        width: 90,
        form: {
          disabled: true,
        },
      },
      {
        title: 'Request method',
        key: 'method',
        sortable: true,
        search: {
          disabled: false,
        },
        type: 'select',
        dict: {
          data: [
            {
              label: 'GET',
              value: 0,
            },
            {
              label: 'POST',
              value: 1,
            },
            {
              label: 'PUT',
              value: 2,
            },
            {
              label: 'DELETE',
              value: 3,
            },
          ],
        },
        form: {
          rules: [
            // Form validation rules
            {
              required: true,
              message: 'required',
            },
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
        title: 'Interface address',
        key: 'url',
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
            {
              required: true,
              message: 'required',
            },
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
                  title="Please fill in correctly to avoid being intercepted when requesting. Match singletons using regular expressions, for example: /api/xx/.*?/"
                  type="warning"
                />
              );
            },
          },
        },
      },
      {
        title: 'Data authority authentication',
        key: 'enable_datasource',
        search: {
          disabled: false,
        },
        width: 150,
        type: 'radio',
        dict: {
          data: vm.dictionary('button_status_bool'),
        },
        form: {
          value: true,
          component: {
            span: 12,
          },
        },
      },
      {
        title: 'Remark',
        key: 'description',
        search: {
          disabled: true,
        },
        type: 'textarea',
        form: {
          component: {
            placeholder: 'Please enter a note',
            showWordLimit: true,
            maxlength: '200',
            props: {
              type: 'textarea',
            },
          },
        },
      },
    ],
  };
};
