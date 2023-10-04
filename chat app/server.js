const WebSocket = require('ws');
const http = require('http');
const url = require('url');
const { v4: uuidv4 } = require('uuid');

class ChatRoom {
  constructor(roomID) {
    this.roomID = roomID;
    this.clients = [];
  }

  static getInstance(roomID) {
    if (!this.instance) {
      this.instance = new ChatRoom(roomID);
    }
    return this.instance;
  }

  addClient(client) {
    this.clients.push(client);
  }

  removeClient(client) {
    const index = this.clients.indexOf(client);
    if (index !== -1) {
      this.clients.splice(index, 1);
    }
  }

  broadcast(message, sender) {
    this.clients.forEach((client) => {
      if (client !== sender) {
        client.sendMessage(message);
      }
    });
  }
}

class ChatClient {
  constructor(ws, chatRoom) {
    this.ws = ws;
    this.chatRoom = chatRoom;
    this.chatRoom.addClient(this);
  }

  sendMessage(message) {
    this.ws.send(message);
  }
}

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('WebSocket server is running');
});

const wss = new WebSocket.Server({ noServer: true });

const rooms = {};

wss.on('connection', (ws, req) => {
  const roomID = url.parse(req.url, true).query.room;

  if (!roomID) {
    ws.close();
  }

  if (!rooms[roomID]) {
    rooms[roomID] = ChatRoom.getInstance(roomID);
  }

  new ChatClient(ws, rooms[roomID]);

  ws.on('message', (message) => {
    rooms[roomID].broadcast(message, ws);
  });

  ws.on('close', () => {
    rooms[roomID].removeClient(ws);
  });
});

server.on('upgrade', (request, socket, head) => {
  wss.handleUpgrade(request, socket, head, (ws) => {
    wss.emit('connection', ws, request);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`WebSocket server is listening on port ${PORT}`);
});
