import { request } from '@/api/service';

export const crudOptions = vm => {
  return {
    pageOptions: {
      compact: true,
    },
    options: {
      tableType: 'vxe-table',
      rowKey: false,
      height: '100%',
      rowId: 'code',
      highlightCurrentRow: true,
      treeConfig: {
        lazy: true,
        children: 'children',
        hasChild: 'hasChildren',
        loadMethod: ({ row }) => {
          return request({
            url: '/api/system/area/',
            method: 'get',
            params: { pcode: row.code, limit: 999 },
          }).then(ret => {
            ret.data.data.map(value => {
              value.hasChildren = value.pcode_count !== 0;
            });
            row.hasChildren = false;
            return ret.data.data;
          });
        },
        iconLoaded: 'el-icon-loading', // 美化loading图标
      },
    },
    rowHandle: {
      show: false,
      width: 140,
      view: {
        thin: true,
        text: '',
        show: false,
        disabled() {
          return !vm.hasPermissions('Retrieve');
        },
      },
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
        text: '',
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
      defaultSpan: 24,
      width: '30%',
    },
    indexRow: {
      // Alternatively, simply pass' true 'without displaying the title or centering it
      title: 'Serial No',
      align: 'center',
      width: 100,
    },
    columns: [
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
        title: 'Parent region',
        key: 'pcode',
        show: false,
        search: {
          disabled: false,
        },
        type: 'area-selector',
        // dict: {
        //   url: areaJointPrefix,
        //   lazy: true,
        //   isTree: true,
        //   cache: false,
        //   value: 'code', // 数据字典中value字段的属性名
        //   label: 'name', // 数据字典中label字段的属性名
        //   children: 'children' // 数据字典中children字段的属性名
        // },
        form: {
          component: {
            showAllLevels: false, // 仅显示最后一级
            props: {
              elProps: {
                clearable: true,
                showAllLevels: false, // 仅显示最后一级
                props: {
                  checkStrictly: true, // 可以不需要选到最后一级
                  emitPath: false,
                  clearable: true,
                },
              },
            },
          },
        },
      },
      {
        title: 'Name',
        key: 'name',
        search: {
          disabled: false,
        },
        treeNode: true,
        width: 160,
        type: 'input',
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'Name is required' },
          ],
          component: {
            placeholder: 'please enter a name',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'Area code',
        key: 'code',
        search: {
          disabled: false,
        },
        type: 'input',
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'Area code is required' },
          ],
          component: {
            placeholder: 'please enter the area code',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'Pinyin',
        key: 'pinyin',
        search: {
          disabled: true,
        },
        type: 'input',
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'Pinyin required' },
          ],
          itemProps: {
            class: { yxtInput: true },
          },
          component: {
            placeholder: 'Please enter pinyin',
          },
        },
      },
      {
        title: 'Regional level',
        key: 'level',
        search: {
          disabled: true,
        },
        type: 'input',
        form: {
          disabled: false,
          rules: [
            // Form validation rules
            { required: true, message: 'Pinyin required' },
          ],
          itemProps: {
            class: { yxtInput: true },
          },
          component: {
            placeholder: 'Please enter pinyin',
          },
        },
      },
      {
        title: 'Initials',
        key: 'initials',
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'Initials are required' },
          ],
          itemProps: {
            class: { yxtInput: true },
          },
          component: {
            placeholder: 'Please enter initials',
          },
        },
      },
      {
        title: 'Whether to enable',
        key: 'enable',
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
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
    ].concat(vm.commonEndColumns()),
  };
};
