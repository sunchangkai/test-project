export let crudOptions;
// eslint-disable-next-line prefer-const
crudOptions = vm => {
  return {
    searchOptions: {
      disabled: true,
      show: false,
    },
    pageOptions: {
      compact: true,
    },
    options: {
      tableType: 'vxe-table',
      size: 'medium',
      rowKey: false,
      height: '100%',
      rowId: 'id',
      stripe: true,
      emptyText: 'No data',
      highlightCurrentRow: true,
      rowStyle({ row, rowIndex }) {
        const stylejson = {};
        stylejson.height = 50 + 'px';
        return stylejson;
      },
    },

    rowHandle: {
      columnHeader: 'Operation',
      align: 'center',
      width: 150,
      view: { show: false },
      edit: { show: false },
      remove: { show: false },
      custom: [
        {
          thin: true,
          text: null,
          title: 'Check the details of the task',
          type: 'primary',
          icon: 'el-icon-view',
          size: 'small',
          emit: 'detailDialog',
          show(index, row) {
            return true;
          },
          disabled(index, row) {
            return false;
          },
          order: 1,
        },
        {
          thin: true,
          text: null,
          title: 'Check the sample code',
          type: 'success',
          icon: 'el-icon-document-copy',
          size: 'small',
          emit: 'showCode',
          show(index, row) {
            return true;
          },
          disabled(index, row) {
            return false;
          },
          order: 2,
        },
        {
          thin: true,
          text: null,
          title: 'Check the result of history test',
          type: 'danger',
          icon: 'el-icon-time',
          size: 'small',
          emit: 'goHistoryList',
          show(index, row) {
            return true;
          },
          disabled(index, row) {
            if (row.status === '0') {
              return true;
            } else {
              return false;
            }
          },
          order: 3,
        },
      ],
      fixed: 'right',
    },
    viewOptions: {
      componentType: 'form',
    },
    formOptions: {
      defaultSpan: 24,
      width: '40%',
      labelWidth: '150px',
      labelPosition: 'left',
      saveLoading: false,
      saveButtonType: 'success',
      saveButtonText: 'Create',
    },
    pagination: {
      pageSizes: [10, 20, 50, 100],
      pageSize: 10,
      textAlign: 'center',
    },
    // indexRow: {
    //   title: '序号',
    //   align: 'center'
    // },

    columns: [
      {
        title: 'Project Name',
        key: 'project_name',
        width: 250,
      },
      {
        title: 'Use Case',
        key: 'usercase_name',
        width: 250,
      },
      {
        title: 'Table Name',
        key: 'table_name_mysql',
        width: 250,
      },

      {
        title: 'Table Version',
        key: 'version',
        width: 250,
      },
      {
        title: 'Algorithm Type',
        key: 'algorithm_type',
        width: 250,
      },
      {
        title: 'Task description',
        key: 'description',
        width: 250,
      },
    ],
  };
};
