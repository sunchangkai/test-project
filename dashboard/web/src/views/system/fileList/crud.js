export const crudOptions = vm => {
  return {
    pageOptions: {
      compact: true,
    },
    options: {
      height: '100%',
    },
    rowHandle: {
      width: 110,
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
      width: 100,
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
        width: 90,
        disabled: true,
        form: {
          disabled: true,
        },
      },
      {
        title: 'File name',
        key: 'name',
        search: {
          disabled: false,
        },
        width: 160,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter a file name',
          },
        },
      },
      {
        title: 'File path',
        key: 'url',
        type: 'file-uploader',
        search: {
          disabled: true,
        },
        width: 220,
      },
      {
        title: 'File MD5',
        key: 'md5sum',
        width: 200,
        search: {
          disabled: true,
        },
        form: {
          disabled: false,
        },
      },
      {
        title: 'Remark',
        key: 'description',
        show: false,
        search: {
          disabled: true,
        },
        type: 'textarea',
        form: {
          component: {
            placeholder: 'Please enter content',
            showWordLimit: true,
            maxlength: '200',
            props: {
              type: 'textarea',
            },
          },
        },
      },
      {
        title: 'Creator',
        show: false,
        width: 100,
        key: 'modifier_name',
        form: {
          disabled: true,
        },
      },
      {
        title: 'Update time',
        key: 'update_datetime',
        width: 160,
        type: 'datetime',
        form: {
          disabled: true,
        },
      },
      {
        title: 'Creation time',
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
