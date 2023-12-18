import util from '@/libs/util.js';

export default {
  methods: {
    handleMenuSelect(index, indexPath) {
      if (/^d2-menu-empty-\d+$/.test(index) || index === undefined) {
        this.$message.warning('temporary menu');
      } else if (/^https:\/\/|http:\/\//.test(index)) {
        // alert(index)
        console.log('index:', index);
        util.open(index);
      } else {
        this.$router.push({
          path: index,
        });
      }
    },
  },
};
