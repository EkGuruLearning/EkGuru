"use strict";

/**
 * Telegram public URL parser.
 *
 * Supports the public URL shapes admins paste into the form:
 *   https://t.me/<username>/<id>
 *   https://t.me/c/<chat_id>/<message_id>[/<topic_id>]
 *   https://t.me/<username>/<topic_thread>/<message_id>   (forum topic links)
 *   https://telegram.me/<username>/<id>
 *
 * Returns a structured reference that the resolver can feed to the MTProto client.
 * Nothing in this module is browser-specific and it does not perform network IO.
 */

const PUBLIC_TG_HOSTS = new Set([
  "t.me",
  "telegram.me",
  "www.t.me",
  "www.telegram.me",
]);

/**
 * @typedef {Object} TelegramReference
 * @property {"public_username"|"private_id"} kind
 * @property {string|number} peer      - username string OR numeric (possibly negative) chat id
 * @property {number} messageId        - target message id within the chat
 * @property {number|null} topicId     - forum topic/thread id if present
 * @property {string} originalUrl      - normalized original URL for logs (do NOT expose publicly)
 */

function normalizeChatId(raw) {
  // /c/<n>/<mid> — Telegram uses MTProto channel id -100<n> for supergroups/channels.
  // https://core.telegram.org/api/links#private-channel-chat-links
  const n = Number(raw);
  if (!Number.isFinite(n) || n <= 0) {
    throw new Error(`Invalid private chat id: ${raw}`);
  }
  return Number("-100" + String(n));
}

/**
 * Parse a Telegram public URL.
 * @param {string} input
 * @returns {TelegramReference}
 */
function parseTelegramUrl(input) {
  if (!input || typeof input !== "string") {
    throw new Error("Telegram URL is required.");
  }
  let url;
  try {
    url = new URL(input.trim());
  } catch (_e) {
    throw new Error("Not a valid URL.");
  }
  if (!PUBLIC_TG_HOSTS.has(url.hostname.toLowerCase())) {
    throw new Error(`Unsupported Telegram host: ${url.hostname}. Only t.me and telegram.me are accepted.`);
  }
  // strip leading/trailing slashes, drop query/hash
  const parts = url.pathname.replace(/^\/+|\/+$/g, "").split("/").filter(Boolean);
  if (parts.length === 0) {
    throw new Error("URL does not point to a specific message.");
  }

  // /c/<chat_id>/<message_id>[/<topic>]
  if (parts[0] === "c") {
    if (parts.length < 3) {
      throw new Error("Private /c/<id>/<mid> link is missing message id.");
    }
    const chatId = normalizeChatId(parts[1]);
    const messageId = Number(parts[2]);
    const topicId = parts[3] ? Number(parts[3]) : null;
    if (!Number.isFinite(messageId) || messageId <= 0) {
      throw new Error("Invalid message id in private link.");
    }
    return {
      kind: "private_id",
      peer: chatId,
      messageId,
      topicId: topicId && Number.isFinite(topicId) ? topicId : null,
      originalUrl: input.trim(),
    };
  }

  // public username links
  const username = parts[0];
  if (!/^[A-Za-z][A-Za-z0-9_]{3,31}$/.test(username)) {
    throw new Error(`Invalid Telegram username: ${username}`);
  }
  let messageId, topicId = null;
  if (parts.length === 2) {
    messageId = Number(parts[1]);
  } else if (parts.length >= 3) {
    // treat first numeric as topic thread id and second as message id
    const a = Number(parts[1]);
    const b = Number(parts[2]);
    if (Number.isFinite(b) && b > 0) {
      topicId = a;
      messageId = b;
    } else {
      messageId = a;
    }
  } else {
    throw new Error("URL does not include a message id. Please link to a specific message containing the PDF.");
  }
  if (!Number.isFinite(messageId) || messageId <= 0) {
    throw new Error("Invalid message id in public link.");
  }
  return {
    kind: "public_username",
    peer: username,
    messageId,
    topicId: topicId && Number.isFinite(topicId) ? topicId : null,
    originalUrl: input.trim(),
  };
}

module.exports = { parseTelegramUrl };
