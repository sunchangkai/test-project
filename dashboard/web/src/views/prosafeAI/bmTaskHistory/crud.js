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
      fit: true,
      rowStyle({ row, rowIndex }) {
        const stylejson = {};
        stylejson.height = 50 + 'px';
        return stylejson;
      },
    },
    //
    rowHandle: {
      columnHeader: 'Operation',
      align: 'center',
      width: 100,
      view: { show: false },
      edit: { show: false },
      remove: { show: false },
      custom: [
        {
          thin: true,
          text: null,
          title: 'Check the test result online ',
          type: 'danger',
          icon: 'el-icon-view',
          size: 'small',
          emit: 'goTaskInfo',
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
    viewOptions: {
      disabled: false,
    },
    pagination: {
      pageSizes: [10, 20, 50, 100],
      pageSize: 10,
      textAlign: 'center',
    },
    columns: [
      {
        title: 'Run ID',
        key: 'id',
        headerAlign: 'center',
        align: 'left',
        width: 100,
      },
      {
        title: 'Algorithm Type',
        key: 'algorithm_type',
        headerAlign: 'center',
        align: 'left',
        width: 150,
      },

      {
        title: 'Task Description',
        key: 'description',
        headerAlign: 'center',
        align: 'left',
        rowSlot: true,
      },
      // {
      //   title: 'Hyperparams',
      //   key: 'hyperparameter',
      //   width: 250,
      //   rowSlot: true
      // },
      {
        title: 'Create Time',
        key: 'start_time',
        headerAlign: 'center',
        align: 'left',
        width: 250,
      },
      {
        title: 'Report',
        key: 'table_id',
        headerAlign: 'center',
        align: 'left',
        width: 100,
        rowSlot: true,
      },
    ],
  };
};
