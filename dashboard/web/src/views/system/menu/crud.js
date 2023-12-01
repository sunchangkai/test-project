import { request } from '@/api/service';
import { urlPrefix as menuPrefix } from './api';
import XEUtils from 'xe-utils';
// import log from '@/libs/util.log'
export const crudOptions = vm => {
  // 验证路由地址
  const validateWebPath = (rule, value, callback) => {
    const isLink = vm.getEditForm().is_link;
    let pattern = /^\/.*?/;
    if (isLink) {
      pattern = /^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+/g;
    } else {
      pattern = /^\/.*?/;
    }
    if (!pattern.test(value)) {
      callback(new Error('Please enter the correct address'));
    } else {
      callback();
    }
  };
  return {
    pagination: false,
    pageOptions: {
      compact: true,
    },
    searchOptions: {
      // 查询配置参数,
      size: 'small',
      show: true, // 是否显示搜索工具条
      disabled: false, // 是否禁用搜索工具条
      searchAfterReset: true, // 点击重置后是否立即查询
      buttons: {
        search: {
          // 配置false，隐藏按钮
          thin: false, // 瘦模式，thin=true 且 text=null 可以设置方形按钮节省位置
          text: 'Search', // 按钮文字， null= 取消文字，↓↓↓↓也可以传入一个方法↓↓↓↓
          // text(scope){return 'xx'}
          type: 'warning', // 按钮类型
          icon: 'el-view', // 按钮图标，↓↓↓↓也可以传入一个方法↓↓↓↓
          // icon(scope){return 'xx'}
          size: 'small', // 按钮大小
          circle: false, // 圆形按钮 ，需要thin=true,且text=null
          show: true, // 是否显示按钮，↓↓↓↓也可以传入一个方法根据数据决定该按钮是否显示↓↓↓↓↓↓↓↓
          // show(index,row){return row.status==='xxx'}
          disabled: false, // 是否禁用，↓↓↓↓也可以传入一个方法根据数据决定该按钮是否禁用↓↓↓↓
          // disabled(index,row){return row.status==='xxx'}
          order: 1, // 排序号，数字小，排前面
        },
        reset: {
          thin: false, // 瘦模式，thin=true 且 text=null 可以设置方形按钮节省位置
          text: 'Reset', // 按钮文字， null= 取消文字，↓↓↓↓也可以传入一个方法↓↓↓↓
          type: 'success', // 按钮类型
          // text(scope){return 'xx'}
          icon: 'el-view', // 按钮图标，↓↓↓↓也可以传入一个方法↓↓↓↓
          // icon(scope){return 'xx'}
          size: 'small', // 按钮大小
          circle: false, // 圆形按钮 ，需要thin=true,且text=null
          show: true, // 是否显示按钮，↓↓↓↓也可以传入一个方法根据数据决定该按钮是否显示↓↓↓↓↓↓↓↓
          // show(index,row){return row.status==='xxx'}
          disabled: false, // 是否禁用，↓↓↓↓也可以传入一个方法根据数据决定该按钮是否禁用↓↓↓↓
          // disabled(index,row){return row.status==='xxx'}
          order: 2, // 排序号，数字小，排前面
        }, // 同上
      },
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true,
      rowId: 'id',
      height: '100%',
      highlightCurrentRow: false,
      // defaultExpandAll: true,
      // expandAll: true,
      treeConfig: {
        transform: true,
        rowField: 'id',
        parentField: 'parent',
        expandAll: true,
        hasChild: 'hasChild',
        lazy: true,
        loadMethod: vm.loadContentMethod,
      },
    },
    rowHandle: {
      columnHeader: 'Operation',
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
      width: 250,
      fixed: 'right',
      custom: [
        {
          show(index, row) {
            if (row.web_path && !row.is_link) {
              return true;
            }
            return false;
          },
          disabled() {
            return !vm.hasPermissions('Update');
          },
          text: 'menu button',
          type: 'warning',
          size: 'small',
          emit: 'createPermission',
        },
      ],
    },
    indexRow: {
      // Alternatively, simply pass' true 'without displaying the title or centering it
      title: 'Serial No',
      align: 'center',
      width: 80,
    },
    viewOptions: {
      componentType: 'form',
    },
    formOptions: {
      defaultSpan: 12,
      width: '50%',
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
            placeholder: 'Please enter a keyword',
          },
        },
        form: {
          disabled: true,
          component: {
            props: {
              clearable: true,
            },
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
        width: 60,
        form: {
          component: {
            show: false,
          },
        },
      },
      {
        title: 'Parent menu',
        key: 'parent',
        show: false,
        search: {
          disabled: true,
        },
        type: 'cascader',
        dict: {
          url: menuPrefix,
          cache: false,
          isTree: true,
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          children: 'children', // 数据字典中children字段的属性名
          getData: (url, dict, { form, component }) => {
            // 配置此参数会覆盖全局的getRemoteDictFunc
            return request({ url: url, params: { limit: 999, status: 1, is_catalog: 1 } }).then(
              ret => {
                const responseData = ret.data.data;
                const result = XEUtils.toArrayTree(responseData, {
                  parentKey: 'parent',
                  strict: true,
                });
                return [{ id: null, name: 'root node', children: result }];
              },
            );
          },
        },
        form: {
          component: {
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
        title: 'Menu name',
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
        minWidth: 180,
        type: 'input',
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'Menu name is required' },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: 'Please enter a menu name',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'Icon',
        key: 'icon',
        width: 60,
        type: 'icon-selector',
        form: {
          component: {
            placeholder: 'Please select icon',
          },
        },
      },
      {
        title: 'Sort',
        key: 'sort',
        width: 60,
        type: 'number',
        form: {
          value: 1,
          component: {
            placeholder: 'Please enter sort',
          },
        },
      },
      {
        title: 'Directory or not',
        key: 'is_catalog',
        width: 130,
        type: 'dict-switch',
        search: {
          disabled: true,
        },
        dict: {
          data: vm.dictionary('button_whether_bool'),
        },
        // dict: { data: [{ value: 1, label: '开启' }, { value: 0, label: '关闭' }] }
        form: {
          value: false,
          component: {
            placeholder: 'Please choose whether it is a directory',
          },
          valueChange(key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            if (!value) {
              form.web_path = undefined;
              form.component = undefined;
              form.component_name = undefined;
              form.cache = false;
              form.is_link = false;
            }
          },
        },
      },
      {
        title: 'External link',
        key: 'is_link',
        width: 100,
        type: 'radio',
        dict: {
          data: vm.dictionary('button_whether_bool'),
        },
        form: {
          value: false,
          component: {
            show(context) {
              const { form } = context;
              return !form.is_catalog;
            },
            placeholder: 'Please choose whether to link',
          },
          valueChange(key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            form.web_path = undefined;
            form.component = undefined;
            form.component_name = undefined;
            if (value) {
              getColumn('web_path').title = 'external link address';
              getColumn('web_path').component.placeholder =
                'Please enter the external link address';
              getColumn('web_path').helper = {
                render(h) {
                  return (
                    <el-alert
                      title="External link address, please start with https|http|ftp|rtsp|mms"
                      type="warning"
                    />
                  );
                },
              };
            } else {
              getColumn('web_path').title = 'routing path';
              getColumn('web_path').component.placeholder = 'Please enter the routing path';
              getColumn('web_path').helper = {
                render(h) {
                  return (
                    <el-alert
                      title="The address of the url in the browser, please start with /"
                      type="warning"
                    />
                  );
                },
              };
            }
          },
        },
      },
      {
        title: 'Routing path',
        key: 'web_path',
        width: 150,
        show: false,
        form: {
          rules: [
            { required: true, message: 'Please enter the routing path' },
            { validator: validateWebPath, trigger: 'change' },
          ],
          component: {
            show(context) {
              const { form } = context;
              return !form.is_catalog;
            },
            props: {
              clearable: true,
            },
            placeholder: 'Please enter the routing path',
          },
          helper: {
            render(h) {
              return (
                <el-alert
                  title="The address of the url in the browser, please start with /"
                  type="warning"
                />
              );
            },
          },
        },
      },
      {
        title: 'Component path',
        key: 'component',
        type: 'select',
        show: false,
        dict: {
          cache: false,
          data: vm.searchFiles(),
        },
        form: {
          rules: [{ required: true, message: 'Please select component path' }],
          component: {
            show(context) {
              const { form } = context;
              return !form.is_catalog && !form.is_link;
            },
            props: {
              clearable: true,
              filterable: true, // 可过滤选择项
            },
            placeholder: 'Please select component path',
          },
          helper: {
            render(h) {
              return <el-alert title="Dir path under the src/views" type="warning" />;
            },
          },
        },
      },
      {
        title: 'Component name',
        key: 'component_name',
        width: 170,
        form: {
          rules: [{ required: true, message: 'Please enter the component name' }],
          component: {
            show(context) {
              const { form } = context;
              return !form.is_catalog && !form.is_link;
            },
            props: {
              clearable: true,
            },
            placeholder: 'Please enter a component name',
          },
          helper: {
            render(h) {
              return <el-alert title="Name in the xx.vue" type="warning" />;
            },
          },
        },
      },
      {
        title: 'Have authority',
        key: 'menuPermission',
        type: 'select',
        width: 150,
        form: {
          disabled: true,
          component: {
            elProps: {
              // el-select的配置项，https://element.eleme.cn/#/zh-CN/component/select
              filterable: true,
              multiple: true,
              clearable: true,
            },
          },
        },
      },
      {
        title: 'Cache',
        key: 'cache',
        search: {
          disabled: false,
        },
        width: 60,
        type: 'radio',
        dict: {
          data: vm.dictionary('button_whether_bool'),
        },
        form: {
          value: false,
          component: {
            show(context) {
              const { form } = context;
              return !form.is_catalog;
            },
            placeholder: 'Please choose whether to cache',
          },
          helper: {
            render(h) {
              return (
                <el-alert
                  title="Whether to enable page caching, the component name needs to be consistent with the name in the xx.vue page"
                  type="warning"
                />
              );
            },
          },
        },
      },
      {
        title: 'Side visible',
        key: 'visible',
        search: {
          disabled: false,
        },
        width: 100,
        type: 'radio',
        dict: {
          data: vm.dictionary('button_whether_bool'),
        },
        form: {
          value: true,
          component: {
            placeholder: 'Please select side visible',
          },
          rules: [
            // Form validation rules
            { required: true, message: 'Required fields visible on side' },
          ],
          helper: {
            render(h) {
              return <el-alert title="Whether to show in the side menu" type="warning" />;
            },
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
            placeholder: 'Please select a status',
          },
          rules: [
            // Form validation rules
            { required: true, message: 'Status Required' },
          ],
        },
      },
    ].concat(
      vm.commonEndColumns({
        update_datetime: { showTable: false },
      }),
    ),
  };
};
