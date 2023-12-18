// import { request } from '@/api/service'
// import { BUTTON_STATUS_NUMBER } from '@/config/button'

export const crudOptions = vm => {
  return {
    pageOptions: {
      compact: true,
    },
    options: {
      tableType: 'vxe-table',
      rowKey: false,
      height: '100%',
      rowId: 'id',
      highlightCurrentRow: true,
    },
    rowHandle: {
      // show: false,
      width: 140,
      view: {
        thin: true,
        text: '',
        // show: false,
        disabled() {
          return !vm.hasPermissions('Retrieve');
        },
      },
      edit: {
        thin: true,
        text: '',
        // show: true,
        disabled() {
          return !vm.hasPermissions('Update');
        },
      },
      remove: {
        thin: true,
        text: '',
        // show: true,
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
      title: '序号',
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

      //   name = models.CharField(max_length=255, blank=True, null=True)
      // department = models.CharField(max_length=255, blank=True, null=True)
      // project_manager = models.CharField(max_length=255, blank=True, null=True)
      // description

      {
        title: 'name',
        key: 'name',
        sortable: true,
        treeNode: true,
        type: 'input',
        form: {
          editDisabled: true,
          rules: [
            // Form validation rules
            { required: true, message: 'project名称必填' },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: '请输入project名称',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'department',
        key: 'department',
        search: {
          disabled: false,
        },
        treeNode: true,
        width: 160,
        type: 'input',
        form: {
          rules: [
            // Form validation rules
            { required: true, message: '部门必填项' },
          ],
          component: {
            placeholder: '请输入部门',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'project_manager',
        key: 'project_manager',
        search: {
          disabled: false,
        },
        type: 'input',
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'PM必填项' },
          ],
          component: {
            placeholder: '请输入PM',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'description',
        key: 'description',
        search: {
          disabled: true,
        },
        type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true },
          },
          component: {
            placeholder: '请输入描述',
          },
        },
      },
    ].concat(vm.commonEndColumns()),
  };
};
