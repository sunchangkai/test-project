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
        text: '删除',
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
        title: 'Username',
        key: 'username',
        search: {
          disabled: false,
        },
        width: 140,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: 'please input login username',
          },
        },
      },
      {
        title: 'IP',
        key: 'ip',
        search: {
          disabled: false,
        },
        width: 130,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: 'please input the login ip',
          },
        },
      },
      {
        title: 'ISP',
        key: 'isp',
        search: {
          disabled: true,
        },
        disabled: true,
        width: 180,
        type: 'input',
        form: {
          component: {
            placeholder: 'please input ISP',
          },
        },
      },
      {
        title: 'Continent',
        key: 'continent',
        width: 80,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: 'please input the continent',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Country',
        key: 'country',
        width: 80,
        type: 'input',
        form: {
          component: {
            placeholder: 'please input the country',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Province',
        key: 'province',
        width: 80,
        type: 'input',
        form: {
          component: {
            placeholder: 'please input the province',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'City',
        key: 'city',
        width: 80,
        type: 'input',
        form: {
          component: {
            placeholder: 'please input the City',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'District',
        key: 'district',
        width: 80,
        type: 'input',
        form: {
          component: {
            placeholder: 'please input the district',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Area code',
        key: 'area_code',
        width: 100,
        type: 'input',
        form: {
          component: {
            placeholder: 'please input the area code',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Country full name',
        key: 'country_english',
        width: 120,
        type: 'input',
        form: {
          component: {
            placeholder: 'please input country full name',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Abbreviation',
        key: 'country_code',
        width: 100,
        type: 'input',
        form: {
          component: {
            placeholder: 'please input the abbreviation',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Longitude',
        key: 'longitude',
        width: 80,
        type: 'input',
        disabled: true,
        form: {
          component: {
            placeholder: 'please input longitude',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Latitude',
        key: 'latitude',
        width: 80,
        type: 'input',
        disabled: true,
        form: {
          component: {
            placeholder: 'please input latitude',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'Login type',
        key: 'login_type',
        width: 100,
        type: 'select',
        search: {
          disabled: false,
        },
        dict: {
          data: [
            { label: 'Normal login', value: 1 },
            { label: 'WeChat scan code login', value: 2 },
          ],
        },
        form: {
          component: {
            placeholder: 'Please select a login type',
          },
        },
        component: { props: { color: 'auto' } }, // 自动染色
      },
      {
        title: 'OS',
        key: 'os',
        width: 180,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter the OS',
          },
        },
      },
      {
        title: 'Browser',
        key: 'browser',
        width: 180,
        type: 'input',
        form: {
          component: {
            placeholder: 'please input the browser name',
          },
        },
      },
      {
        title: 'agent info',
        key: 'agent',
        disabled: true,
        width: 180,
        type: 'input',
        form: {
          component: {
            placeholder: 'please input agent info',
          },
        },
      },
      {
        fixed: 'right',
        title: 'Login time',
        key: 'create_datetime',
        width: 160,
        type: 'datetime',
      },
    ],
  };
};
