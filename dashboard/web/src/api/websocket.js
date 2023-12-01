import ElementUI from 'element-ui';
import util from '@/libs/util';
import store from '@/store';
function initWebSocket(e) {
  const token = util.cookies.get('token');
  if (token) {
    const wsUri = util.wsBaseURL() + 'ws/' + token + '/';
    this.socket = new WebSocket(wsUri);
    this.socket.onerror = webSocketOnError;
    this.socket.onmessage = webSocketOnMessage;
    this.socket.onclose = closeWebsocket;
  }
}

function webSocketOnError(e) {
  ElementUI.Notification({
    title: '',
    message: 'An error occurred on the WebSocket connection' + JSON.stringify(e),
    type: 'error',
    position: 'bottom-right',
    duration: 3000,
  });
}

function webSocketOnMessage(e) {
  const data = JSON.parse(e.data);
  if (data.contentType === 'SYSTEM') {
    ElementUI.Notification({
      title: 'websocket',
      message: data.content,
      type: 'success',
      position: 'bottom-right',
      duration: 3000,
    });
  } else if (data.contentType === 'ERROR') {
    ElementUI.Notification({
      title: '',
      message: data.content,
      type: 'error',
      position: 'bottom-right',
      duration: 0,
    });
  } else if (data.contentType === 'INFO') {
    ElementUI.Notification({
      title: 'Kind tips',
      message: data.content,
      type: 'success',
      position: 'bottom-right',
      duration: 0,
    });
  } else {
    const { content } = data;
    if (content.model === 'message_center') {
      const unread = content.unread;
      store.dispatch('d2admin/messagecenter/setUnread', unread);
    }
  }
}
function closeWebsocket() {
  ElementUI.Notification({
    title: 'websocket',
    message: 'connection closed...',
    type: 'danger',
    position: 'bottom-right',
    duration: 3000,
  });
}

function webSocketSend(message) {
  this.socket.send(JSON.stringify(message));
}
export default {
  initWebSocket,
  closeWebsocket,
  webSocketSend,
};
