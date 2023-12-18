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
          title: 'Download the task report ',
          type: 'primary',
          icon: 'el-icon-download',
          emit: 'downloadReport',
          size: 'small',
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
          title: 'Check the result of history test',
          type: 'danger',
          icon: 'el-icon-view',
          size: 'small',
          emit: 'viewTestResult',
          show(index, row) {
            return true;
          },
          disabled(index, row) {
            return false;
          },
          order: 2,
        },
      ],
      fixed: 'right',
    },
    pagination: false,
    columns: [
      {
        title: 'Run id',
        key: 'id',
        align: 'left',
        width: 100,
      },
      {
        title: 'Task Description',
        key: 'description',
        width: 350,
        align: 'left',
        rowSlot: true,
      },
      {
        title: 'Model Path',
        key: 'model_path',
        width: 350,
        align: 'left',
        rowSlot: true,
      },
      {
        title: 'Data Path',
        key: 'data_path',
        width: 350,
        align: 'left',
        rowSlot: true,
      },
      {
        title: 'Alg Type ',
        key: 'algorithm_type',
        align: 'left',
        width: 150,
      },
      {
        title: 'Create Time',
        key: 'start_time',
        align: 'left',
        width: 200,
      },
    ],
  };
};
