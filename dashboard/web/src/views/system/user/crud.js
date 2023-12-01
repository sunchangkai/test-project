import { request } from '@/api/service';
import util from '@/libs/util';

export const crudOptions = vm => {
  util.filterParams(vm, ['dept_name', 'role_info{name}', 'dept_name_all']);
  return {
    pageOptions: {
      compact: true,
    },
    options: {
      height: '100%',
      tableType: 'vxe-table',
      rowKey: true,
      rowId: 'id',
    },
    selectionRow: {
      align: 'center',
      width: 46,
    },
    rowHandle: {
      width: 240,
      fixed: 'right',
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
      custom: [
        {
          thin: true,
          text: 'Reset password',
          size: 'small',
          type: 'warning',
          icon: 'el-icon-refresh-left',
          show() {
            return vm.hasPermissions('ResetPassword');
          },
          emit: 'resetPassword',
        },
      ],
    },
    viewOptions: {
      componentType: 'form',
    },
    formOptions: {
      defaultSpan: 12,
    },
    indexRow: {
      // Alternatively, simply pass' true 'without displaying the title or centering it
      title: 'Serial No',
      align: 'center',
      width: 60,
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
        disabled: true,
        form: {
          disabled: true,
        },
      },
      {
        title: 'Account',
        key: 'username',
        search: {
          disabled: false,
        },
        minWidth: 100,
        type: 'input',
        form: {
          rules: [
            // Form validation rules
            {
              required: true,
              message: 'Account required',
            },
          ],
          component: {
            placeholder: 'please input account',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'Password',
        key: 'password',
        minWidth: 90,
        type: 'input',
        form: {
          rules: [
            // Form validation rules
            {
              required: true,
              message: 'Password required',
            },
          ],
          component: {
            span: 12,
            showPassword: true,
            placeholder: 'please input password',
          },
          value: vm.systemConfig('base.default_password'),
          editDisabled: true,
          itemProps: {
            class: { yxtInput: true },
          },
        },
        disabled: true,
        valueResolve(row, key) {
          if (row.password) {
            row.password = vm.$md5(row.password);
          }
        },
      },
      {
        title: 'Name',
        key: 'name',
        minWidth: 90,
        search: {
          disabled: false,
        },
        type: 'input',
        form: {
          rules: [
            // Form validation rules
            {
              required: true,
              message: 'Name required',
            },
          ],
          component: {
            span: 12,
            placeholder: 'please input name',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'Dept',
        key: 'dept',
        search: {
          disabled: true,
        },
        minWidth: 140,
        type: 'tree-selector',
        dict: {
          cache: true,
          isTree: true,
          url: '/api/system/dept/all_dept/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
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
            span: 12,
            pagination: true,
            props: { multiple: false },
          },
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'dept_name',
        },
      },
      {
        title: 'Role',
        key: 'role',
        search: {
          disabled: true,
        },
        minWidth: 130,
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
            span: 12,
            pagination: true,
            props: { multiple: true },
            elProps: {
              columns: [
                {
                  field: 'name',
                  title: 'Role name',
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
        title: 'Phone number',
        key: 'mobile',
        search: {
          disabled: false,
        },
        minWidth: 110,
        type: 'input',
        form: {
          rules: [
            {
              max: 20,
              message: 'please input phone number',
              trigger: 'blur',
            },
            {
              pattern: /^1[3-9]\d{9}$/,
              message: 'please input correct phone number',
            },
          ],
          itemProps: {
            class: { yxtInput: true },
          },
          component: {
            placeholder: 'please input phone number',
          },
        },
      },
      {
        title: 'Email',
        key: 'email',
        minWidth: 180,
        form: {
          rules: [
            {
              type: 'email',
              message: 'please input email',
              trigger: ['blur', 'change'],
            },
          ],
          component: {
            placeholder: 'please input email',
          },
        },
      },
      {
        title: 'Gender',
        key: 'gender',
        type: 'radio',
        width: 70,
        dict: {
          data: vm.dictionary('gender'),
        },
        form: {
          value: 1,
          component: {
            span: 12,
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'User type',
        key: 'user_type',
        search: {
          disabled: false,
        },
        width: 145,
        type: 'select',
        dict: {
          data: vm.dictionary('user_type'),
        },
        form: {
          show: false,
          value: 0,
          component: {
            span: 12,
          },
        },
      },
      {
        title: 'Status',
        key: 'is_active',
        search: {
          disabled: false,
        },
        width: 70,
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
        title: 'Avatar',
        key: 'avatar',
        type: 'avatar-cropper',
        width: 60,
        align: 'left',
        form: {
          component: {
            props: {
              elProps: {
                // 与el-uploader 配置一致
                multiple: false,
                limit: 1, // 限制5个文件
              },
              sizeLimit: 500 * 1024, // 不能超过限制
            },
            span: 24,
          },
          helper: 'Limit file size to no more than 500k',
        },
      },
    ].concat(
      vm.commonEndColumns({
        create_datetime: { showTable: false },
        update_datetime: { showTable: false },
      }),
    ),
  };
};
