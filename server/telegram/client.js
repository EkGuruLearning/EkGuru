"use strict";

/**
 * Telegram MTProto client wrapper for EkGuru.
 *
 * Exposes only the operations the PDF gateway needs:
 *   - resolveEntity(username|chatId)
 *   - getMessage(ref)                 -> message with media
 *   - downloadDocumentChunk(doc, {offset, limit}) -> Buffer
 *   - isReady() / connect()
 *
 * Uses teleproto (maintained GramJS fork). Credentials come from env
 * (TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION).
 *
 * Also supports a MOCK mode for tests/dev: set ALLOW_MOCK_TELEGRAM=true
 * and TELEGRAM_MOCK_DIR=<path>. In mock mode the resolver reads local
 * fixture files instead of calling Telegram. Production MUST NOT run in
 * mock mode; the server refuses to start PDF routes if both mock mode
 * is allowed and NODE_ENV=production.
 */

const fs = require("fs");
const path = require("path");
const { TelegramClient, Api, sessions, errors, Logger } = require("teleproto");

const DEFAULT_LOG_LEVEL = "none";

class EkGuruTelegramClient {
  constructor(options = {}) {
    this.apiId = parseInt(options.apiId || process.env.TELEGRAM_API_ID || "0", 10);
    this.apiHash = options.apiHash || process.env.TELEGRAM_API_HASH || "";
    this.sessionString = options.sessionString || process.env.TELEGRAM_SESSION || "";
    this.mockAllowed = String(process.env.ALLOW_MOCK_TELEGRAM || options.mockAllowed || "false").toLowerCase() === "true";
    this.mockDir = options.mockDir || process.env.TELEGRAM_MOCK_DIR || path.join(__dirname, "..", "..", "data", "mock-telegram");
    this.mockMode = false; // enabled when connect() detects mock
    this.client = null;
    this.connected = false;
    this._connectPromise = null;
    this._entityCache = new Map();
    this._logger = options.logger || null;
  }

  log(level, ...args) {
    if (this._logger) this._logger(level, ...args);
  }

  /**
   * Check configuration and connect to Telegram.
   * If real credentials are missing but mock is allowed, fall into mock mode.
   */
  async connect() {
    if (this._connectPromise) return this._connectPromise;
    this._connectPromise = (async () => {
      if ((!this.apiId || !this.apiHash || !this.sessionString) && this.mockAllowed) {
        this.log("warn", "[telegram] Real credentials missing; using MOCK mode (ALLOW_MOCK_TELEGRAM=true).");
        this.mockMode = true;
        this.connected = true;
        return;
      }
      if (!this.apiId || !this.apiHash || !this.sessionString) {
        throw new Error(
          "Telegram credentials not configured. Set TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION. " +
          "Or for tests only set ALLOW_MOCK_TELEGRAM=true."
        );
      }
      const session = new sessions.StringSession(this.sessionString);
      this.client = new TelegramClient(session, this.apiId, this.apiHash, {
        connectionRetries: 3,
        useWSS: true,
        autoReconnect: true,
        langCode: "en",
        // Silence lib logs in production
        baseLogger: Logger.setLevel(DEFAULT_LOG_LEVEL),
      });
      await this.client.connect();
      if (!(await this.client.isUserAuthorized())) {
        throw new Error("Telegram session is not authorized. Run `npm run telegram:login` to authorize.");
      }
      this.connected = true;
      this.log("info", "[telegram] Client connected and authorized.");
    })();
    return this._connectPromise;
  }

  isReady() {
    return this.connected;
  }

  /**
   * Resolve a peer identifier to an InputPeer-style object teleproto expects.
   * Usernames are cached for the process lifetime.
   * @param {string|number} peer
   */
  async resolvePeer(peer) {
    if (this.mockMode) {
      return { _: "mockPeer", id: String(peer) };
    }
    const key = String(peer).toLowerCase();
    if (this._entityCache.has(key)) return this._entityCache.get(key);
    // getEntity accepts either a username string or a numeric id (negative for channels).
    const entity = await this.client.getEntity(peer);
    this._entityCache.set(key, entity);
    return entity;
  }

