import ctypes
import os

os.environ["DYLD_LIBRARY_PATH"] = "/opt/homebrew/opt/zbar/lib:" + os.environ.get(
    "DYLD_LIBRARY_PATH", ""
)
ctypes.cdll.LoadLibrary("/opt/homebrew/opt/zbar/lib/libzbar.dylib")
