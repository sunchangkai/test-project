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
      treeConfig: {
        children: 'children',
        hasChild: 'hasChildren',
        expandAll: true,
      },
    },
    rowHandle: {
      width: 230,
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
          text: ' Dictionary configuration',
          type: 'success',
          size: 'small',
          emit: 'dictionaryConfigure',
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
        title: 'Dictionary name',
        key: 'label',

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
            { required: true, message: 'Dictionary name is required' },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: 'Please enter a dictionary name',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'Dictionary number',
        key: 'value',
        search: {
          disabled: true,
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
            { required: true, message: 'Dictionary number required' },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: 'Please enter the dictionary number',
          },
          itemProps: {
            class: { yxtInput: true },
          },
          helper: {
            render(h) {
              return (
                <el-alert title="How to use: vm.dictionary('dictionary number')" type="warning" />
              );
            },
          },
        },
      },

      {
        title: 'Status',
        key: 'status',
        width: 90,
        search: {
          disabled: false,
        },
        type: 'radio',
        dict: {
          data: vm.dictionary('button_status_bool'),
        },
        component: {
          props: {
            options: [],
          },
        },
        form: {
          rules: [
            // Form validation rules
            { required: true, message: 'Status Required' },
          ],
          value: true,
          component: {
            placeholder: 'Please select a status',
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: 'Sort',
        key: 'sort',
        width: 90,
        type: 'number',
        form: {
          value: 1,
          component: {},
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
    ].concat(
      vm.commonEndColumns({
        description: {
          showForm: true,
          showTable: true,
        },
      }),
    ),
  };
};
