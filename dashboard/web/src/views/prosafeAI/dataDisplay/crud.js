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
      width: 260,
      view: { show: false },
      edit: { show: false },
      remove: { show: false },
      custom: [
        {
          text: 'Visualization',
          type: 'danger',
          size: 'small',
          emit: 'moreDetails',
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
      componentType: 'form',
    },
    formOptions: {
      defaultSpan: 24,
      width: '30%',
    },
    pagination: {
      pageSizes: [10, 20, 50, 100],
      pageSize: 10,
      textAlign: 'center',
    },
    columns: [
      {
        title: 'Project Id',
        key: 'id',
        width: 250,
        show: false,
        form: {
          disabled: true,
        },
      },
      {
        title: 'Project Name',
        key: 'project_name',
        width: 250,
        form: {
          disabled: true,
        },
      },
      {
        title: 'Use Case',
        key: 'usercase_name',
        width: 250,
        form: {
          disabled: true,
        },
      },
      {
        title: 'Table Name',
        key: 'table_name_mysql',
        width: 250,
        form: {
          disabled: true,
        },
      },
      {
        title: 'Table Description',
        key: 'table_description',
        width: 250,
        form: {
          disabled: true,
        },
      },
      {
        title: 'Field Summary',
        key: 'fields',
        showOverflowTooltip: true,
        width: 250,
        rowSlot: true,
        form: {
          disabled: true,
        },
      },
      {
        title: 'Task Type',
        key: 'task_type',
        width: 200,
        rowSlot: true,
        form: {
          disabled: true,
        },
      },
      {
        title: 'Latest Version',
        key: 'latest_version',
        width: 200,
        form: {
          disabled: true,
        },
      },
    ],
  };
};
