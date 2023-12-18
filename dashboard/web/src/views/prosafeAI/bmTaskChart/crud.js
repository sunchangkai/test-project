/*
 * @Author: zhaoyang8710
 * @Date: 2023-07-11 10:51:55
 * @LastEditors: zhaoyang8710
 * @LastEditTime: 2023-10-27 16:10:54
 * @FilePath: /prosafeai-prosafeai-main/dashboard/web/src/views/prosafeAI/bmTaskChart/crud.js
 */
export let crudOptions;
// eslint-disable-next-line prefer-const
crudOptions = vm => {
  return {
    options: {
      tableType: 'vxe-table',
      size: 'medium',
      rowKey: false,
      height: '100%',
      rowId: 'id',
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
          text: 'More features',
          type: 'warning',
          size: 'small',
          emit: 'moreFeatures',
          show(index, row) {
            return true;
          },
          disabled(index, row) {
            return false;
          },
          order: 1,
        },
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
    columns: [],
  };
};
