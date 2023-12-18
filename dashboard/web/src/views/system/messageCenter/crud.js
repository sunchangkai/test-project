import { request } from '@/api/service';

export const crudOptions = vm => {
  return {
    indexRow: {
      // Alternatively, simply pass' true 'without displaying the title or centering it
      width: 60,
      title: 'Serial No',
      align: 'center',
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true,
      height: '100%',
    },
    rowHandle: {
      width: 160,
      fixed: 'right',
      view: false,
      edit: {
        thin: true,
        text: '',
        show() {
          return vm.tabActivted !== 'receive';
        },
        disabled() {
          return !vm.hasPermissions('Update');
        },
      },
      remove: {
        thin: true,
        text: '',
        show() {
          return vm.tabActivted !== 'receive';
        },
        disabled() {
          return !vm.hasPermissions('Delete');
        },
      },
      custom: [
        {
          thin: true,
          text: null,
          icon: 'el-icon-view',
          size: 'small',
          disabled() {
            return !vm.hasPermissions('Retrieve');
          },
          order: 1,
          emit: 'onView',
        },
      ],
    },
    columns: [
      {
        title: 'Id',
        key: 'id',
        width: 100,
        form: { disabled: true },
      },
      {
        title: 'Title',
        key: 'title',
        search: {
          disabled: false,
        },
        width: 200,
        form: {
          rules: [
            // Form validation rules
            {
              required: true,
              message: 'required',
            },
          ],
          component: { span: 24, placeholder: 'please input the title' },
        },
      },
      {
        title: 'Whether read',
        key: 'is_read',
        type: 'select',
        width: 100,
        show() {
          return vm.tabActivted === 'receive';
        },
        dict: {
          data: [
            { label: 'read', value: true, color: 'success' },
            { label: 'unread', value: false, color: 'danger' },
          ],
        },
        form: {
          disabled: true,
        },
      },
      {
        title: 'Target type',
        key: 'target_type',
        type: 'radio',
        width: 120,
        show() {
          return vm.tabActivted === 'send';
        },
        dict: {
          data: [
            { value: 0, label: 'by user' },
            { value: 1, label: 'by role' },
            { value: 2, label: 'by dept' },
            { value: 3, label: 'announcement' },
          ],
        },
        form: {
          component: {
            span: 24,
            props: {
              type: 'el-radio-button',
            },
          },
          rules: [
            {
              required: true,
              message: 'required',
              trigger: ['blur', 'change'],
            },
          ],
        },
      },
      {
        title: 'Target users',
        key: 'target_user',
        search: {
          disabled: true,
        },
        width: 130,
        type: 'table-selector',
        disabled: true,
        dict: {
          cache: false,
          url: '/api/system/user/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          getData: (url, dict, { form, component }) => {
            return request({
              url: url,
              params: {
                page: 1,
                limit: 10,
              },
            }).then(ret => {
              component._elProps.page = ret.data.page;
              component._elProps.limit = ret.data.limit;
              component._elProps.total = ret.data.total;
              return ret.data.data;
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
          itemProps: {
            class: { yxtInput: true },
          },
          component: {
            span: 24,
            show(context) {
              return context.form.target_type === 0;
            },
            pagination: true,
            props: { multiple: true },
            elProps: {
              columns: [
                {
                  field: 'name',
                  title: 'user name',
                },
                {
                  field: 'phone',
                  title: 'user phone',
                },
              ],
            },
          },
        },
        component: {
          name: 'manyToMany',
          valueBinding: 'user_info',
          children: 'name',
        },
      },
      {
        title: 'Target role',
        key: 'target_role',
        search: {
          disabled: true,
        },
        disabled: true,
        width: 130,
        type: 'table-selector',
        dict: {
          cache: false,
          url: '/api/system/role/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          getData: (url, dict, { form, component }) => {
            return request({
              url: url,
              params: {
                page: 1,
                limit: 10,
              },
            }).then(ret => {
              component._elProps.page = ret.data.page;
              component._elProps.limit = ret.data.limit;
              component._elProps.total = ret.data.total;
              return ret.data.data;
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
          itemProps: {
            class: { yxtInput: true },
          },
          component: {
            span: 24,
            show(context) {
              return context.form.target_type === 1;
            },
            pagination: true,
            props: { multiple: true },
            elProps: {
              columns: [
                {
                  field: 'name',
                  title: 'role name',
                },
                {
                  field: 'key',
                  title: 'Authority ID',
                },
              ],
            },
          },
        },
        component: {
          name: 'manyToMany',
          valueBinding: 'role_info',
          children: 'name',
        },
      },
      {
        title: 'Target dept',
        key: 'target_dept',
        search: {
          disabled: true,
        },
        width: 130,
        type: 'table-selector',
        dict: {
          cache: false,
          url: '/api/system/dept/all_dept/',
          isTree: true,
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          children: 'children', // 数据字典中children字段的属性名
          getData: (url, dict, { form, component }) => {
            return request({
              url: url,
            }).then(ret => {
              return ret.data.data;
            });
          },
        },
        disabled: true,
        form: {
          rules: [
            // Form validation rules
            {
              required: true,
              message: 'required',
            },
          ],
          itemProps: {
            class: { yxtInput: true },
          },
          component: {
            span: 24,
            show(context) {
              return context.form.target_type === 2;
            },
            props: {
              multiple: true,
              elProps: {
                treeConfig: {
                  transform: true,
                  rowField: 'id',
                  parentField: 'parent',
                  expandAll: true,
                },
                columns: [
                  {
                    field: 'name',
                    title: 'dept name',
                    treeNode: true,
                  },
                  {
                    field: 'status_label',
                    title: 'status',
                  },
                  {
                    field: 'parent_name',
                    title: 'parent dept',
                  },
                ],
              },
            },
          },
        },
        component: {
          name: 'manyToMany',
          valueBinding: 'dept_info',
          children: 'name',
        },
      },
      {
        title: 'Content',
        key: 'content',
        minWidth: 300,
        type: 'editor-quill', // 富文本图片上传依赖file-uploader，请先配置好file-uploader
        form: {
          rules: [
            // Form validation rules
            {
              required: true,
              message: 'required',
            },
          ],
          component: {
            disabled: () => {
              return vm.getEditForm().disable;
            },
            props: {
              uploader: {
                type: 'form', // 上传后端类型【cos,aliyun,oss,form】
              },
            },
            events: {
              'text-change': event => {
                console.log('text-change:', event);
              },
            },
          },
        },
      },
    ].concat(
      vm.commonEndColumns({
        create_datetime: { showTable: true },
        update_datetime: { showTable: false },
      }),
    ),
  };
};
