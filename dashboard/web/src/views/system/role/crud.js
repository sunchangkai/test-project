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
      view: {
        thin: true,
        text: '',
        disabled() {
          return !vm.hasPermissions('Retrieve');
        },
      },
      width: 330,
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
          show(index, row) {
            return true;
          },
          disabled() {
            return !vm.hasPermissions('Update');
          },
          text: 'Authority management',
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
      width: 100,
    },

    viewOptions: {
      componentType: 'form',
    },
    formOptions: {
      defaultSpan: 24,
      width: '35%',
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
        title: 'Role name',
        key: 'name',
        sortable: true,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true,
            },
          },
        },

        type: 'input',
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'role name required' },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: 'please input role name',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'Authority ID',
        key: 'key',
        sortable: true,
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'Authority ID required' },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: 'please input Authority ID',
          },
          itemProps: {
            class: { yxtInput: true },
          },
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
            placeholder: 'please input sort',
          },
        },
      },
      {
        title: 'Is administrator',
        key: 'admin',
        sortable: true,

        type: 'radio',
        dict: {
          data: vm.dictionary('button_whether_bool'),
        },
        form: {
          value: false,
          component: {
            placeholder: 'Please choose whether to be an administrator',
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
        type: 'radio',
        dict: {
          data: vm.dictionary('button_status_bool'),
        },
        form: {
          value: true,
          component: {
            placeholder: 'please choose status',
          },
        },
        component: { props: { color: 'auto' } },
      },
    ].concat(vm.commonEndColumns()),
  };
};