  /**
   * Fetch the message at `ref` and return it along with the resolved entity.
   * @param {import('./url-parser').TelegramReference} ref
   */
  async getMessage(ref, { forceRefresh = false } = {}) {
    if (!this.connected) await this.connect();

    if (this.mockMode) {
      return this._mockGetMessage(ref);
    }

    const entity = await this.resolvePeer(ref.peer);
    // For channel/supergroup entities, use InputChannel (need access_hash from resolve)
    const inputPeer = this._toInputPeer(entity);

    const replyTo = ref.topicId ? { replyToMsgId: ref.topicId } : undefined;
    // getMessages returns array of messages by ID
    const iter = await this.client.getMessages(inputPeer, {
      ids: [ref.messageId],
      replyTo,
    });
    const msg = Array.isArray(iter) ? iter[0] : null;
    if (!msg) {
      const err = new Error("Telegram message not found.");
      err.code = "TG_MSG_NOT_FOUND";
      throw err;
    }
    if (msg.className === "MessageEmpty") {
      const err = new Error("Telegram message is empty or inaccessible.");
      err.code = "TG_MSG_EMPTY";
      throw err;
    }
    return { message: msg, entity, ref };
  }

  _toInputPeer(entity) {
    if (!entity) throw new Error("Cannot build InputPeer from null entity.");
    if (entity.className === "Channel" || entity._ === "channel") {
      return new Api.InputPeerChannel({ channelId: entity.id, accessHash: entity.accessHash });
    }
    if (entity.className === "Chat" || entity._ === "chat") {
      return new Api.InputPeerChat({ chatId: entity.id });
    }
    if (entity.className === "User" || entity._ === "user") {
      return new Api.InputPeerUser({ userId: entity.id, accessHash: entity.accessHash });
    }
    return entity;
  }

  /**
   * Download a slice of a Document. Returns Buffer.
   * @param {object} doc          - document media object from message.media.document
   * @param {object} range
   * @param {number} range.offset
   * @param {number} range.limit
   */
  async downloadDocumentChunk(doc, { offset, limit }) {
    if (!this.connected) await this.connect();
    if (this.mockMode) {
      return this._mockDownload(doc, offset, limit);
    }
    try {
      const buf = await this.client.downloadFile(doc, {
        dcId: doc.dcId,
        fileSize: Number(doc.size || 0),
        workers: 1,
        offset,
        limit,
      });
      return Buffer.from(buf);
    } catch (err) {
      // Translate "file reference expired" errors into a known code
      if (err && err.message && /FILE_REFERENCE.*EXPIRED/i.test(String(err.message))) {
        const e = new Error("Telegram file reference expired; refresh the message and retry.");
        e.code = "TG_FILE_REF_EXPIRED";
        throw e;
      }
      throw err;
    }
  }

  async getFileInfo(doc) {
    // Returns { size, mimeType, name }
    const nameAttr = doc.attributes && doc.attributes.find((a) => a.className === "DocumentAttributeFilename");
    return {
      size: Number(doc.size || 0),
      mimeType: doc.mimeType || "application/octet-stream",
      name: nameAttr ? String(nameAttr.fileName) : "download",
      id: String(doc.id),
    };
  }

  // -------- Mock implementations (tests/dev only) --------
  _mockGetMessage(ref) {
    // We expect a mock file tree under mockDir/<slug>/<messageId>/...
    // For private links, slug is derived from the MTProto peer id (e.g. c1004430299776).
    let slug;
    if (typeof ref.peer === "number") {
      slug = "c" + String(Math.abs(ref.peer));
    } else {
      slug = String(ref.peer);
    }
    const msgDir = path.join(this.mockDir, slug, String(ref.messageId));
    const metaPath = path.join(msgDir, "meta.json");
    const pdfPath = path.join(msgDir, "file.pdf");
    if (!fs.existsSync(metaPath) || !fs.existsSync(pdfPath)) {
      const err = new Error("Mock Telegram message not found.");
      err.code = "TG_MSG_NOT_FOUND";
      throw err;
    }
    const meta = JSON.parse(fs.readFileSync(metaPath, "utf8"));
    const stat = fs.statSync(pdfPath);
    const doc = {
      _: "mockDocument",
      id: meta.id || String(ref.messageId),
      dcId: 0,
      size: BigInt(stat.size),
      mimeType: meta.mimeType || "application/pdf",
      attributes: [{ className: "DocumentAttributeFilename", fileName: meta.name || "mock.pdf" }],
      _mockPath: pdfPath,
    };
    const msg = {
      id: ref.messageId,
      media: { className: "MessageMediaDocument", document: doc },
      // noforwards flag simulation
      noforwards: Boolean(meta.noforwards),
    };
    return { message: msg, entity: { _: "mockPeer", id: ref.peer }, ref };
  }

  _mockDownload(doc, offset, limit) {
    if (!doc._mockPath) throw new Error("Mock download missing path");
    const fd = fs.openSync(doc._mockPath, "r");
    try {
      const buf = Buffer.alloc(limit);
      const read = fs.readSync(fd, buf, 0, limit, offset);
      return buf.slice(0, read);
    } finally {
      fs.closeSync(fd);
    }
  }
}

module.exports = { EkGuruTelegramClient };
