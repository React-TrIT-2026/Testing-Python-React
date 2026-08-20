const { performance } = require("node:perf_hooks");
const { ReadableStream, TransformStream, WritableStream } = require("node:stream/web");
const { clearImmediate, setImmediate } = require("node:timers");
const { TextDecoder, TextEncoder } = require("node:util");
const { BroadcastChannel, MessageChannel, MessagePort } = require("node:worker_threads");

function define(values) {
  for (const [name, value] of Object.entries(values)) {
    Object.defineProperty(globalThis, name, {
      value,
      writable: true,
      configurable: true,
    });
  }
}

define({
  TextEncoder,
  TextDecoder,
  ReadableStream,
  TransformStream,
  WritableStream,
  BroadcastChannel,
  MessageChannel,
  MessagePort,
  performance,
  setImmediate,
  clearImmediate,
});

const { fetch: undiciFetch, Headers, FormData, Request, Response } = require("undici");

function absolute(input) {
  if (typeof input === "string" && input.startsWith("/")) {
    return new URL(input, globalThis.location?.origin ?? "http://localhost").href;
  }
  return input;
}

const fetch = (input, init) => undiciFetch(absolute(input), init);

define({ fetch, Headers, FormData, Request, Response });
