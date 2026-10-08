export type ModuleRegistration = {
  id: string;
  name?: string;
  description?: string;
  version?: string;
  /** Start background work and return promptly. Use signal to cancel that work. */
  onEnable: (context: { signal: AbortSignal }) => void | Promise<void>;
  /** Stop and await background work before returning. */
  onDisable: () => void | Promise<void>;
  onError?: (error: unknown) => void;
};

export type RegisteredModule = {
  readonly id: string;
  readonly enabled: boolean;
  close(): Promise<void>;
};

/** Serializes lifecycle changes and pauses work whenever status cannot be confirmed. */
export async function watchModule(
  options: ModuleRegistration,
  initialEnabled: boolean,
  heartbeat: () => Promise<boolean>,
): Promise<RegisteredModule> {
  let enabled = false;
  let closed = false;
  let controller: AbortController | undefined;
  let inFlight: Promise<void> | undefined;
  let closing: Promise<void> | undefined;

  function report(error: unknown) {
    try {
      if (options.onError) options.onError(error);
      else console.error(error);
    } catch (callbackError) {
      console.error(callbackError);
    }
  }
  async function stop() {
    enabled = false;
    if (!controller) return;
    controller.abort();
    await options.onDisable();
    controller = undefined;
  }
  async function apply(nextEnabled: boolean) {
    if (!nextEnabled || closed) {
      await stop();
      return;
    }
    if (enabled) return;
    // Retry failed cleanup before starting another job.
    await stop();
    if (closed) return;
    controller = new AbortController();
    enabled = true;
    await options.onEnable({ signal: controller.signal });
  }
  async function fail(error: unknown) {
    try {
      await stop();
    } catch (cleanupError) {
      report(cleanupError);
    }
    report(error);
  }
  try {
    await apply(initialEnabled);
  } catch (error) {
    await fail(error);
  }

  const timer = setInterval(() => {
    if (closed || inFlight) return;
    inFlight = (async () => {
      try {
        await apply(await heartbeat());
      } catch (error) {
        await fail(error);
      }
    })().finally(() => {
      inFlight = undefined;
    });
  }, 30_000);

  return {
    id: options.id,
    get enabled() {
      return enabled;
    },
    close() {
      if (!closing) {
        closed = true;
        enabled = false;
        clearInterval(timer);
        controller?.abort();
        closing = (async () => {
          await inFlight;
          await stop();
        })();
      }
      return closing;
    },
  };
}
