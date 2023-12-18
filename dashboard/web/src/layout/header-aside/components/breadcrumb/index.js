export default {
  name: 'layout-breadcrumb',
  render(h) {
    return (
      <div>
        <el-breadcrumb class="!leading-[50px] select-none" separator="/">
          {this.levelList.map(i => (
            <el-breadcrumb-item key={i.name}>{i.title}</el-breadcrumb-item>
          ))}
        </el-breadcrumb>
      </div>
    );
  },
  computed: {},
  data() {
    return {
      levelList: [],
    };
  },
  watch: {
    '$route.path': 'getBreadcrumb',
  },
  methods: {
    getBreadcrumb() {
      let menuTree = sessionStorage.getItem('menuData');
      menuTree = JSON.parse(menuTree);
      const currentMenu = menuTree.find(i => i.path === this.$route.path);
      const levelList = this.getLevelList(currentMenu, menuTree);
      this.levelList = levelList;
    },
    getLevelList(currentMenu, menuTree) {
      const _getLevelList = (curr, menus, levelList = []) => {
        levelList.unshift(curr);
        if (curr?.parent) {
          const parentMenu = menus.find(i => i.id === curr.parent);
          _getLevelList(parentMenu, menus, levelList);
        }
        return levelList;
      };

      return _getLevelList(currentMenu, menuTree);
    },
  },
  mounted() {
    this.getBreadcrumb();
  },
};
