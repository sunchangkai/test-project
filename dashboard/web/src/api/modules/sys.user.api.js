import { find, assign } from 'lodash';

const users = [
  { username: 'admin', password: 'admin', uuid: 'admin-uuid', name: 'Admin' },
  { username: 'editor', password: 'editor', uuid: 'editor-uuid', name: 'Editor' },
  { username: 'user1', password: 'user1', uuid: 'user1-uuid', name: 'User1' },
];

export default ({ service, request, serviceForMock, requestForMock, mock, faker, tools }) => ({
  /**
   * @description Login
   * @param {Object} data Information carried by login
   */
  SYS_USER_LOGIN(data = {}) {
    // analog data
    mock.onAny('/login').reply(config => {
      const user = find(users, tools.parse(config.data));
      return user
        ? tools.responseSuccess(assign({}, user, { token: faker.random.uuid() }))
        : tools.responseError({}, '账号或密码不正确');
    });
    // Interface Request
    return requestForMock({
      url: '/login',
      method: 'post',
      data,
    });
  },
});
